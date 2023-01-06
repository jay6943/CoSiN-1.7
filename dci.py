import cfg
import dxf
import dev
import tip
import numpy as np
import euler as elr

wg = 0.41
tilted = 3
radius = 50

xsize = cfg.size
ysize = 200

def bends(x, y, angle, rotate, xsign, ysign):

  core = elr.update(wg, radius, angle)
  edge = elr.update(cfg.eg, radius, angle)
  sio2 = elr.update(cfg.sg, radius, angle)

  x1, y1 = dxf.bends('edge', x, y, edge, rotate, xsign, ysign)
  x1, y1 = dxf.bends('core', x, y, core, rotate, xsign, ysign)
  x1, y1 = dxf.bends('sio2', x, y, sio2, rotate, xsign, ysign)

  return x1, y1

def units(x, y, dy, xsign, ysign):

  angle = 20

  df = elr.update(cfg.wg, cfg.radius, angle)

  sign = xsign * ysign

  x1, y1 = x, y + cfg.spacing * ysign
  x2, y2 = bends(x1, y1, tilted, 0, xsign, ysign)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, 100 * xsign, wg, cfg.wg)
  x4, y4 = dev.bends(x3, y3, angle - tilted, 0, xsign, ysign)
  x5, y5 = dxf.move(idev, x2, y2, x4, y4, 0, 0, tilted * sign)

  dh = dy - (y5 - y) * ysign - df['dy']
  dl = dh * xsign / np.sin(angle / 180 * np.pi)

  x6, y6 = dev.tilts(x5, y5, dl, angle * sign)
  x7, y7 = x6 + df['dx'] * xsign, y + dy * ysign
  x8, y8 = dev.bends(x7, y7, angle, 0, -xsign, -ysign)

  return x7, y
  
def device(x, y, ch):

  idev = len(cfg.data)

  x1, y1 = units(x, y, ch,  1,  1)
  x1, y1 = units(x, y, ch,  1, -1)
  x1, y1 = units(x, y, ch, -1,  1)
  x1, y1 = units(x, y, ch, -1, -1)

  dxf.move(idev, x, y, x1, y1, x - x1, 0, 0)

  return x + (x - x1) * 2, y

def chip(x, y, lchip):
  
  ch = 50
  y1 = y + ch
  y2 = y - ch

  idev = len(cfg.data)
  x1, _ = device(x, y, ch)
  x3, x4, ltip = dev.center(idev, x, x1, lchip)

  x5, t1 = tip.fiber(x3, y1, ltip, -1)
  x5, t1 = tip.fiber(x3, y2, ltip, -1)
  x6, t2 = tip.fiber(x4, y1, ltip, 1)
  x6, t2 = tip.fiber(x4, y2, ltip, 1)

  s = 'dc-' + str(round(cfg.spacing, 2))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x4 - x3), round(x6 - x5))

  return x + lchip, y + ysize

def chips(x, y, arange):

  var = cfg.spacing
  for cfg.spacing in arange: _, y = chip(x, y, xsize)
  cfg.spacing = var

  return x + xsize, y

if __name__ == '__main__':

  # chip(0, 0, xsize)

  chips(0, 0, dev.arange(0.87, 0.91, 0.01))

  dev.saveas(cfg.work + 'dci')