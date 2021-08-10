     goto main 
     wb 0        
    
n    ww 39
fib1 ww 0
fib2 ww 1
aux  ww 0
um   ww 1 

fim  let x, fib1
     mov x, n
     halt
main let x, n
     jz x, fim
     let x, fib1
     add x, fib2
     mov x, aux
     let x, fib2
     mov x, fib1
     let x, aux
     mov x, fib2
     let x, n
     sub x, um
     mov x, n
     goto main