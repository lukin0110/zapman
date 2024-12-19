[![Lint and Test](https://github.com/lukin0110/zapman/actions/workflows/test.yml/badge.svg)](https://github.com/lukin0110/zapman/actions)

# 🌐 Zapman

An API Client for the terminal. A Python CLI for API testing and development.

## ✨ Features

- 🛠️ Environments & variables
- 🔄 Scriptable & easily shareable via git
- 🖥️ A simple and small CLI 
- 🌈 Colored output
- 🐍 Pure python

## 🚀 Using

To install this package, run:
```bash
pip install zapman
```

Create a `Zapfile` called `get.py` (_`Zapfiles` are just regular python files_):
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

More example `Zapfiles` in [zaps](zaps).

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
