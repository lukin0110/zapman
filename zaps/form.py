from zapman import env

POST = f"{env['endpoint']}/post"

BODY_FORM = {
    "name": "Eddie",
    "last_name": "Vedder",
}

COOKIES = {
    "session": "123",
    "foo": "bar",
}
