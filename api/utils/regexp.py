import re

def match_pattern(pattern: str, string: str):
    mathched = re.match(pattern, string)
    is_valid = bool(mathched)
    if not is_valid: raise Exception(f'{string} does not match the requested pattern')
    return is_valid