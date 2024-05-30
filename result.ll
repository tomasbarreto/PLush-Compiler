
define dso_local void @main() {
entry:
   %prt_1 = alloca i32
   store i32 10, ptr %prt_1
   br i1 %['\ndefine dso_local void @main() {', 'entry:', '   %prt_1 = alloca i32', '   store i32 10, ptr %prt_1', '\ndeclare void @print_int(ptr, ...) #1\n'], label %if_1.then, label %if_1.else
if_1.then:
   store i32 5, ptr %prt_1
   %prt_2 = load i32, ptr %prt_1
   %cmp_1 = icmp eq i32 %prt_2, 5
   br i1 %cmp_1, label %if_2.then, label %if_2.else
if_2.then:
   call void @print_int(i32 1)
   br label %if_2.end
if_2.else:
   call void @print_int(i32 2)
   br label %if_2.end
if_2.end:
   br label %if_1.end
if_1.else:
   call void @print_int(i32 0)
   br label %if_1.end
if_1.end:
   ret void
}

declare void @print_int(ptr, ...) #1

