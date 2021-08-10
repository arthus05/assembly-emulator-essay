import ufc2x as cpu
import sys
import memory as mem
import clock as clk 
import disk

disk.read(str(sys.argv[1]))

print("Antes: ", mem.read_word(1))
print("X: ", cpu.X)

clk.start([cpu])

print("Depois: ", mem.read_word(1))
print("X: ", cpu.X)