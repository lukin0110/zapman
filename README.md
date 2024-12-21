[![Lint and Test](https://github.com/lukin0110/zapman/actions/workflows/test.yml/badge.svg)](https://github.com/lukin0110/zapman/actions)

# 🌐 Zapman

An API Client for the terminal. A Python CLI for API testing and development.

```bash
usage: zap [-h] {run,curl,cookies,vars,version} ...

An API Client for the terminal. A Python CLI for API testing and development.

options:
  -h, --help            show this help message and exit

commands:
  {run,curl,cookies,vars,version}
    run                 🚀 run a Zapfile
    curl                🌊 print the curl command for a Zapfile
    cookies             🍪 view stored cookies
    vars                📋 view stored variables
    version             🔖 show version
```

## ✨ Features

- 🐍 Define requests with pure python
- 🛠️ Environments & variables
- 🔄 Scriptable: parse responses, update environment variables, etc.
- 🚀 Collaborate and share via Git (they’re just Python files 🤷🏽‍♀️)
- 🖥️ Lightweight and simple CLI 
- 🌈 Beautiful & colored output

## 🚀 Using

To install this package, run:
```bash
pip install zapman
```

### `GET` request

Create a `Zapfile` called `get.py`:
```python
GET = "https://httpbin.org/get"

PARAMS = {
    "foo": "bar"
}
```

Run with:
```bash
zap run get.py
```

Output:
```bash
GET /get?foo=bar HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: httpbin.org
User-Agent: Zapman/0.0.0



HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: *
Connection: keep-alive
Content-Length: 325
Content-Type: application/json
Date: Thu, 19 Dec 2024 23:26:56 GMT
Server: gunicorn/19.9.0

{
    "args": {
        "foo": "bar"
    },
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "httpbin.org",
        "User-Agent": "Zapman/0.0.0",
        "X-Amzn-Trace-Id": "Root=1-6764abbf-60e6ac856a6fe7c32c0e2f3b"
    },
    "origin": "0.0.0.0",
    "url": "https://httpbin.org/get?foo=bar"
}


Elapsed time: 1.10440575s
```

### `POST` request

Create a `Zapfile` called `post.py`:
```python
POST = "https://httpbin.org/post"

BODY_FORM = {
    "foo": "bar"
}
```

Run with:
```bash
zap run post.py
```

Output:
```bash
POST /post HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 7
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Host: httpbin.org
User-Agent: Zapman/0.0.1

foo=bar


HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: *
Connection: keep-alive
Content-Length: 482
Content-Type: application/json
Date: Sat, 21 Dec 2024 13:54:44 GMT
Server: gunicorn/19.9.0

{
    "args": {},
    "data": "",
    "files": {},
    "form": {
        "foo": "bar"
    },
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "7",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Host": "httpbin.org",
        "User-Agent": "Zapman/0.0.1",
        "X-Amzn-Trace-Id": "Root=1-6766c8a4-19b2d0c813b7161f02cc4b30"
    },
    "json": null,
    "origin": "0.0.0.0",
    "url": "https://httpbin.org/post"
}


Elapsed time: 0.479004791s
```

### Print `cURL` command

Create a `Zapfile` called `put_json.py`:
```python
PUT = "https://httpbin.org/put"

HEADERS = {
    "X-Dude": "Duderino",
}

BODY_JSON = {
    "name": "Jeffrey",
    "last_name": "Lebowski",
}
```

Run with:
```bash
zap curl put_json.py
```

Output:
```bash
curl -i -X PUT 'https://httpbin.org/put' \
--header 'X-Dude: Duderino' \
--header 'Content-Type: application/json' \
--data '{"name": "Jeffrey", "last_name": "Lebowski"}'
```

### Store environment variables

Create an _"environments"_ file called `zapenvs.py`:
```python
def env_default() -> dict[str, str]:
    """Provide default environment."""
    return {
        "endpoint": "https://httpbin.org",
    }
```

Create a `Zapfile` called `store.py`:
```python
from zapman import After, env

GET = f"{env['endpoint']}/get"

PARAMS = {
    "foo": "bar",
}


def after(ctx: After) -> None:
    env["my_var"] = ctx.json["args"]
    env["my_date"] = ctx.headers["Date"]
```

Run with:
```bash
zap run --quiet store.py
zap vars
```

Output:
```bash
Environment: default
  my_var={'foo': 'bar'}
  my_date=Sat, 21 Dec 2024 22:57:38 GMT
```


### More examples

More example `Zapfiles` can be found in [zaps](zaps). Dive deeper on how to use environments, environment variables and cookies.

## 🧑‍💻 Contributing

<details>
<summary>Prerequisites</summary>

<details>
<summary>1. Install Docker</summary>

1. Go to [Docker](https://www.docker.com/get-started), download and install docker.
2. [Configure Docker to use the BuildKit build system](https://docs.docker.com/build/buildkit/#getting-started). On macOS and Windows, BuildKit is enabled by default in Docker Desktop.

</details>

<details>
<summary>2. Install VS Code</summary>

Go to [VS Code](https://code.visualstudio.com/), download and install VS Code.
</details>


</details>

#### 1. Open DevContainer with VS Code
Open this repository with VS Code, and run <kbd>Ctrl/⌘</kbd> + <kbd>⇧</kbd> + <kbd>P</kbd> → _Dev Containers: Reopen in Container_.

The following commands can be used inside a DevContainer.

#### 2. Run linters
```bash
poe lint
```

#### 3. Run tests
```bash
poe test
```

#### 4. Update poetry lock file
```bash
poetry lock --no-update
```

---
See how to develop with [PyCharm or any other IDE](https://github.com/lukin0110/poetry-copier/tree/main/docs/ide.md).

---
️⚡️ Scaffolded with [Poetry Copier](https://github.com/lukin0110/poetry-copier/).\
🛠️ [Open an issue](https://github.com/lukin0110/poetry-copier/issues/new) if you have any questions or suggestions.
