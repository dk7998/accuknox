import re

def is_email(value: str) -> bool:
    if re.match(r"[^@]+@[^@]+\.[^@]+", value):
        return True
    else:
        return False