from plush_tokenizer import tokenize
from plush_parser import parse
import json
import sys

source_code = ""

# read lines from a file and compact them into a single string
with open(sys.argv[1], 'r') as f:
    source_code = f.read()

tokens = tokenize(source_code)
ast = parse(tokens)
print(json.dumps(ast.to_dict(), indent=4))