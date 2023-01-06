import cfg
import dxf
import dev
import dci
import cir
import tip
import numpy as np
import euler as elr

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

def arms(x, y, ch, sign):

  wdc = 0.6
  ldc = 20

  x1, y1 = dxf.srect('core', x, y + cfg.spacing * sign, cfg.spacing, dci.wg)
  x2, y2 = sbend(x1, y1, ch * sign)
  x3, y3 = dxf.taper('core', x2, y2, 10, dci.wg, wdc)
  if sign > 0: x3, y3 = dxf.srect('core', x3, y3, ldc, wdc)
  x4, y4 = dxf.taper('core', x3, y3, 10, wdc, dci.wg)
  if sign < 0: x4, y4 = dxf.srect('core', x4, y4, ldc, dci.wg)
  x5, y5 = sbend(x4, y4, -ch * sign)
  x6, y6 = dxf.srect('core', x5, y5, cfg.spacing, dci.wg)

  return x6, y6

def ports(x, y, angle, dy, xsign, ysign):
  
  df = elr.update(dci.wg, cfg.radius, angle)
  ef = elr.update(cfg.eg, dci.radius, dci.tilted)

  sign = xsign * ysign

  x1, y1 = x, y + cfg.spacing * ysign
  x2, y2 = dxf.bends('edge', x1, y1, ef, 0, xsign, ysign)
  x2, y2 = bends(x1, y1, 0, xsign, ysign)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, 100 * xsign, dci.wg, cfg.wg)
  x4, y4 = dev.bends(x3, y3, angle - dci.tilted, 0, xsign, ysign)
  x5, y5 = dxf.move(idev, x2, y2, x4, y4, 0, 0, dci.tilted * sign)

  dh = dy - (y5 - y) * ysign - df['dy']
  dl = dh * xsign / np.sin(angle / 180 * np.pi)

  x6, y6 = dev.tilts(x5, y5, dl, angle * sign)
  x7, y7 = x6 + df['dx'] * xsign, y + dy * ysign
  x8, y8 = dev.bends(x7, y7, angle, 0, -xsign, -ysign)
  
  return x7, y
  
def pbs2(x, y, ch, sign):

  dh = 1

  x1, y1 = arms(x, y, ch, sign)
  x2, y2 = sbend(x1, y1,  ch * 2 * sign)
  x3, y4 = arms(x2, y2 + cfg.spacing * sign, ch,  1)
  x3, y5 = arms(x2, y2 + cfg.spacing * sign, ch, -1)
  x4, y6 = sbend(x3, y4,  dh)
  x5, y7 = sbend(x3, y5, -dh)

  x9, y9 = x1, y2 + (cfg.spacing * 2 + ch * 2) * sign
  sbend(x9, y9, -ch * 2 * sign)

  core = cir.update(dci.wg, 5, 90)

  dxf.bends('core', x9, y9, core, 90, 1, -sign)
  dxf.bends('core', x5, y7, core, 90, -1, 1)

  return x4, y6

def pbs4(x, y, angle, dy, ch, sign):

  dh = 1

  x1, y1 = arms(x, y, ch, sign)
  x2, y2 = sbend(x1, y1,  ch * 2 * sign)
  x3, y4 = arms(x2, y2 + cfg.spacing * sign, ch,  1)
  x3, y5 = arms(x2, y2 + cfg.spacing * sign, ch, -1)
  x4, y6 = sbend(x3, y4,  dh)
  x5, y7 = sbend(x3, y5, -dh)

  x9, y9 = x2, y2 + cfg.spacing * sign
  ports(x9, y9, angle, dy, -1, sign)

  return x4, y6

def device(x, y, dy, angle):

  ch = 2
  dh = 1
  yh = ch * 2 + cfg.spacing
  th = cfg.spacing + dh
  y1 = y + yh + th
  y2 = y - yh + th

  idev = len(cfg.data)

  x1, _ = ports(x, y, angle, dy, -1,  1)
  x1, _ = ports(x, y, angle, dy, -1, -1)
  x2, _ = pbs2(x, y, ch,  1)
  x2, _ = pbs2(x, y, ch, -1)
  x3, _ = ports(x2, y1, angle, y + dy - y1, 1,  1)
  x4, _ = ports(x2, y2, angle, y + dy + y2, 1, -1)
  x4, _ = dev.sline(x3, y + dy, x4 - x3)

  dxf.srect('edge', x, y, x2 - x, 40)

  dxf.move(idev, x1, y, x3, y, x - x1, 0, 0)

  return x, y

def device4(x, y, dy, angle):

  ch = 2
  dh = 1
  yh = ch * 2 + cfg.spacing
  th = cfg.spacing + dh
  y1 = y + yh + th
  y2 = y - yh + th

  idev = len(cfg.data)

  x1, _ = ports(x, y, angle, dy, -1,  1)
  x1, _ = ports(x, y, angle, dy, -1, -1)
  x2, _ = pbs4(x, y, angle, dy, ch,  1)
  x2, _ = pbs4(x, y, angle, dy, ch, -1)
  x3, _ = ports(x2, y1, angle, y + dy - y1, 1,  1)
  x4, _ = ports(x2, y2, angle, y + dy + y2, 1, -1)
  x4, _ = dev.sline(x3, y + dy, x4 - x3)

  dxf.srect('edge', x, y, x2 - x, 40)

  dxf.move(idev, x1, y, x3, y, x - x1, 0, 0)

  return x, y

def chip(x, y, lchip):
  
  ch = 50
  y1 = y + ch
  y2 = y - ch
  x2 = x

  idev = len(cfg.data)

  x1, _ = dev.sline(x2, y1, 50)
  x1, _ = dev.sline(x2, y2, 50)
  x1, _ = device4(x1, y, ch, 20)
  x2, _ = dev.sline(x1, y1, 50)
  x2, _ = dev.sline(x1, y2, 50)

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

  device(0, 0, 50, 20)

  # chip(0, 0, 50, 20)
  # chips(0, 0, dev.arange(18, 20, 1))

  dev.saveas(cfg.work + 'pdc')