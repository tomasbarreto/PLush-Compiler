val value1 : int := 5;
val value2 : int := 10;

function square(val x:int) : int {
    square := x * x;
}

function min (val x:int, val y:int) : int {
    if x < y {
        min := x;
    } else {
        min := y;
    }
}

function minOfSquares(val x:int, val y:int) : int {
    minOfSquares := min(squar(x), square(y)); # Lexical error: 'squar' instead of 'square'
}

function main(val args:[string]) {
    val result : int := minOfSquares(value1, value2);
    print_int(result);
}
