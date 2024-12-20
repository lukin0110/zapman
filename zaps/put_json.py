###################################
# $ zap run put_json.py
###################################
PUT = "https://httpbin.org/put"

HEADERS = {
    "Content-Type": "application/json",
}

# Put a JSON string in the body
BODY_RAW = """
{
    "bttf": {"great": "scott", "biff": "Tannen"},
    "enabled": true,
    "float": 3.007,
    "empty": null
}
"""
