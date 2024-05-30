function print_int(var n : {int | n > 0}) : void;

function print(var n : {int | n > 0}) : void;

function print(var n : {int | n > 0}) : void {
    print_int(n);
}

function sum(var a : {int | a >= 0}, var b : {int | b >= 0}) : {int | sum >= 0} {
    var result : {int | result >= 0} := 2;

    sum := result;
}

function main() : void {
    var n1 : {int | n1 >= -1} := 0;

    var n5 : {int | n5 >= 5} := 5;

    var n4 : {int | n4 >= 0} := 1 + -1;

    print(n4);
}

