from plush_tokenizer import tokenize
from plush_parser import parse
from plush_typechecker import verify
from plush_compiler import compile
from context import Context
from emitter import Emitter

source_code = '''
val m1_rows : int := 3;
val m1_cols : int := 2;
val m2_rows : int := 2;
val m2_cols : int := 2;

function get_array2d(val rows : int, val cols : int) : [[int]];

function print_int_array(val arr : [int], val size : int) : void;

function print_int(val n : int) : void;

function matrixProduct(val m1 : [[int]], val m2 : [[int]]) : [[int]]{
    val res : [[int]] := get_array2d(m1_rows, m2_cols);
    var m1RowIdx : int := 0;
    while  m1RowIdx < m1_rows {
        var m2ColIdx : int := 0;
        while m2ColIdx<m2_rows{
            var m2RowIdx : int := 0;
            while m2RowIdx<m2_rows {
                res[m1RowIdx][m2ColIdx] := res[m1RowIdx][m2ColIdx] + m1[m1RowIdx][m2RowIdx]*m2[m2RowIdx][m2ColIdx];
                m2RowIdx := m2RowIdx + 1;
            }
            m2ColIdx := m2ColIdx + 1;
        }
        m1RowIdx := m1RowIdx + 1;
    }
    matrixProduct := res;
}


function print_matrix(val m : [[int]], val rows : int, val cols : int) : void {
    var i : int := 0;
    while i < rows{
        print_int_array(m[i], cols);
        i := i + 1;
    }
}


function main() : void {
    val m1 : [[int]] := get_array2d(m1_rows, m1_cols);
    val m2 : [[int]] := get_array2d(m2_rows, m2_cols);

    m1[0][0] := 1;
    m1[0][1] := 2;
    m1[1][0] := 3;
    m1[1][1] := 4;
    m1[2][0] := 5;
    m1[2][1] := 6;

    m2[0][0] := 1;
    m2[0][1] := 2;
    m2[1][0] := 3;
    m2[1][1] := 4;

    
    print_matrix(matrixProduct(m1, m2), m1_rows, m2_cols);

    print_int(get_array2d(2, 2)[0][0]);

    val x : int := 5;
    x := x + 1;
}
'''
tokens = tokenize(source_code)
for token in tokens:
    print(token)

ast = parse(tokens)

# type check the ast
context = Context()
context.enter_function_def_scope()
context.set_type_function_def("printf", "void")
typed_ast = verify(ast, context)

emitter = Emitter()
emitter.function_declarations.append("declare double @pow(ptr noundef, ...)\n")
llvm_code = compile(typed_ast, emitter)

for line in llvm_code:
    print(line)

# write to llvm file
with open('output.ll', 'w') as f:
    for line in llvm_code:
        f.write(line + '\n')