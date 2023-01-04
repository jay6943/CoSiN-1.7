import cfg
import dxf
import dev
import dci
import tip
import numpy as np
import euler as elr

xsize = cfg.size
ysize = 200

def units(x, y, wg, dy, xsign, ysign):

  angle = 20

  df = elr.update(cfg.wg, cfg.radius, angle)

  sign = xsign * ysign

  x1, y1 = x, y + cfg.dc * ysign
  x2, y2 = dci.bends(x1, y1, wg, dci.tilt, 0, xsign, ysign)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, 100 * xsign, wg, cfg.wg)
  x4, y4 = dev.bends(x3, y3, 90 - dci.tilt, 0, xsign, ysign)
  x5, y5 = dxf.move(idev, x2, y2, x4, y4, 0, 0, dci.tilt * sign)

  return x5, y5
  
def device(x, y, wg, ch):

  idev = len(cfg.data)

  x1, y1 = units(x, y, wg, ch, -1, -1)
  x1, y1 = units(x, y, wg, ch,  1, -1)
  x2, y2 = dci.units(x, y, wg, ch,  1,  1)
  x2, y2 = dci.units(x, y, wg, ch, -1,  1)

  dxf.move(idev, x, y, x2, y2, x - x2, -ch, 0)

  return x + (x - x2) * 2, x1 + (x - x2), y1 - ch

def chip(x, y, lchip):
  
  wg = 0.39
  ch = 50
  y1 = y + ch
  y2 = y - ch

  idev = len(cfg.data)
  x1, _ = dci.device(x, y, wg, ch)
  x3, x4, ltip = dev.center(idev, x, x1, lchip)

  x5, t1 = tip.fiber(x3, y1, ltip, -1)
  x5, t1 = tip.fiber(x3, y2, ltip, -1)
  x6, t2 = tip.fiber(x4, y1, ltip, 1)
  x6, t2 = tip.fiber(x4, y2, ltip, 1)

  s = 'tap-' + str(round(cfg.dc, 2))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x4 - x3), round(x6 - x5))

  return x + lchip, y + ysize

def chips(x, y, arange):

  var = cfg.dc

  for cfg.dc in arange: _, y = chip(x, y, xsize)

  cfg.dc = var

  return x + xsize, y

if __name__ == '__main__':

  # chip(0, 0, 3000)

  chips(0, 0, dev.arange(1.16, 1.46, 0.1))

  dev.saveas(cfg.work + 'tap')