     goto main 
     wb 0        
    
n     ww 1     
count     ww 0
um       ww 1

fim  let x, count
     sub x, um
     mov x, n
     halt
main let x, n
     jz x, fim
     desl x, n
     mov x, n
     let x, count
     add x, um
     mov x, count
     goto main