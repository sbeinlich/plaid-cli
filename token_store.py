"""
Write Access tokens to a simple text file to persist between sessions.
TODO: In the future, can migrate this to a SQLite DB if our app has other
persistent storage needs.
"""

from pathlib import Path

STORE_DIR = Path("store/")
STORE_DIR.mkdir(parents=True, exist_ok=True)
ACCESS_TOKEN_STORE_PATH = STORE_DIR / "access_tokens.txt"

def fetch_tokens():
    tokens = []
    try:
        with open(ACCESS_TOKEN_STORE_PATH, "r") as f:
            for line in f:
                line = line.rstrip('\n')
                tokens.append(line)
    except FileNotFoundError:
        f = open(ACCESS_TOKEN_STORE_PATH, "x")
        f.close()
    return tokens

def add_token(token):
    tokens = fetch_tokens()
    if token in tokens:
        return

    with open(ACCESS_TOKEN_STORE_PATH, "a") as f:
        f.write(f"{token}\n")

def remove_token(token):
    tokens = fetch_tokens()
    if token not in tokens:
        return

    tokens.remove(token)
    with open(ACCESS_TOKEN_STORE_PATH, "w") as f:
        for token in tokens:
            f.write(f"{token}\n")
