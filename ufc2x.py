from array import array
import memory

MIR = 0
MPC = 0

MAR = 0
MDR = 0
PC  = 0
MBR = 0
X   = 0
Y   = 0
H   = 0

N   = 0
Z   = 1

BUS_A = 0
BUS_B = 0
BUS_C = 0

firmware = array('L', [0]) * 512

#main
firmware[0] = 0b000000000100001101010010000001001000 
            #PC <- PC + 1; MBR <- read_byte(PC); GOTO MBR;

#X = X + mem[address]
firmware[2] = 0b000000011000001101010010000001001000 
            #PC <- PC + 1; MBR <- read_byte(PC); GOTO 3
firmware[3] = 0b000000100000000101001000000010010000 
            #MAR <- MBR; read_word; GOTO 4
firmware[4] = 0b000000101000000101000000010000000000 
            #H <- MDR; GOTO 5
firmware[5] = 0b000000000000001111000001000000011000 
            #X <- X + H; GOTO MAIN;

#mem[address] = X
firmware[6] = 0b000000111000001101010010000001001000 
            #PC <- PC + 1; fetch; GOTO 7
firmware[7] = 0b000001000000000101001000000000010000 
            #MAR <- MBR; GOTO 8
firmware[8] = 0b000000000000000101000100000100011000 
            #MDR <- X; write; GOTO MAIN

#goto address
firmware[9]  = 0b000001010000001101010010000001001000 
            #PC <- PC + 1; fetch; GOTO 10
firmware[10] = 0b000000000100000101000010000001010000 
            #PC <- MBR; fetch; GOTO MBR;

#if X = 0 goto address
firmware[11]  = 0b000001100001000101000001000000011000 
            #X <- X; IF ALU = 0 GOTO 268 (100001100) ELSE GOTO 12 (000001100);
firmware[12]  = 0b000000000000001101010010000000001000 
            #PC <- PC + 1; GOTO MAIN;
firmware[268] = 0b100001101000001101010010000001001000 
            #PC <- PC + 1; fetch; GOTO 269
firmware[269] = 0b000000000100000101000010000001010000 
            #PC <- MBR; fetch; GOTO MBR;

#X = X - mem[address]
firmware[13] = 0b000001110000001101010010000001001000 
            #PC <- PC + 1; fetch;
firmware[14] = 0b000001111000000101001000000010010000 
            #MAR <- MBR; read;
firmware[15] = 0b000010000000000101000000010000000000
            #H <- MDR;
firmware[16] = 0b000000000000001111110001000000011000 
            #X <- X - H; GOTO MAIN;

def read_regs(reg_num):
   global BUS_A, BUS_B, H, MDR, PC, MBR, X, Y
   
   BUS_A = H
   
   if reg_num == 0:
      BUS_B = MDR
   elif reg_num == 1:
      BUS_B = PC
   elif reg_num == 2:
      BUS_B = MBR
   elif reg_num == 3:
      BUS_B = X
   elif reg_num == 4:
      BUS_B = Y
   else:
      BUS_B = 0
   
def write_regs(reg_bits):
   global MAR, MDR, PC, X, Y, H, BUS_C
   
   if reg_bits & 0b100000:
      MAR = BUS_C
   if reg_bits & 0b010000:
      MDR = BUS_C
   if reg_bits & 0b001000:
      PC = BUS_C
   if reg_bits & 0b000100:
      X = BUS_C
   if reg_bits & 0b000010:
      Y = BUS_C
   if reg_bits & 0b000001:
      H = BUS_C
      
def alu(control_bits):
   global N, Z, BUS_A, BUS_B, BUS_C

   a = BUS_A
   b = BUS_B
   o = 0
   
   shift_bits = (0b11000000 & control_bits) >> 6
   control_bits = 0b00111111 & control_bits
      
   if control_bits == 0b011000:
      o = a
   elif control_bits == 0b010100:
      o = b
   elif control_bits == 0b011010:
      o = ~a
   elif control_bits == 0b101100:
      o = ~b
   elif control_bits == 0b111100:
      o = a+b
   elif control_bits == 0b111101:
      o = a+b+1
   elif control_bits == 0b111001:
      o = a+1
   elif control_bits == 0b110101:
      o = b+1
   elif control_bits == 0b111111:
      o = b-a
   elif control_bits == 0b110110:
      o = b-1
   elif control_bits == 0b111011:
      o = -a
   elif control_bits == 0b001100:
      o = a & b
   elif control_bits == 0b011100:
      o = a | b
   elif control_bits == 0b010000:
      o = 0
   elif control_bits == 0b110001:
      o = 1
   elif control_bits == 0b110010:
      o = -1   
   
   if o == 0:
      N = 0
      Z = 1
   else:
      N = 1
      Z = 0
      
   if shift_bits == 0b01:
      o = o << 1
   elif shift_bits == 0b10:
      o = o >> 1
   elif shift_bits == 0b11:
      o = o << 8
      
   BUS_C = o
   
def next_instruction(next, jam):
   global MPC, MBR, Z, N
   
   if jam == 0:
      MPC = next
      return
      
   if jam & 0b001:
      next = next | (Z << 8)   
   
   if jam & 0b010:
      next = next | (N << 8)
      
   if jam & 0b100:
      next = next | MBR
      
   MPC = next
   
def memory_io(mem_bits):
   global PC, MBR, MDR, MAR
   
   if mem_bits & 0b001:
      MBR = memory.read_byte(PC)
   
   if mem_bits & 0b010:
      MDR = memory.read_word(MAR)
      
   if mem_bits & 0b100:
      memory.write_word(MAR, MDR)
      
def step():
   global MIR, MPC
   
   MIR = firmware[MPC]
   
   if MIR == 0:
      return False
      
   read_regs(MIR & 0b00000000000000000000000000000111)   
   alu((MIR & 0b00000000000011111111000000000000) >> 12)
   write_regs((MIR & 0b00000000000000000000111111000000) >> 6)
   memory_io((MIR & 0b00000000000000000000000000111000) >> 3)
   next_instruction((MIR & 0b11111111100000000000000000000000) >> 23,
                    (MIR & 0b00000000011100000000000000000000) >> 20)
   
   return True