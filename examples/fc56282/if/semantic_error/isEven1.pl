val value : int := 10;

function isEven(val x:int) : bool {
    if x % 2 == 0 {
        isEven := true;
    } else {
        isEven := x;  # Semantic error: returning an int instead of a bool
    }
}

function main(val args:[string]) {
    val result : bool := isEven(value);
    print_bool(result);
}