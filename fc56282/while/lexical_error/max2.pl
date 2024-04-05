val values : int[] := [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

function max() : int {
    val i : int := 0;
    val maxValue : int := values[0];
    while i < values.length() {
        if values[i] > maxValue {
            maxValue := values[i];
        }
        i := i + 1;
    }
    mx := maxValue; # Lexical error: 'mx' instead of 'max'
}

function main(val args:[string]) {
    val result : int := max();
    print_int(result);
}