import os
import json

def save_cookies(cookie,accountNumber):
    """Save cookies from cookie dict to a JSON file."""
    folder = f'accounts/{accountNumber}/cookies'
    filename = f"{folder}/cookie.json"
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(cookie, f)
    except Exception as e:
        print(f"Error saving cookies: {e}")        

def load_cookies(accountNumber):
    """Load cookies from a JSON file and return them as a dict."""
    folder = f'accounts/{accountNumber}/cookies'
    filename = f"{folder}/cookie.json"
    with open(filename, "r") as f:
        cookie = json.load(f)
    return cookie

