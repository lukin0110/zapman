###################################
# $ zap run get.py
# $ zap run --env pie get.py
###################################
from zapman import env

GET = f"{env['endpoint']}/get"

PARAMS = {
    "foo": "bar",
}
