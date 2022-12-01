import cfg
import dxf
import dev
import tip
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

def units(x, y, dy, angle, xsign, ysign):

  wg, tilt, h = 0.38, 3, 1
  df = elr.update(wg, cfg.radius, angle, cfg.draft)

  sign = xsign * ysign

  x1, y1 = dev.srect(x, y + h * ysign, cfg.dc * 0.5 * xsign, wg)
  x2, y2 = bends(x1, y1, wg, tilt, 0, xsign, ysign)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, 100 * xsign, wg, cfg.wg)
  x4, y4 = bends(x3, y3, cfg.wg, angle - tilt, 0, xsign, ysign)
  x5, y5 = dxf.move(idev, x2, y2, x4, y4, 0, 0, tilt * sign)

  dh = dy - (y5 - y) * ysign - df['dy']
  dl = dh * xsign / np.sin(angle / 180 * np.pi)

  x6, y6 = dev.tilts(x5, y5, dl, angle * sign)
  x7, y7 = x6 + df['dx'] * xsign, y + dy * ysign
  x8, y8 = dev.bends(x7, y7, angle, 0, -xsign, -ysign)

  return x7, y
  
def device(x, y, dy, angle):

  idev = len(cfg.data)

  x1, y1 = units(x, y, dy, angle,  1,  1)
  x1, y1 = units(x, y, dy, angle,  1, -1)
  x1, y1 = units(x, y, dy, angle, -1,  1)
  x1, y1 = units(x, y, dy, angle, -1, -1)

  dxf.move(idev, x, y, x1, y1, x - x1, 0, 0)

  return x + (x - x1) * 2, y

def chip(x, y, lchip):
  
  ch = 50
  y1 = y + ch
  y2 = y - ch
  x2 = x

  idev = len(cfg.data)

  for _ in range(10):
    x1, _ = dev.sline(x2, y1, 50)
    x1, _ = dev.sline(x2, y2, 50)
    x1, _ = device(x1, y, ch, 20)
    x2, _ = dev.sline(x1, y1, 50)
    x2, _ = dev.sline(x1, y2, 50)

  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x7, t1 = tip.fiber(x5, y2, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = 'dc-' + str(round(cfg.dc, 1))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y + ysize

def chips(x, y, arange):

  var = cfg.dc

  for cfg.dc in arange: _, y = chip(x, y, xsize)

  cfg.dc = var

  return x + xsize, y

if __name__ == '__main__':

  # chip(0, 0, xsize)
  chips(0, 0, dev.arange(18, 20, 1))

  dev.saveas(cfg.work + 'coupler')