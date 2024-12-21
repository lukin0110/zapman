###################################
# $ zap run get.py
# $ zap --env pie run get.py
###################################
from zapman import env

GET = f"{env['endpoint']}/get"

PARAMS = {
    "foo": "bar",
}
