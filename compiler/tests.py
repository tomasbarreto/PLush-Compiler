from tokenizer import tokenize
from plush_parser import parse

source_code = '''
val x : [int] := false && true || false = false;

while true {
    var y : int := kekw()[1][2][3];
}

print("fhgdasfdsa");

if true {
    x := print("Hello, World!")[1];
    print(x);
}

function kekw() : [int] {
    return getArray();
}
'''
tokens = tokenize(source_code)
for token in tokens:
    print(token)

parse(tokens)
