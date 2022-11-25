import cfg
import dev
import pbs
import voa
import psk
import tip
import tap

yqpsk = 1800
xback = 1200

xsize = 5000
ysize = 5000

def inbend(x, y, ystart, sign):

  x1, y1 = dev.sbend(x, y, 350, 45, 0, sign * 2)
  x2, y2 = dev.tline(x1, y1, sign * cfg.ch * 3.5)
  x3, y3 = dev.bends(x2, y2, 90, 90, sign)
  x4, y4 = dev.sline(x3, y3, -xback)
  h = sign * (yqpsk - cfg.ch * 0.5) + ystart - y4
  x5, y5 = dev.sbend(x4, y4, h, 90, 180, -2)
  x6, y6 = dev.sline(x5, y5, 100)

  return x6, y6

def outbend(x, y, xstart, ystart, sign):

  x1, y1 = dev.sbend(x, y, sign * cfg.ch * 3, 90, 0, 2)
  x2, y2 = dev.sline(x1, y1, -xback)
  h = sign * (yqpsk + cfg.ch * 0.5) + ystart - y2
  x3, y3 = dev.sbend(x2, y2, h, 90, 180, -2)
  x4, y4 = dev.sline(x3, y3, xstart - x3)

  return x4, y4

def fiber_pd(x, y, lchip):

  x1, _, _ = tip.fiber(x, y, lchip * 0.5, -1)
  x2, _, _ = tip.pd(x1, y, lchip * 0.5, 1)

  return x2, y

def chip(x, y):
  
  ch = cfg.ch * 0.5

  y1 = y + ch
  y2 = y - ch
  
  x1, _, _ = tip.fiber(x, y1, 0, -1)
  x1, _, _ = tip.fiber(x, y2, 0, -1)
  
  x2, y3 = dev.sbend(x1, y1, ch * 2, 90, 0,  1)
  x2, y4 = dev.sbend(x1, y2, ch * 2, 90, 0, -1)

  x4, _ = voa.device(x2, y3)
  x4, _ = dev.sline(x2, y4, x4 - x2)

  x6, y5 = dev.sbend(x4, y3, ch * 1, 45, 0, -1)
  x6, y6 = dev.sbend(x4, y4, ch * 1, 45, 0,  1)

  x7, y61, y62 = pbs.device(x6, y5)
  x7, y63, y64 = pbs.device(x6, y6)

  x8, _ = inbend(x7, y63, y,  1)
  x8, _ = inbend(x7, y62, y, -1)

  x9, _ = outbend(x7, y61, x8, y,  1)
  x9, _ = outbend(x7, y64, x8, y, -1)

  x10, _ = psk.device(x9, y + yqpsk)
  x10, _ = psk.device(x9, y - yqpsk)

  for i in [-3,-1,1,3]:
    x11, _, _ = tip.pd(x10, y + i * ch + yqpsk, xsize - x10 - x, 1)
    x11, _, _ = tip.pd(x10, y + i * ch - yqpsk, xsize - x10 - x, 1)

  print('ICR chip length =', int(x11 - x))

  return x11, y

if __name__ == '__main__':

  chip(0, 0)

  dev.saveas(cfg.work + 'opt')