import cfg
import dxf
import dev
import pbs
import tip
import y1x2
import y2x2
import numpy as np

wavelength = 1.55
nTE = 1.66636 # SiN 0.4T x 1.2W @ 1.55
nTM = 1.58571 # SiN 0.4T x 1.2W @ 1.55
refractive = (nTE + nTM) * 0.5

xsize = cfg.size
ysize = cfg.ch * 4

def sbend(x, y):

  cfg.draft = 'mask'

  x1, y1 = dev.sline(x, y, 10)
  x2, y2 = dev.sbend(x1, y1, 45, 20)
  x3, y3 = dev.sline(x2, y2, 10)

  return x3, y3

def device(x, y):

  k = wavelength / refractive
  h = cfg.phase * k / (4 * (np.sqrt(2) - 1)) / 180

  l = 50

  ch1x2 = cfg.ch - cfg.d1x2
  ch2x2 = cfg.ch * 0.5 - cfg.d2x2
  ph1x2 = ch1x2 + h
  ph2x2 = ch2x2 + h

  x1, y11, y12 = y1x2.device(x, y + cfg.ch * 0.5, 1)
  x2, y21, y22 = y1x2.device(x, y - cfg.ch * 0.5, 1)

  x3, y1 = dev.sbend(x1, y11, 45,  ph1x2)
  x4, y2 = dev.sbend(x1, y12, 45, -ch1x2)
  x4, y3 = dev.sbend(x2, y21, 45,  ch1x2)
  x4, y4 = dev.sbend(x2, y22, 45, -ch1x2)

  xl = np.sqrt(0.5) * cfg.eg

  xh = (x4 + x2) * 0.5 - xl
  ya = (y1 + y11) * 0.5 + xl
  yb = (y4 + y22) * 0.5 - xl

  dxf.tilts('core', xh, ya, cfg.eg * 2, cfg.wg, -45)
  dxf.tilts('core', xh, yb, cfg.eg * 2, cfg.wg,  45)

  x5, _ = dev.sline(x3, y1, l - h * 2)
  x6, _ = dev.sline(x4, y2, l)
  x6, _ = dev.sline(x4, y3, l)
  x6, _ = dev.sline(x4, y4, l)

  x7, _ = dev.sbend(x5, y1, 45, -ph2x2)
  x7, _ = dev.sbend(x6, y2, 45, -ch2x2)
  x7, _ = dev.sbend(x6, y3, 45,  ch2x2)
  x7, _ = dev.sbend(x6, y4, 45,  ch2x2)

  x8, y31, y32 = y2x2.device(x7, y + cfg.ch)
  x8, y41, y42 = y2x2.device(x7, y - cfg.ch)

  x9, _ = dev.sbend(x8, y31, 45,  ch2x2)
  x9, _ = dev.sbend(x8, y32, 45, -ch2x2)
  x9, _ = dev.sbend(x8, y41, 45,  ch2x2)
  x9, _ = dev.sbend(x8, y42, 45, -ch2x2)

  return x9, y

def chip2x2(x, y):

  y1 = y + cfg.ch * 0.5
  y2 = y - cfg.ch * 0.5

  ch1x2 = cfg.ch - cfg.d1x2
  ch2x2 = cfg.ch - cfg.d2x2

  x1, _ = dev.sbend(x, y1, 2, cfg.d2x2)
  x2, _ = dev.sline(x, y2, x1 - x)
  pbs.tail(x1, y1 - cfg.d2x2, 90, 90, 1, 1)
  x1, y11, y12 = y2x2.device(x1, y1)
  x2, y21, y22 = y1x2.device(x2, y2, 1)

  x3, y31 = dev.sbend(x1, y11, 45,  ch2x2)
  x3, y32 = dev.sbend(x1, y12, 45, -ch2x2)
  x4, y41 = dev.sbend(x2, y21, 45,  ch1x2)
  x4, y42 = dev.sbend(x2, y22, 45, -ch1x2)

  xl = np.sqrt(0.5) * cfg.eg

  xa = (x3 + x1) * 0.5 - xl
  xb = (x4 + x2) * 0.5 - xl
  ya = (y31 + y41) * 0.5 + xl
  yb = (y32 + y42) * 0.5 - xl

  dxf.tilts('core', xa, ya, cfg.eg * 2, cfg.wg, -45)
  dxf.tilts('core', xb, yb, cfg.eg * 2, cfg.wg,  45)

  x5, _ = dev.sline(x4, y41, x3 - x4)
  x5, _ = dev.sline(x4, y42, x3 - x4)

  ch2x2 = cfg.ch * 0.5 - cfg.d2x2

  x7, _ = dev.sbend(x5, y31, 45, -ch2x2)
  x7, _ = dev.sbend(x5, y32, 45, -ch2x2)
  x7, _ = dev.sbend(x5, y41, 45,  ch2x2)
  x7, _ = dev.sbend(x5, y42, 45,  ch2x2)

  x8, y31, y32 = y2x2.device(x7, y + cfg.ch)
  x8, y41, y42 = y2x2.device(x7, y - cfg.ch)

  x9, _ = dev.sbend(x8, y31, 45,  ch2x2)
  x9, _ = dev.sbend(x8, y32, 45, -ch2x2)
  x9, _ = dev.sbend(x8, y41, 45,  ch2x2)
  x9, _ = dev.sbend(x8, y42, 45, -ch2x2)

  return x9, y

def chip(x, y, lchip):

  ch = cfg.ch * 0.5

  idev = len(cfg.data)
  # x1, _ = device(x, y)
  x1, _ = chip2x2(x, y)
  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y + ch, ltip, -1)
  x7, t1 = tip.fiber(x5, y - ch, ltip, -1)

  for i in [3,1,-1,-3]: x8, t2 = tip.fiber(x6, y + ch * i, ltip, 1)

  s = 'iq-' + str(round(cfg.phase))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))
  
  return x + lchip, y + ysize

def chips(x, y, arange):

  var = cfg.phase
  for cfg.phase in arange: _, y = chip(x, y, xsize)
  cfg.phase = var

  return x + xsize, y - ysize * 0.5

if __name__ == '__main__':

  chip(0, 0, 0)
  
  # chips(0, 0, dev.arange(70, 115, 5))

  dev.saveas(cfg.work + 'psk')