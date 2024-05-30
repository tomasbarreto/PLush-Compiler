
define dso_local i32 @sum(i32 %prt_1, i32 %prt_2) {
   %sum = alloca i32
   store i32 0, ptr %sum
   %prt_1.addr = alloca i32
   store i32 %prt_1, ptr %prt_1.addr
   %prt_2.addr = alloca i32
   store i32 %prt_2, ptr %prt_2.addr
   %prt_3 = alloca i32
   store i32 2, ptr %prt_3
   %prt_4 = load i32, ptr %prt_3
   store i32 %prt_4, ptr %sum
   %prt_5 = load i32, ptr %sum
   ret i32 %prt_5
}

define dso_local void @main() {
   %prt_6 = alloca i32
   store i32 -1, ptr %prt_6
   %prt_7 = alloca i32
   store i32 5, ptr %prt_7
   %prt_8 = alloca i32
   store i32 0, ptr %prt_8
   ret void
}
declare double @pow(ptr noundef, ...)

