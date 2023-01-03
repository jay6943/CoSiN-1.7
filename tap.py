import cfg
import dxf
import dev
import dci
import tip
import numpy as np
import euler as elr

xsize = cfg.size
ysize = 200

# def device(x, y, dy, angle, xsign, ysign):

#   dh = 2
#   df = elr.update(cfg.wg, cfg.radius, angle)

#   sign = xsign * ysign

#   x1, _ = dev.taper(x, y, 100, cfg.wg, 0.39)

#   idev = len(cfg.data)
#   x2, y2 = dci.bends(x1, y + dh * ysign, dci.tilt, 0, -xsign, ysign)
#   dxf.move(idev, x1, y, x2, y, x1 - x2, 0, 0)

#   dl = x1 - x2

#   x3, _ = dev.srect(x1, y, dl * 2, 0.39)
#   x4, _ = dev.taper(x3, y, 100, 0.39, cfg.wg)

#   idev = len(cfg.data)
#   x5, y5 = dev.taper(x1, y2, -100 * xsign, 0.39, cfg.wg)
#   x7, y7 = dxf.move(idev, x1, y2, x5, y5, 0, 0, -dci.tilt * sign)

#   x2, y2 = dci.bends(x1 + dl, y + dh * ysign, dci.tilt, 0,  xsign, ysign)

#   idev = len(cfg.data)
#   x5, y5 = dev.taper(x2, y2, 100 * xsign, 0.39, cfg.wg)
#   x6, y6 = dev.bends(x5, y5, angle - dci.tilt, 0, xsign, ysign)
#   x7, y7 = dxf.move(idev, x2, y2, x6, y6, 0, 0, dci.tilt * sign)

#   if angle < 90:
#     dh = dy - (y7 - y) * ysign - df['dy']
#     dl = dh * xsign / np.sin(angle / 180 * np.pi)

#     x7, y7 = dev.tilts(x7, y7, dl, angle * sign)
#     x7, y7 = x7 + df['dx'] * xsign, y + dy * ysign
#     dev.bends(x7, y7, angle, 0, -xsign, -ysign)

#   dev.sline(x4, y, x7 - x4)

#   return x7, y7
  
def device(x, y, wg, ch):

  idev = len(cfg.data)

  x1, y1 = dci.units(x, y, wg, ch,  1,  1)
  x1, y1 = dci.units(x, y, wg, ch,  1, -1)
  x1, y1 = dci.units(x, y, wg, ch, -1,  1)
  x1, y1 = dci.units(x, y, wg, ch, -1, -1)

  dxf.move(idev, x, y, x1, y1, x - x1, 0, 0)

  return x + (x - x1) * 2, y

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

  s = 'dc-' + str(round(cfg.dc, 2))
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