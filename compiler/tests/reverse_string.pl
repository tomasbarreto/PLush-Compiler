function print_char_array(var str : [char], var str_size : int) : void;

function get_char_array(var str : string, var str_size : int) : [char];

function reverse_string(var input : [char], var input_size: int) : [char] {
    var left : int := 0;
    var right : int := input_size - 1;

    while left < right {
        var temp : char := input[left];
        input[left] := input[right];
        input[right] := temp;
        left := left + 1;
        right := right - 1;
    }

    reverse_string := input;
}

function main() : void {
    var str_size : int := 13;
    var str : [char] := get_char_array("Hello, world!", str_size);
    var reversed_str : [char] := reverse_string(str, str_size);
    print_char_array(reversed_str, str_size);
}
