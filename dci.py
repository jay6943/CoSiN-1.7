import cfg
import dxf
import dev
import tip
import elr
import numpy as np

wg = 0.41
tilted = 3
radius = 50
ltaper = 100
ybends = elr.update(wg, radius, tilted)
offset = ltaper * np.sin(tilted * np.pi / 180) + cfg.spacing + ybends['dy']

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

def rbend(x, y, angle, dy, xsign, ysign):

  df = elr.update(cfg.wg, cfg.radius, angle)

  sign = xsign * ysign

  idev = len(cfg.data)
  x1, y1 = dev.bends(x, y, angle - tilted, 0, xsign, ysign)
  x2, y2 = dxf.move(idev, x, y, x1, y1, 0, 0, tilted * sign)

  dh = dy - (y2 - y) * ysign - df['dy']
  dl = dh * xsign / np.sin(angle / 180 * np.pi)

  x3, y3 = dev.tilts(x2, y2, dl, angle * sign)
  x4, y3 = x3 + df['dx'] * xsign, y + dy * ysign
  x3, y4 = dev.bends(x4, y3, angle, 0, -xsign, -ysign)

  return x4, y4

def sbend(x, y, angle, dy, xsign, ysign):

  if xsign > 0: x2, y2 = rbend(x, y, angle, dy, xsign, ysign)
  else:
    idev = len(cfg.data)
    x1, y1 = rbend(x, y + dy * ysign, angle, dy, xsign, -ysign)
    x2, y2 = dxf.move(idev, x, y, x1, y1, x - x1, 0, 0)
    x2 = x2 + x - x1

  return x2, y2

def arm(x, y, xsign, ysign):

  sign = xsign * ysign

  x1, y1 = x, y + cfg.spacing * ysign
  x2, y2 = bends(x1, y1, tilted, 0, xsign, ysign)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, ltaper * xsign, wg, cfg.wg)
  x4, y4 = dxf.move(idev, x2, y2, x3, y3, 0, 0, tilted * sign)

  return x4, y4

def dc(x, y, xsign, ysign):

  if xsign > 0:
    x1, y1 = x, y
    x4, y4 = arm(x, y, xsign, ysign)
  else:
    idev = len(cfg.data)
    x1, y1 = arm(x, y, xsign, ysign)
    x4, y4 = dxf.move(idev, x, y, x1, y1, x - x1, 0, 0)

  return x4 + x - x1, y4

def device(x, y):

  x1, y1 = dc(x, y, -1,  1)
  x1, y2 = dc(x, y, -1, -1)
  x2, y1 = dc(x1, y, 1,  1)
  x2, y2 = dc(x1, y, 1, -1)

  return x2, y1, y2

def chip(x, y, lchip):
  
  ch = 50
  y1 = y + ch
  y2 = y - ch

  idev = len(cfg.data)

  x1, _ = sbend(x, y1, 20, ch - offset, -1, -1)
  x1, _ = sbend(x, y2, 20, ch - offset, -1,  1)
  x1, y3, y4 = device(x1, y)
  x2, _ = sbend(x1, y3, 20, ch - offset, 1,  1)
  x2, _ = sbend(x1, y4, 20, ch - offset, 1, -1)

  x3, x4, ltip = dev.center(idev, x, x2, lchip)

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

  chip(0, 0, 2000)

  # chips(0, 0, dev.arange(0.87, 0.91, 0.01))

  dev.saveas(cfg.work + 'dci')