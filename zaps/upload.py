from zapman import env

BOUNDERY = "----ZapmanBoundary1234"

POST = f"{env['endpoint']}/files/"

HEADERS = {
    "X-API-Key": "dummy",
    "Content-Type": f"multipart/form-data; boundary={BOUNDERY}",
}

BODY_RAW = f"""
--{BOUNDERY}\r
Content-Disposition: form-data; name="file"; filename="zappy.txt"\r
Content-Type: text/plain\r\n\r
Hello, World!\r
Hello, Dude!\r
--{BOUNDERY}--\r
"""
