###################################
# $ zap run store.py
# $ zap vars
###################################
from zapman import After, env

GET = f"{env['endpoint']}/get"

PARAMS = {
    "foo": "bar",
}


def after(ctx: After) -> None:
    env["my_var"] = ctx.json["args"]
    env["my_date"] = ctx.headers["Date"]
