### Instruções

Para rodar as questões, exemplo:
```
python3 assembler.py questoes/q1.asm q1.asm

python3 computador_disco.py q1.asm
```

## Mudanças

### Assembler
Comandos adicionados:
- let: coloca o valor na memória em um registrador
- desl: desloca o valor de X para a direita e atribui em X
- mult: multiplica o valor de X pelo valor na memoria e atribui em X
- div: atribui em X o resto da divisão de X pelo valor na memória

### ULA
Apenas adiciona um shift de bits para deslocar todos os bits, exceto o bit de sinal. Utilizado na operação `div`
```
  elif shift_bits == 0b11:
    o = o >> 31
```