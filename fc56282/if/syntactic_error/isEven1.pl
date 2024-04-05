val value : int := 10;

function isEven(val x:int) : bool {
    if x % 2 == 0 {
        isEven := true
    } else {
        isEven := false;
    }
}

function main(val args:[string]) {
    val result : bool := isEven(value);
    print_bool(result);
}