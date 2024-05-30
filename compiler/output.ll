
define dso_local i32 @factorial(i32 %prt_1) {
   %factorial = alloca i32
   store i32 0, ptr %factorial
   %prt_1.addr = alloca i32
   store i32 %prt_1, ptr %prt_1.addr
   %prt_2 = load i32, ptr %prt_1.addr
   %cmp_1 = icmp eq i32 %prt_2, 0
   br i1 %cmp_1, label %if_1.then, label %if_1.else
if_1.then:
   store i32 1, ptr %factorial
   br label %if_1.end
if_1.else:
   %prt_3 = load i32, ptr %prt_1.addr
   %prt_4 = load i32, ptr %prt_1.addr
   %add_1 = sub nsw i32 %prt_4, 1
   %prt_5 = call i32 @factorial(i32 %add_1)
   %mult_1 = mul nsw i32 %prt_3, %prt_5
   store i32 %mult_1, ptr %factorial
   br label %if_1.end
if_1.end:
   %prt_6 = load i32, ptr %factorial
   ret i32 %prt_6
}

define dso_local void @main() {
   %prt_7 = alloca i32
   store i32 5, ptr %prt_7
   %prt_9 = load i32, ptr %prt_7
   %prt_10 = call i32 @factorial(i32 %prt_9)
   %prt_8 = alloca i32
   store i32 %prt_10, ptr %prt_8
   %prt_11 = load i32, ptr %prt_8
   call void @print_int(i32 %prt_11)
   ret void
}
declare double @pow(ptr noundef, ...)


declare void @print_int(ptr, ...) #1

