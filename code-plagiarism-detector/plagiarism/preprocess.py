import re

def preprocess(code):
    # remove comments
    code = re.sub(r'#.*|//.*', '', code)
    # remove extra spaces and empty lines
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    return "\n".join(lines)

