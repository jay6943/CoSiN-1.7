import cfg
import dxf
import dev
import dci
import elr
import tip
import numpy as np

xsize = cfg.size
ysize = 200

def bends(x, y, rotate, xsign, ysign):

  core = elr.update(dci.wg, dci.radius, dci.tilted)
  sio2 = elr.update(cfg.sg, dci.radius, dci.tilted)

  x1, y1 = dxf.bends('core', x, y, core, rotate, xsign, ysign)
  x1, y1 = dxf.bends('sio2', x, y, sio2, rotate, xsign, ysign)

  return x1, y1

def sbend(x, y, dy):

  core = elr.update(dci.wg, dci.radius, dci.tilted)
  sio2 = elr.update(cfg.sg, dci.radius, dci.tilted)

  x1, y1 = dxf.sbend('core', x, y, core, dci.tilted, dy)
  x1, y1 = dxf.sbend('sio2', x, y, sio2, dci.tilted, dy)

  return x1, y1

def arm(x, y, ch, sign):

  wdc, ltaper = 0.6, 5

  x1, y1 = sbend(x, y + cfg.spacing * sign, ch * sign)
  x2, y2 = dxf.taper('core', x1, y1, ltaper, dci.wg, wdc)
  if sign > 0: x2, y2 = dxf.srect('core', x2, y2, cfg.lpbs, wdc)
  x3, y3 = dxf.taper('core', x2, y2, ltaper, wdc, dci.wg)
  if sign < 0: x3, y3 = dxf.srect('core', x3, y3, cfg.lpbs, dci.wg)
  x4, y4 = sbend(x3, y3, -ch * sign)

  return x4, y4

def mzi(x, y, ch, sign):

  dh = 1

  x1, y1 = arm(x, y, ch, sign)
  x2, y2 = sbend(x1, y1,  ch * 2 * sign)
  x3, y4 = arm(x2, y2 + cfg.spacing * sign, ch,  1)
  x3, y5 = arm(x2, y2 + cfg.spacing * sign, ch, -1)
  x4, y6 = sbend(x3, y4,  dh)
  x5, y7 = sbend(x3, y5, -dh)

  sbend(x1, y2 + (cfg.spacing * 2 + ch * 2) * sign, -ch * 2 * sign)

  return x4, y6

def device(x, y, dy, angle):

  ch = 1

  x1, y1 = dci.sbend(0, y + dy, angle, dy - dci.offset, -1, -1)
  x1, y2 = dci.sbend(0, y - dy, angle, dy - dci.offset, -1,  1)
  x2, y1 = dci.dc(x1, y, -1,  1)
  x2, y2 = dci.dc(x1, y, -1, -1)
  x3, y1 = mzi(x2, y, ch,  1)
  x3, y2 = mzi(x2, y, ch, -1)
  x4, y1 = dev.taper(x3, y1, 100, 0.4, cfg.wg)
  x4, y2 = dev.taper(x3, y2, 100, 0.4, cfg.wg)
  x5, y3 = dev.sbend(x4, y1, angle, y + dy - y1)
  x6, y4 = dev.sbend(x4, y2, angle, y - dy - y2)
  x6, y3 = dev.sline(x5, y3, x6 - x5)

  dxf.srect('edge', x2, y, x3 - x2, 40)

  return x6, y

def chip(x, y, lchip):
  
  ch = 50
  y1 = y + ch
  y2 = y - ch

  idev = len(cfg.data)
  x1, _ = device(x, y, ch, 20)
  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x7, t1 = tip.fiber(x5, y2, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = 'dc-' + str(round(cfg.spacing, 1))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y + ysize

def chips(x, y, arange):

  var = cfg.spacing
  for cfg.spacing in arange: _, y = chip(x, y, xsize)
  cfg.spacing = var

  return x + xsize, y

if __name__ == '__main__':

  chip(0, 0, 0)

  # chips(0, 0, dev.arange(18, 20, 1))

  dev.saveas(cfg.work + 'pdc')