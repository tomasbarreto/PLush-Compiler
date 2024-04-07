from tokenizer import tokenize

source_code = '''
# This is a comment
val x := 'ola'
var y := 10 # This is a comment
if x > y {
    y := y + 1
} then else { # This is a comment
    y := y - 1
} 
# This is a comment
'''
tokens = tokenize(source_code)
for token in tokens:
    print(token)
