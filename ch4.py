import cfg
import dxf
import dev
import pbs
import voa
import qsk
import tip
import tap
import elr
import numpy as np

yqpsk = 1800
xback = 1500
yhigh = 900

def sbend(x, y, angle, dy):

  x1, y1 = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wr)
  x2, y2 = dev.sbend(x1, y1, angle, dy)
  x3, y3 = dev.taper(x2, y2, cfg.ltpr, cfg.wr, cfg.wg)

  return x3, y3

def tapertilt(x, y, length, wstart, wstop):
  
  idev = len(cfg.data)
  x1, y1 = dev.taper(x, y, length, wstart, wstop)
  x2, y2 = dxf.move(idev, x, y, x1, y1, 0, 0, 90)
  
  return x2, y2

def tbend(x, y, dy, xsign):

  ysign = 1 if dy > 0 else -1

  df = elr.update(cfg.wg, cfg.radius, 45)
  dl = np.sqrt(2) * (dy * ysign - df['dx'] - df['dy'])

  a1 = 0 if xsign > 0 else 90
  a2 = 0 if xsign < 0 else 90
  xo = df['dy'] if xsign > 0 else df['dx']
  yo = df['dx'] if xsign > 0 else df['dy']

  x1, y1 = dev.bends(x, y, 45, a1, xsign, ysign)
  x2, y2 = dev.tilts(x1, y1, dl, cfg.wr, 45 * ysign)
  
  x3, y3 = x2 + xo, y2 + yo * ysign
  x4, y4 = dev.bends(x3, y3, 45, a2, xsign, -ysign)

  return x3, y3

def cbend(x, y, dy, xsign):

  ysign = 1 if dy > 0 else -1

  df = elr.update(cfg.wg, cfg.radius, 90)
  dl = dy * ysign - df['dx'] - df['dy']

  x1, y1 = dev.bends(x, y, 90, 0, xsign, ysign)
  x2, y2 = dev.tilts(x1, y1, dl, cfg.wr, 90 * ysign)
  x3, y3 = x2 - df['dx'] * xsign, y2 + df['dy'] * ysign
  x4, y4 = dev.bends(x3, y3, 90, 0, xsign, -ysign)

  return x3, y3

def inbend(x, y, ystart, sign):

  x1, y1 = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wr)
  x1, y1 = tbend(x1, y1, 215 * sign, 1)
  x2, y2 = dev.tilts(x1, y1, yhigh + 50, cfg.wr, 90 * sign)
  x3, y3 = dev.bends(x2, y2, 90, 90, 1, sign)
  x6, y4 = dev.srect(x3, y3, -xback, cfg.wr)
  h = sign * (yqpsk - cfg.ch * 0.5) + ystart - y4
  x5, y5 = cbend(x6, y4, h, -1)
  x7, y7 = dev.taper(x5, y5, cfg.ltpr, cfg.wr, cfg.wg)

  return x7, y7

def outbend(x, y, ystart, sign):

  x1, y1 = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wr)
  x1, y1 = cbend(x1, y1, sign * yhigh, 1)
  x2, y2 = dev.srect(x1, y1, -xback, cfg.wr)
  h = sign * (yqpsk + cfg.ch * 0.5) + ystart - y2
  x3, y3 = cbend(x2, y2, h, -1)
  x7, y7 = dev.taper(x3, y3, cfg.ltpr, cfg.wr, cfg.wg)

  return x7, y7

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

  x3, _, _ = tap.device(x2, y1)
  x3, _ = dev.sline(x2, y2, x3 - x2)

  x4, y3 = sbend(x3, y1, 90,  300)
  x4, y4 = sbend(x3, y2, 90, -300)

  x6, _ = voa.device(x4, y3)
  x6, _ = dev.sline(x4, y4, x6 - x4)

  x8, y5 = sbend(x6, y3, 90, -300)
  x8, y6 = sbend(x6, y4, 90,  300)

  x9, y61, y62 = pbs.device(x8, y5)
  x9, y63, y64 = pbs.device(x8, y6)

  x10, y73 = inbend(x9, y63, y,  1)
  x10, y72 = inbend(x9, y62, y, -1)

  x11, y71 = outbend(x9, y61, y,  1)
  x11, y74 = outbend(x9, y64, y, -1)

  idev = len(cfg.data)

  x12, _ = qsk.device(x, y + yqpsk)
  x12, _ = qsk.device(x, y - yqpsk)

  for i in [-3,-1,1,3]:
    x15, y1 = dev.taper(x12, y + i * ch + yqpsk, cfg.ltpr, cfg.wr, cfg.wg)
    x15, y2 = dev.taper(x12, y + i * ch - yqpsk, cfg.ltpr, cfg.wr, cfg.wg)
    x13, y1 = tip.diode(x15, y1, 0, 1)
    x13, y2 = tip.diode(x15, y2, 0, 1)

  x14, _ = dxf.move(idev, x, 0, x13, 0, lchip - x13 + x, 0, 0)

  dev.sline(x10, y73, x14 - x13 + x - x10)
  dev.sline(x10, y72, x14 - x13 + x - x10)
  dev.sline(x11, y71, x14 - x13 + x - x11)
  dev.sline(x11, y74, x14 - x13 + x - x11)

  print('Optimized ICR', round(x14 - x))

  return x + lchip, y

if __name__ == '__main__':

  chip(0, 0, 4000)

  dev.saveas(cfg.work + '4ch')