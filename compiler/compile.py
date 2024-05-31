from plush_tokenizer import tokenize
from plush_parser import parse
from plush_typechecker import verify
from plush_compiler import compile
from context import Context
from emitter import Emitter
import json
import sys

source_code = ""

# read lines from a file and compact them into a single string
with open(sys.argv[1], 'r') as f:
    source_code = f.read()
tokens = tokenize(source_code)

ast = parse(tokens)

# type check the ast
context = Context()
context.enter_function_def_scope()
context.set_type_function_def("printf", "void")
typed_ast = verify(ast, context)

emitter = Emitter()
emitter.function_declarations.append("declare double @pow(ptr noundef, ...)\n")
llvm_code = compile(typed_ast, emitter)

# write to llvm file
with open('output.ll', 'w') as f:
    for line in llvm_code:
        f.write(line + '\n')