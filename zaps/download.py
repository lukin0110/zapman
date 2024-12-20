###################################
# $ zap run download.py
###################################
from zapman import After

GET = "https://httpbin.org/get"

DOWNLOAD = True


def after(ctx: After) -> None:
    ctx.info("Downloaded 🤘")
    if ctx.output_file:
        print(ctx.output_file.read_text())
