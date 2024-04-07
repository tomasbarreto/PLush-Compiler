import re

TOKEN_TYPES = [
    ('VAL', r'val'),
    ('VAR', r'var'),
    ('IF', r'if'),
    ('ELSE', r'else'),
    ('WHILE', r'while'),
    ('FUNCTION', r'function'),
    ('RETURN', r'return'),
    ('TYPE', r'double|int|string|void'),
    ('BOOLEAN', r'true|false'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMBER', r'\d+(\.\d*)?'),
    ('STRING', r'\".*?\"|\'.*?\''),
    ('LOGICOPERATOR', r'\&\&|\|\||\!|\<\=|\>\=|\>|\<|\=|\!\='),
    ('NOTEQUALS', r'\!\='),
    ('ADDICTIONOPERATOR', r'[\+\-]'),
    ('MULTIPLICATIONOPERATOR', r'[\*\/\%]'),
    ('ASSIGNMENT', r'\:\='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LRECPAREN', r'\['),
    ('RRECPAREN', r'\]'),
    ('LCURLYPAREN', r'\{'),
    ('RCURLYPAREN', r'\}'),
    ('COMMA', r'\,'),
    ('SEMICOLON', r'\;'),
    ('COLON', r'\:'),
    ('WHITESPACE', r'\s+'),
    ('COMMENT', r'\#.*'),
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
