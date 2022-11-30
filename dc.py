import cfg
import dxf
import dev
import numpy as np
import euler as elr

xsize = cfg.size
ysize = 200

def curve(wg, radius, angle):

  m = 100 if cfg.draft != 'mask' else 1000

  df = elr.curve(wg, radius, angle, m)
  ef = elr.curve(cfg.eg, radius, angle, 100)

  return df, ef

def bend(layer, x, y, df, angle, xsign, ysign):

  xa, ya = df['x'], df['y']
  xa, ya = xa * xsign + x, ya * ysign + y

  xb, yb = df['xo'] - df['x'], df['y'] - df['yo']
  xb, yb = dxf.rotate(xb, yb, angle)
  xb, yb = xb + df['xo'], yb + df['yo']
  xb, yb = xb * xsign + x, yb * ysign + y

  x1 = (xb[0] + xb[df['n'] * 2 - 1]) * 0.5
  y1 = (yb[0] + yb[df['n'] * 2 - 1]) * 0.5

  data = np.array([xa, ya]).transpose()
  cfg.data.append([layer] + data.tolist())

  data = np.array([xb, yb]).transpose()
  cfg.data.append([layer] + data.tolist())

  return x1, y1

def bends(x, y, df, ef, angle, xsign, ysign):

  x1, y1 = bend('core', x, y, df, angle, xsign, ysign)
  x1, y1 = bend('edge', x, y, ef, angle, xsign, ysign)

  return x1, y1

def units(x, y, ch, xsign, ysign):

  wg, length, angle, h = 0.38, 19, 3, 1

  cf, cfe = curve(wg, cfg.radius, angle)
  df, dfe = curve(cfg.wg, cfg.radius, 45 - angle)
  rf, rfe = curve(cfg.wg, cfg.radius, 45)

  sign = xsign * ysign

  x1, y1 = dev.srect(x, y + h * ysign, length * 0.5 * xsign, wg)
  x2, y2 = bends(x1, y1, cf, cfe, angle, xsign, ysign)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, 100 * xsign, wg, cfg.wg)
  x4, y4 = bends(x3, y3, df, dfe, 45 - angle, xsign, ysign)
  x5, y5 = dxf.move(idev, x2, y2, x4, y4, 0, 0, angle * sign)

  idev = len(cfg.data)
  x7, y7 = bends(x5, y5, rf, rfe, 45, -xsign, -ysign)
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