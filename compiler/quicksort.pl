function get_random_int_array(var n : int) : [int];

function print_int_array(var arr : [int], var arr_size : int) : void;

function swap(var arr : [int], var i : int, var j : int) : void {
    var temp : int := arr[i];
    arr[i] := arr[j];
    arr[j] := temp;
}

function partition(var arr : [int], var low : int, var high : int) : int {
    var pivot : int := arr[high];
    var i : int := low - 1;
    var j : int := low;
    
    while j <= high - 1 {
        if arr[j] < pivot {
            i := i + 1;
            swap(arr, i, j);
        }
        j := j + 1;
    }
    swap(arr, i + 1, high);
    partition := i + 1;
}

function quicksort(var arr : [int], var low : int, var high : int) : void {
    if low < high {
        var part : int := partition(arr, low, high);
        
        quicksort(arr, low, part - 1);
        quicksort(arr, part + 1, high);
    }
}

function main() : void {
    var n : int := 10;
    var arr : [int] := get_random_int_array(n);
    
    print_int_array(arr, n);

    quicksort(arr, 0, n - 1);
    
    print_int_array(arr, n);
}
