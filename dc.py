import cfg
import dxf
import dev
import numpy as np
import euler as elr

xsize = cfg.size
ysize = 200

def bends(x, y, wg, angle, rotate, xsign, ysign):

  core = elr.update(wg, cfg.radius, angle, cfg.draft)
  edge = elr.update(wg, cfg.radius, angle, 'edge')

  x1, y1 = dxf.bends('edge', x, y, edge, rotate, xsign, ysign)
  x1, y1 = dxf.bends('core', x, y, core, rotate, xsign, ysign)

  return x1, y1

def units(x, y, ch, xsign, ysign):

  wg, length, angle, h = 0.38, 19, 3, 1

  sign = xsign * ysign

  x1, y1 = dev.srect(x, y + h * ysign, length * 0.5 * xsign, wg)
  x2, y2 = bends(x1, y1, wg, angle, 0, xsign, ysign)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, 100 * xsign, wg, cfg.wg)
  x4, y4 = bends(x3, y3, cfg.wg, 45 - angle, 0, xsign, ysign)
  x5, y5 = dxf.move(idev, x2, y2, x4, y4, 0, 0, angle * sign)

  idev = len(cfg.data)
  x7, y7 = dev.bends(x5, y5, 45, 0, -xsign, -ysign)
  dy = (y + ch) * ysign - y5
  dl = dy + y7 - y5
  dx = x5 - x7 + dl * sign
  x8, y8 = dxf.move(idev, x5, y5, x7, y7, dx, dy, 0)
  
  dev.tilts(x5, y5, np.sqrt(2) * dl * sign, 45 * sign)

  return x8 + x5 - x7, y8 + y5 - y7
  
def device(x, y, ch):

  x1, y1 = units(x, y, ch,  1,  1)
  x1, y1 = units(x, y, ch,  1, -1)
  x1, y1 = units(x, y, ch, -1,  1)
  x1, y1 = units(x, y, ch, -1, -1)

  return x - x1, y - y1

def chip(x, y, lchip):
  
  idev = len(cfg.data)
  x1, y1 = device(x, y, cfg.ch * 0.5)
  x2, y2 = dxf.move(idev, x, y, x1, y1, x1, 0, 0)

  return x2, y2

def chips(x, y, arange):

  var = cfg.l2x2

  for cfg.l2x2 in arange: _, y = chip(x, y, xsize)

  cfg.l2x2 = var

  return x + xsize, y

if __name__ == '__main__':

  chip(0, 0, xsize)
  # chips(0, 0, dev.arange(49, 53, 1))

  dev.saveas(cfg.work + 'coupler')