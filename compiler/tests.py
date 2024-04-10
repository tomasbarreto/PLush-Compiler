from tokenizer import tokenize
from plush_parser import parse

source_code = '''
a := 2 * 2 - 3 * 2;

'''
tokens = tokenize(source_code)
for token in tokens:
    print(token)

parse(tokens)
