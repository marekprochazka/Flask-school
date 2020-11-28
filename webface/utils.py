from random import choice 
import string
from flask import request


def generate_short_url(existing=[]):
    chars = list(string.ascii_letters + "0123456789")
    result = ""
    for _ in range(6):
        result += choice(chars)
    if result in existing:
        result = generate_short_url(existing)
    return result

def add_url_to_shortcut(shortcut):
    return f"{request.url}{shortcut}"