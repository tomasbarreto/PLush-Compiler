from plush_tokenizer import tokenize
from plush_parser import parse
from plush_typechecker import verify
from plush_compiler import compile
from context import Context
from emitter import Emitter

source_code = '''
function print_int(var x : int) : void;

function main() : void {
    var x : int := 5;
    var y : int := 10;

    var isA : boolean := true;
    var isB : boolean := false;
    var isC : boolean := true;

    while isA && isB || isC {
        x := x + 1;
        print_int(x);
    }
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