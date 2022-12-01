import cfg
import dxf
import dev
import tip
import numpy as np
import euler as elr

spacing = 1
radius = 50
tilt = 3

xsize = cfg.size
ysize = 200

def bends(x, y, wg, angle, rotate, xsign, ysign):

  core = elr.update(wg, radius, angle, cfg.draft)
  edge = elr.update(wg, radius, angle, 'edge')

  x1, y1 = dxf.bends('edge', x, y, edge, rotate, xsign, ysign)
  x1, y1 = dxf.bends('core', x, y, core, rotate, xsign, ysign)

  return x1, y1

def sbend(x, y, wg, dy, angle):

  core = elr.update(wg, radius, angle, cfg.draft)
  edge = elr.update(wg, radius, angle, 'edge')

  x1, y1 = dxf.sbend('edge', x, y, edge, dy, angle)
  x1, y1 = dxf.sbend('core', x, y, core, dy, angle)

  return x1, y1

def arms(x, y, wg, ch, sign):

  x1, y1 = dev.srect(x, y + spacing * sign, cfg.dc, wg)
  x2, y2 = sbend(x1, y1, wg,  ch * sign, tilt)
  x3, y3 = dev.sline(x2, y2, 100)
  x4, y4 = sbend(x3, y3, wg, -ch * sign, tilt)
  x5, y5 = dev.srect(x4, y4, cfg.dc, wg)

  return x5, y5

def polarizer(x, y, wg, ch):

  x1, y1 = arms(x, y, wg, ch,  1)
  x1, y2 = arms(x, y, wg, ch, -1)

  x2, y3 = sbend(x1, y1, wg,  ch * 2, tilt)
  x2, y4 = sbend(x1, y2, wg, -ch * 2, tilt)

  x3, y1 = arms(x2, y3 + spacing, wg, ch,  1)
  x3, y2 = arms(x2, y3 + spacing, wg, ch, -1)

  x3, y3 = arms(x2, y4 - spacing, wg, ch,  1)
  x3, y4 = arms(x2, y4 - spacing, wg, ch, -1)

  x4, _ = bends(x2, y1, wg, tilt, 0, -1,  1)
  x4, _ = bends(x2, y4, wg, tilt, 0, -1, -1)

  x5, _ = bends(x3, y2, wg, tilt, 0, 1, -1)
  x5, _ = bends(x3, y4, wg, tilt, 0, 1, -1)

  x6, y1 = sbend(x3, y1, wg, 1, tilt)
  x6, y3 = sbend(x3, y3, wg, 1, tilt)

  x7, _ = sbend(x6, y1, wg, -2, tilt)
  x7, _ = sbend(x6, y3, wg, -2, tilt)

  return x7, y

def units(x, y, wg, dy, angle, xsign, ysign):
  
  df = elr.update(wg, cfg.radius, angle, cfg.draft)

  sign = xsign * ysign

  x1, y1 = x, y + spacing * ysign
  x2, y2 = bends(x1, y1, wg, tilt, 0, xsign, ysign)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, 100 * xsign, wg, cfg.wg)
  x4, y4 = dev.bends(x3, y3, angle - tilt, 0, xsign, ysign)
  x5, y5 = dxf.move(idev, x2, y2, x4, y4, 0, 0, tilt * sign)

  dh = dy - (y5 - y) * ysign - df['dy']
  dl = dh * xsign / np.sin(angle / 180 * np.pi)

  x6, y6 = dev.tilts(x5, y5, dl, angle * sign)
  x7, y7 = x6 + df['dx'] * xsign, y + dy * ysign
  x8, y8 = dev.bends(x7, y7, angle, 0, -xsign, -ysign)

  return x7, y
  
def device(x, y, dy, angle):

  ch = 2
  dh = ch + 3
  wg = 0.38

  idev = len(cfg.data)

  x1, _ = units(x, y, wg, dy, angle, -1,  1)
  x1, _ = units(x, y, wg, dy, angle, -1, -1)
  x2, _ = polarizer(x, y, wg, ch)
  x1, _ = units(x2, y + dh, wg, dy - dh, angle,  1,  1)
  x1, _ = units(x2, y - dh, wg, dy - dh, angle,  1, -1)

  dxf.move(idev, x, y, x1, y, x1 - x2, 0, 0)

  return x + (x1 - x) * 2 - (x2 - x), y

def chip(x, y, lchip):
  
  ch = 50
  y1 = y + ch
  y2 = y - ch
  x2 = x

  idev = len(cfg.data)

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

  device(0, 0, 50, 20)

  # chip(0, 0, 3000)
  # chips(0, 0, dev.arange(18, 20, 1))

  dev.saveas(cfg.work + 'polarizer')