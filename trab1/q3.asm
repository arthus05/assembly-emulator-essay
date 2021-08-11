     goto main 
     wb 0        
    
n     ww 17
um    ww 1
dois  ww 2
true  ww 1
false ww 0
aux   ww 1

primo let x, true
      mov x, n
      halt

nprimo let x, false
       mov x, n
       halt
main let x, n
     jz x, nprimo
     sub x, um
     jz x, nprimo
     mov x, aux

     let x, aux
loop sub x, um
     jz x, primo
     let x, n
     div x, aux
     jz x, nprimo
     let x, aux
     sub x, um
     mov x, aux
     goto loop
