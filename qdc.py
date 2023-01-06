import cfg
import dxf
import dev
import dci
import tip
import y1x2
import numpy as np

xsize = cfg.size
ysize = cfg.ch * 4

def units(x, y, angle, ch):

  idev = len(cfg.data)

  x1, _ = dci.units(x, y, angle, ch, -1,  1)
  x1, _ = dci.units(x, y, angle, ch, -1, -1)
  x2, y1 = dci.units(x, y, 45, cfg.ch,  1,  1)
  x2, y2 = dci.units(x, y, 45, cfg.ch,  1, -1)

  dxf.move(idev, x, y, x1, y1, x - x1, 0, 0)

  return x2, y1, y2

def device(x, y):

  y1 = y + cfg.ch * 0.5
  y2 = y - cfg.ch * 0.5

  ch1x2 = cfg.ch - cfg.d1x2
  ch2x2 = cfg.ch - cfg.d2x2

  x1, _ = dev.sbend(x, y1, 2, cfg.d2x2)
  x2, _ = dev.sline(x, y2, x1 - x)
  x3, y31, y32 = units(x1, y1, 5, 20)
  x2, y21, y22 = y1x2.device(x2, y2, 1)

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

  x8, _ = dci.device(x5, y + cfg.ch, 45, cfg.ch * 0.5)
  x8, _ = dci.device(x5, y - cfg.ch, 45, cfg.ch * 0.5)

  return x8, y

def chip(x, y, lchip):

  ch = cfg.ch * 0.5

  idev = len(cfg.data)
  x1, _ = device(x, y)
  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y + ch, ltip, -1)
  x7, t1 = tip.fiber(x5, y - ch, ltip, -1)

  for i in [3,1,-1,-3]: x8, t2 = tip.fiber(x6, y + ch * i, ltip, 1)

  s = 'iq-dc-' + str(round(cfg.phase))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))
  
  return x + lchip, y + ysize

if __name__ == '__main__':

  chip(0, 0, 0)
  
  dev.saveas(cfg.work + 'qdc')