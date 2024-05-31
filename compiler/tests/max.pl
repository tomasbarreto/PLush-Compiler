function print_int(var n : int) : void;

function get_array(var size : int) : [int];

function max(var values : [int]) : int {
    var i : int := 0;
    var maxValue : int := values[0];
    while i < 5 {
        if values[i] > maxValue {
            maxValue := values[i];
        }
        i := i + 1;
    }
    max := maxValue;
}

function main(val args:[string]) : void {
    var values : [int] := get_array(5);
    values[0] := 5;
    values[1] := 10;
    values[2] := 6;
    values[3] := 8;
    values[4] := 7;

    val result : int := max(values);
    print_int(result);
}
