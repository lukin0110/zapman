###################################
# $ zap run download.py
###################################
from zapman import After

GET = "https://httpbin.org/get"

DOWNLOAD = True


def after(ctx: After) -> None:
    if ctx.output_file:
        ctx.info(f"Downloaded 🤘: {ctx.output_file.absolute()}")
