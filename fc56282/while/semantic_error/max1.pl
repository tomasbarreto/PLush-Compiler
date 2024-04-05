val values : int[] := [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

function max() : int {
    val i : int := 0;
    val maxValue : int := 0;  # Incorrect initialization
    while i < 10 {
        if values[i] > maxValue {
            maxValue := values[i];
        }
        i := i + 1;
    }
    max := maxValue; 
}

function main(val args:[string]) {
    val result : int := max();
    print_int(result);
}