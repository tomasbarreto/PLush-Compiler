function print_int(var n : int) : void;

function factorial(var n : int) : int {
    if n = 0 {
        factorial := 1;
    } else {
        factorial := n * factorial(n - 1);
    }
}

function main() : void {
    var n : int := 5;
    var result : int := factorial(n);
    print_int(result);
}