from plush_tokenizer import tokenize
from plush_parser import parse
from plush_typechecker import verify
from plush_compiler import compile
from context import Context
from emitter import Emitter

source_code = '''
var x : int := 1;
var y : int := 1 + 2;

var z : int := x + y;

function print_int(var x : int) : void;
'''
tokens = tokenize(source_code)
for token in tokens:
    print(token)

ast = parse(tokens)

# type check the ast
typed_ast = verify(ast, Context())

llvm_code = compile(typed_ast, Emitter())

for line in llvm_code:
    print(line)