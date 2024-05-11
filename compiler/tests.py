from plush_tokenizer import tokenize
from plush_parser import parse
from plush_typechecker import verify
from plush_compiler import compile
from context import Context
from emitter import Emitter

source_code = '''
var x : int := 5;
var y : int := 10;

function add(var x : int, var y : int) : int {
    var isA : boolean := true;
    var isB : boolean := false;
    var isC : boolean := true;

    while isA && isB || isC {
        x := x + 1;
    }

    add := 2;
}
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

# write to llvm file
with open('output.ll', 'w') as f:
    for line in llvm_code:
        f.write(line + '\n')