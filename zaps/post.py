###################################
# $ zap run post.py
###################################
from zapman import env

POST = f"{env['endpoint']}/post"

HEADERS = {
    "X-Dude": "Duderino",
}

BODY_JSON = {
    "name": "Jeffrey",
    "last_name": "Lebowski",
    "endpoint": env["endpoint"],
}
