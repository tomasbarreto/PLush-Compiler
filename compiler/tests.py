from plush_tokenizer import tokenize
from plush_parser import parse
from plush_typechecker import verify
from plush_compiler import compile
from context import Context
from emitter import Emitter

source_code = '''
function print_float(var x : float) : void;

var a : string := "hello";

function print_int(var x : int) : void;

function add(var x : int, var y : int) : int {
    add := x + y;
}

function get_array(var nr_positios : int) : [int];

function get_array2d(var nr_positios : int, var nr_positios2 : int) : [[int]];

function print_string(var x : string) : void;

function concat_strings(var x : string, var y : string) : string;

function get_array2d_char(var nr_positions : int) : [char];

function print_char(var a : char) : void;

function main() : void {

    var o : float := 2.0;
    var new : float := 1.0 / o;

    print_float(new);

    var a : [int] := get_array(10);
    var b : [[int]] := get_array2d(10, 10);

    var i : int := 0;
    while i < 10 {
        var xdd : int := a[i] + 1;
        print_int(xdd);
        i := i + 1;
    }

    var fdsa : int := a[0];
    print_int(fdsa);

    print_int(get_array(15)[14]);

    i := 0;
    var j : int := 0;

    while i < 10 {
        while j < 10 {
            var xdd : int := b[i][j];
            print_int(xdd);
            j := j + 1;
        }
        i := i + 1;
    }

    var x : int := add(1, 2);
    printf("x: %d\n", x);
    var t : float := 3.139999999999;
    print_float(t);

    t := 3.1 + 3.1;
    print_float(t);

    a[1] := 100;

    print_int(a[1]);

    print_string("hello kekw\nCARECA");

    var new_string : string := "teste";
    var new_string2 : string := "this is a test";
    var new_string3 : string := concat_strings(new_string, new_string2);

    print_string(new_string3);

    var isA : boolean := false;
    var isB : boolean := true;
    var isC : boolean := true;

    if isC && isB && isA {
        x := x + 1;
        print_int(x);
        if isA || isB {
            x := x + 1;
            print_int(x);
        }
        else {
            x := x - 1;
            print_int(x);
        }

        while x < 10 {
            x := x + 1;
            var z : int := 3;
            while z > 0 {
                z := z - 1;
                if z > -1 {
                    print_int(x);
                }
            }
        }
    }
    else {
        x := x - 1;
        print_int(x);
    }

    var z : int := 0;
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
emitter.function_declarations.append("declare i32 @printf(ptr noundef, ...)\n")
llvm_code = compile(typed_ast, emitter)

for line in llvm_code:
    print(line)

# write to llvm file
with open('output.ll', 'w') as f:
    for line in llvm_code:
        f.write(line + '\n')