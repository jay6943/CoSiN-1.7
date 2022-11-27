import cfg
import dxf
import dev
import pbs
import voa
import psk
import tip
import tap

xsize = 4000
ysize = 5000

yqpsk = 1800
xback = 1500
yhigh = 900

def inbend(x, y, ystart, sign):

  x1, y1 = dev.sbend(x, y, 250, 45, 0, sign * 2)
  x2, y2 = dev.tline(x1, y1, sign * yhigh)
  x3, y3 = dev.bends(x2, y2, 90, 90, sign)
  x6, y4 = dev.sline(x3, y3, -xback)
  h = sign * (yqpsk - cfg.ch * 0.5) + ystart - y4
  x5, y5 = dev.sbend(x6, y4, h, 90, 180, -2)

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
  
  ch = cfg.ch * 0.5

  y1 = y + ch
  y2 = y - ch
  
  idev = len(cfg.data)
  x1, _ = tip.fiber(x, y1, 0, -1)
  x1, _ = tip.fiber(x, y2, 0, -1)
  dxf.move(idev, x, 0, x1, 0, x - x1, 0, 0)
  
  x2 = x * 2 - x1

  x3, _ = tap.device(x2, y1, 4, 100, 300, yqpsk)
  x3, _ = dev.sline(x2, y2, x3 - x2)

  x4, y3 = dev.sbend(x3, y1, 300, 90, 0,  1)
  x4, y4 = dev.sbend(x3, y2, 300, 90, 0, -1)

  x6, _ = voa.device(x4, y3)
  x6, _ = dev.sline(x4, y4, x6 - x4)

  x8, y5 = dev.sbend(x6, y3, 300, 90, 0, -1)
  x8, y6 = dev.sbend(x6, y4, 300, 90, 0,  1)

  x9, y61, y62 = pbs.device(x8, y5)
  x9, y63, y64 = pbs.device(x8, y6)

  x10, y73 = inbend(x9, y63, y,  1)
  x10, y72 = inbend(x9, y62, y, -1)

  x11, y71 = outbend(x9, y61, y,  1)
  x11, y74 = outbend(x9, y64, y, -1)

  idev = len(cfg.data)

  x12, _ = psk.device(x, y + yqpsk)
  x12, _ = psk.device(x, y - yqpsk)

  for i in [-3,-1,1,3]:
    x13, _ = tip.diode(x12, y + i * ch + yqpsk, 0, 1)
    x13, _ = tip.diode(x12, y + i * ch - yqpsk, 0, 1)

  x14, _ = dxf.move(idev, x, 0, x13, 0, lchip - x13 + x, 0, 0)

  dev.sline(x10, y73, x14 - x13 + x - x10)
  dev.sline(x10, y72, x14 - x13 + x - x10)
  dev.sline(x11, y71, x14 - x13 + x - x11)
  dev.sline(x11, y74, x14 - x13 + x - x11)

  print('Optimized ICR', int(x14 - x))

  return x + lchip, y

if __name__ == '__main__':

  chip(0, 0, xsize)

  dev.saveas(cfg.work + 'opt')