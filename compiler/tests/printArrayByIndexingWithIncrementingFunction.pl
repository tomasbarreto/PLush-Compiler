function print_int(var n : int) : void;

function print_int_array(var n : [int], var dim : int) : void;

function get_random_int_array(var size : int) : [int];

function print_string(var a : string) : void;

function increment(var i : int) : int {
    increment := i + 1;
}

var ola : string := "ola\n\nkekw";

function main() : void {
    var n : int := 5;
    var arr : [int] := get_random_int_array(n);

    print_string("Original array:\n");
    print_int_array(arr, n);

    print_string("Print array with incrementing function\n");

    var i : int := -1;

    while i + 1 < n {
        print_int(arr[increment(i)]);
        i := increment(i);
    }
    print_string(ola);
}