     goto main 
     wb 0        
    
n    ww 10
um   ww 1
aux  ww 1

fim  let x, aux
     mov x, n
     halt
main let x, n
     jz x, fim
     let x, aux
     mult x, n
     mov x, aux
     let x, n
     sub x, um
     mov x, n
     goto main
     