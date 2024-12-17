# ruff: noqa: C901, PGH004, PLR0912, PLR0915, D400, D401, TC002, RET503
"""A wrapper class around HTTPie's program function.

Wrapper is needed to capture the response, content and/or output file of the request. The `program` function is largely
copied from HTTPie's core.py file and slightly modified to capture the response, content and/or output file.

HTTPie's program function
-------------------------
https://github.com/httpie/cli/blob/2843b874c60bda30e7393f0500353b6fe8451542/httpie/core.py#L170
"""

import argparse
from pathlib import Path
from typing import Any, ClassVar

import requests
from httpie.cli.constants import OUT_REQ_BODY
from httpie.client import collect_messages
from httpie.context import Environment, LogLevel
from httpie.downloads import Downloader
from httpie.models import OutputOptions, RequestsMessageKind
from httpie.output.models import ProcessingOptions
from httpie.output.writer import MESSAGE_SEPARATOR_BYTES, write_message, write_raw_data, write_stream
from httpie.status import ExitStatus, http_status_to_exit_status


class ZapProgramWrapper:
    __attrs__: ClassVar = ["response", "content"]

    def __init__(self) -> None:
        self.response: requests.Response | None = None
        self.content: bytes | None = None
        self.output_file: Path | None = None

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.program(
            args=kwargs["args"],
            env=kwargs["env"],
        )

    def program(self, args: argparse.Namespace, env: Environment) -> ExitStatus:
        """The main program without error handling"""
        # TODO: Refactor and drastically simplify, especially so that the separator logic is elsewhere.
        exit_status = ExitStatus.SUCCESS
        downloader = None
        initial_request: requests.PreparedRequest | None = None
        final_response: requests.Response | None = None
        processing_options = ProcessingOptions.from_raw_args(args)

        def separate() -> None:
            getattr(env.stdout, "buffer", env.stdout).write(MESSAGE_SEPARATOR_BYTES)

        def request_body_read_callback(chunk: bytes) -> Any:
            should_pipe_to_stdout = bool(
                # Request body output desired
                OUT_REQ_BODY in args.output_options
                # & not `.read()` already pre-request (e.g., for  compression)
                and initial_request
                # & non-EOF chunk
                and chunk
            )
            if should_pipe_to_stdout:
                return write_raw_data(
                    env,
                    chunk,
                    processing_options=processing_options,
                    headers=initial_request.headers,  # type: ignore[union-attr]
                )

        try:
            if args.download:
                args.follow = True  # --download implies --follow.
                downloader = Downloader(env, output_file=args.output_file, resume=args.download_resume)
                downloader.pre_request(args.headers)
            messages = collect_messages(env, args=args, request_body_read_callback=request_body_read_callback)
            force_separator = False
            prev_with_body = False

            messages = list(messages)
            self.response = messages[1]
            self.content = self.response.content  # type: ignore[union-attr]

            # Process messages as they're generated
            for message in messages:
                output_options = OutputOptions.from_message(message, args.output_options)

                do_write_body = output_options.body
                if prev_with_body and output_options.any() and (force_separator or not env.stdout_isatty):
                    # Separate after a previous message with body, if needed. See test_tokens.py.
                    separate()
                force_separator = False
                if output_options.kind is RequestsMessageKind.REQUEST:
                    if not initial_request:
                        initial_request = message
                    if output_options.body:
                        is_streamed_upload = not isinstance(message.body, str | bytes)
                        do_write_body = not is_streamed_upload
                        force_separator = is_streamed_upload and env.stdout_isatty
                else:
                    final_response = message
                    if args.check_status or downloader:
                        exit_status = http_status_to_exit_status(http_status=message.status_code, follow=args.follow)
                        if exit_status != ExitStatus.SUCCESS and (not env.stdout_isatty or args.quiet == 1):
                            env.log_error(f"HTTP {message.raw.status} {message.raw.reason}", level=LogLevel.WARNING)
                write_message(
                    requests_message=message,
                    env=env,
                    output_options=output_options._replace(body=do_write_body),
                    processing_options=processing_options,
                )
                prev_with_body = output_options.body

            # Cleanup
            if force_separator:
                separate()
            if downloader and exit_status == ExitStatus.SUCCESS:
                # Last response body download.
                download_stream, download_to = downloader.start(
                    initial_url=initial_request.url,  # type: ignore[union-attr]
                    final_response=final_response,
                )
                write_stream(stream=download_stream, outfile=download_to, flush=False)
                downloader.finish()
                if downloader.interrupted:
                    exit_status = ExitStatus.ERROR
                    env.log_error(
                        f"Incomplete download: size={downloader.status.total_size};"
                        f" downloaded={downloader.status.downloaded}"
                    )
            return exit_status

        finally:
            if downloader and not downloader.finished:
                downloader.failed()

            if args.output_file and args.output_file_specified:
                args.output_file.close()

            if downloader:
                if args.output_file and args.output_file_specified:
                    self.output_file = Path(args.output_file.name)
                elif downloader._output_file:  # noqa: SLF001
                    self.output_file = Path(downloader._output_file.name)  # noqa: SLF001
