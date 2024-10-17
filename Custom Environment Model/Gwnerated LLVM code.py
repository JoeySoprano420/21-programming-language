define i32 @main() {
entry:
  %x = alloca i32
  store i32 10, i32* %x
  %y = alloca i32
  store i32 5, i32* %y
  %eax = alloca i32
  store i32 3, i32* %eax
  %0 = load i32, i32* %eax
  %1 = load i32, i32* %x
  %addtmp = add i32 %0, %1
  store i32 %addtmp, i32* %eax
  ret i32 0
}
