val value : int := 10;

function print_boolean(val x:boolean) : void;

function isEven(val x:int) : boolean {
    if x % 2 = 0 {
        isEven := true;
    } else {
        isEven := false;
    }
}

function main(val args:[string]) : void {
    val result : boolean := isEven(value);
    print_boolean(result);
}
