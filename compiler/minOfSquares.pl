val value1 : float := 5.0;
val value2 : float := 10.0;

function print_int(val x:int) : void;

function print_float(val x:float) : void;

function square(val x:float) : float {
    square := x ^ 2.0;
}

function min (val x:float, val y:float) : float {
    if x < y {
        min := x;
    } else {
        min := y;
    }
}

function minOfSquares(val x:float, val y:float) : float {
    minOfSquares := min(square(x), square(y));
}

function main(val args:[string]) : void {
    val result : float := minOfSquares(value1, value2);
    print_float(result);

    print_int(10 % 3);
}