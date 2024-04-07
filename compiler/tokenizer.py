import re

TOKEN_TYPES = [
    ('VAL', r'val'),
    ('VAR', r'var'),
    ('IF', r'if'),
    ('THEN', r'then'),
    ('ELSE', r'else'),
    ('WHILE', r'while'),
    ('TYPE', r'double|int|string|void'),
    ('VNAME', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMBER', r'\d+(\.\d*)?'),
    ('STRING', r'\".*?\"|\'.*?\''),
    ('OPERATOR', r'[\!\&\|\<\>\=\+\-\*\/\%]'),
    ('ASSIGNMENT', r'\:\='),
    ('SEPARATOR', r'[\{\}\[\];,:]'),  # Modified to remove parentheses
    ('WHITESPACE', r'\s+'),
    ('COMMENT', r'\#.*'),  # Single-line comments starting with #
]

def tokenize(source_code):
    tokens = []
    pos = 0

    while pos < len(source_code):
        match = None
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(source_code, pos)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE' and token_type != 'COMMENT':
                    tokens.append((token_type, value))
                break
        if not match:
            raise Exception(f"Invalid token: {source_code[pos]} at position {pos}")
        else:
            pos = match.end()

    return tokens
