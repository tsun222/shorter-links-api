import string
import secrets

alphanumeric_chars = string.ascii_letters + string.digits
URL_CODE_LENGTH = 8

def generate_random_url_code():
    return "".join(secrets.choice(alphanumeric_chars) for _ in range(URL_CODE_LENGTH))

def is_valid_code(code: str):
    return isinstance(code, str) and len(code) == 8 and code.isalnum()