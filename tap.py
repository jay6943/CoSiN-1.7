import cfg
import dxf
import dev
import dci
import tip
import numpy as np
import euler as elr

xsize = cfg.size
ysize = 200

def device(x, y, dy, angle, xsign, ysign):

  dh = 2
  df = elr.update(cfg.wg, cfg.radius, angle)

  sign = xsign * ysign

  x1, _ = dev.taper(x, y, 100, cfg.wg, dci.wg)

  idev = len(cfg.data)
  x2, y2 = dci.bends(x1, y + dh * ysign, dci.tilt, 0, -xsign, ysign)
  dxf.move(idev, x1, y, x2, y, x1 - x2, 0, 0)

  dl = x1 - x2

  x3, _ = dev.srect(x1, y, dl * 2, dci.wg)
  x4, _ = dev.taper(x3, y, 100, dci.wg, cfg.wg)

  idev = len(cfg.data)
  x5, y5 = dev.taper(x1, y2, -100 * xsign, dci.wg, cfg.wg)
  x7, y7 = dxf.move(idev, x1, y2, x5, y5, 0, 0, -dci.tilt * sign)

  x2, y2 = dci.bends(x1 + dl, y + dh * ysign, dci.tilt, 0,  xsign, ysign)

  idev = len(cfg.data)
  x5, y5 = dev.taper(x2, y2, 100 * xsign, dci.wg, cfg.wg)
  x6, y6 = dev.bends(x5, y5, angle - dci.tilt, 0, xsign, ysign)
  x7, y7 = dxf.move(idev, x2, y2, x6, y6, 0, 0, dci.tilt * sign)

  if angle < 90:
    dh = dy - (y7 - y) * ysign - df['dy']
    dl = dh * xsign / np.sin(angle / 180 * np.pi)

    x7, y7 = dev.tilts(x7, y7, dl, angle * sign)
    x7, y7 = x7 + df['dx'] * xsign, y + dy * ysign
    dev.bends(x7, y7, angle, 0, -xsign, -ysign)

  dev.sline(x4, y, x7 - x4)

  return x7, y7
  
def chip(x, y, lchip):
  
  ch = 50
  y1 = y + ch
  y2 = y - ch

  idev = len(cfg.data)
  x2, _ = device(x, y1, 100, 20, 1, -1)
  x5, x6, ltip = dev.center(idev, x, x2, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = 'tap-' + str(round(cfg.dc, 2))
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

  chip(0, 0, 3000)

  # chips(0, 0, dev.arange(1.1, 1.3, 0.1))

  dev.saveas(cfg.work + 'tap')