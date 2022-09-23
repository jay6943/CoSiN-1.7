import cfg
import dev
import pbs
import voa
import psk
import tip
import tap
import euler as er

yqpsk = 2400

xsize = cfg.size
ysize = 8000

def inbend(x, y, sign):

  h = 300

  dx = er.bends['125_90_' + cfg.draft]['dx']
  dy = er.bends['125_90_' + cfg.draft]['dy']

  x1, y1 = dev.sbend(x, y, sign * h, 45, 0, 2)
  x2, y2 = dev.tline(x1, y1, sign * (yqpsk - (dx + dy) * 0.5 - h))
  x3, y3 = dev.bends(x2, y2, 90, 270, -sign)

  return x3, y3

def outbend(x, y, xstart, sign):

  x1, y1 = dev.sbend(x, y, sign * (yqpsk - cfg.ch), 90, 0, 1)
  x2, y2 = dev.sline(x1, y1, xstart - x1)

  return x2, y2

def fiber_pd(x, y, lchip):

  x1, _, _ = tip.fiber(x, y, lchip * 0.5, -1)
  x2, _, _ = tip.pd(x1, y, lchip * 0.5, 1)

  return x2, y

def chip(x, y, lchip):
  
  ch = cfg.ch * 0.5

  y1 = y + ch
  y2 = y - ch
  
  ltip = tip.ltip + 1500

  x1, _, _ = tip.fiber(x, y1, ltip, -1)
  x1, _, _ = tip.fiber(x, y2, ltip, -1)
  
  x2, y3 = dev.sbend(x1, y1, ch * 4, 90, 0,  1)
  x2, y4 = dev.sbend(x1, y2, ch * 4, 90, 0, -1)

  x3, _ = tap.device(x2, y3, ysize * 0.5 + ch * 5, -1)
  x4, _ = voa.device(x3, y3)
  x4, _ = dev.sline(x2, y4, x4 - x2)

  x5, y5 = dev.sbend(x4, y3, ch * 3, 90, 0, -1)
  x5, y6 = dev.sbend(x4, y4, ch * 3, 90, 0,  1)

  x6, _ = dev.sline(x5, y5, 500)
  x6, _ = dev.sline(x5, y6, 500)

  x7, y61, y62 = pbs.device(x6, y5)
  x7, y63, y64 = pbs.device(x6, y6)

  x8, _ = inbend(x7, y63,  1)
  x8, _ = inbend(x7, y62, -1)

  x9, _ = outbend(x7, y61, x8,  1)
  x9, _ = outbend(x7, y64, x8, -1)

  x10, _ = psk.device(x9, y + yqpsk)
  x10, _ = psk.device(x9, y - yqpsk)

  ltip = lchip - x10 + x

  for i in [-3,-1,1,3]:
    x11, _, _ = tip.pd(x10, y + i * ch + yqpsk, ltip, 1)
    x11, _, _ = tip.pd(x10, y + i * ch - yqpsk, ltip, 1)

  print('ICR chip length =', int(x11 - x))

  return x11, y

def chips(x, y):

  chip(x, y, xsize)

  fiber_pd(x, y + cfg.ch * 3.5 + yqpsk, xsize)
  voa.chips(x, y - cfg.size * 0.5, dev.arange(200, 500, 100))
  pbs.chip(x, y + cfg.ch * 5 + yqpsk, xsize)
  psk.chip(x, y + 4500, xsize)

  dev.sline(x, y + ysize * 0.5, xsize)
  dev.sline(x, y - ysize * 0.5, xsize)

  return x + xsize, y
  
if __name__ == '__main__':

  chip(0, 0, xsize)

  dev.saveas('icr')