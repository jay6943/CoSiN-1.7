import cfg
import dxf
import dev
import pbs
import voa
import psk
import tip
import tap

yqpsk = 1800
xback = 2000
yhigh = 900

xsize = 5000
ysize = 5000

def inbend(x, y, ystart, sign):

  x1, y1 = dev.sbend(x, y, 250, 45, 0, sign * 2)
  x2, y2 = dev.tline(x1, y1, sign * yhigh)
  x3, y3 = dev.bends(x2, y2, 90, 90, sign)
  x4, y4 = dev.sline(x3, y3, -xback)
  h = sign * (yqpsk - cfg.ch * 0.5) + ystart - y4
  x5, y5 = dev.sbend(x4, y4, h, 90, 180, -2)

  return x5, y5

def outbend(x, y, ystart, sign):

  x1, y1 = dev.sbend(x, y, sign * yhigh, 90, 0, 2)
  x2, y2 = dev.sline(x1, y1, -xback)
  h = sign * (yqpsk + cfg.ch * 0.5) + ystart - y2
  x3, y3 = dev.sbend(x2, y2, h, 90, 180, -2)

  return x3, y3

def fiber_pd(x, y, lchip):

  x1, _, _ = tip.fiber(x, y, lchip * 0.5, -1)
  x2, _, _ = tip.pd(x1, y, lchip * 0.5, 1)

  return x2, y

def chip(x, y, lchip):
  
  ch, ltip = cfg.ch * 0.5, 2000

  x1 = x + ltip
  y1 = y + ch
  y2 = y - ch
  
  tip.fiber(x1, y1, 0, -1)
  tip.fiber(x1, y2, 0, -1)
  
  x2, y3 = dev.sbend(x1, y1, 300, 90, 0,  1)
  x2, y4 = dev.sbend(x1, y2, 300, 90, 0, -1)

  x4, _ = voa.device(x2, y3)
  x4, _ = dev.sline(x2, y4, x4 - x2)

  x6, y5 = dev.sbend(x4, y3, 300, 90, 0, -1)
  x6, y6 = dev.sbend(x4, y4, 300, 90, 0,  1)

  x7, y61, y62 = pbs.device(x6, y5)
  x7, y63, y64 = pbs.device(x6, y6)

  x8, y73 = inbend(x7, y63, y,  1)
  x8, y72 = inbend(x7, y62, y, -1)

  x9, y71 = outbend(x7, y61, y,  1)
  x9, y74 = outbend(x7, y64, y, -1)

  idev = len(cfg.data)

  x10, _ = psk.device(x, y + yqpsk)
  x10, _ = psk.device(x, y - yqpsk)

  for i in [-3,-1,1,3]:
    x11, _ = tip.diode(x10, y + i * ch + yqpsk, 0, 1)
    x11, _ = tip.diode(x10, y + i * ch - yqpsk, 0, 1)

  x12, _ = dxf.move(idev, x, 0, x11, 0, lchip - x11 + x, 0, 0)

  dev.sline(x8, y73, x12 - x11 + x - x8)
  dev.sline(x8, y72, x12 - x11 + x - x8)
  dev.sline(x9, y71, x12 - x11 + x - x9)
  dev.sline(x9, y74, x12 - x11 + x - x9)

  print('Optimized ICR', int(x12 - x))

  return x11, y

if __name__ == '__main__':

  chip(0, 0, xsize)

  dev.saveas(cfg.work + 'opt')