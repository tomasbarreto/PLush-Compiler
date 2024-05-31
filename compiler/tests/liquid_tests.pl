function get_5(var n : {int | n = 0}) : {int | get_5 = 5} {
    get_5 := 5;
}

function print_int(var n : {int | n > 0}) : void;

function print(var n : {int | n > 0}) : void;

function print(var n : {int | n = 0}) : void {
    var five : {int | five = 5 } := get_5(n);
    print_int(five);
}

function main() : void {
    var n1 : {int | n1 >= 10} := 12;

    var n2 : {int | n2 >= 11} := n1;

    var n3 : {int | n3 >= 12} := n2;

    var result : {int | result >= 24} := n1 + n2;

    print(0);
}

