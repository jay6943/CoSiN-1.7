import cfg
import dxf
import dev
import elr
import dci
import tip
import y1x2
import numpy as np

def sbend(x, y, angle, dy):

  core = elr.update(cfg.wg, cfg.radius, angle)
  edge = elr.update(cfg.eg, cfg.radius, angle)
  sio2 = elr.update(cfg.sg, cfg.radius, angle)

  x1, y1 = dxf.sbend('edge', x, y, edge, angle, dy)
  x1, y1 = dxf.sbend('core', x, y, core, angle, dy)
  x1, y1 = dxf.sbend('sio2', x, y, sio2, angle, dy)

  return x1, y1

def device(x, y):

  y1 = y + cfg.ch * 0.5
  y2 = y - cfg.ch * 0.5

  dy = 10

  x1, y3 = sbend(x, y1, 9, dy)
  x1, _ = dci.sbend(x1, y3, 4, dy - dci.offset, -1, -1)
  x1, y11, y12 = dci.device(x1, y1)

  x2, _ = dev.sline(x, y2, x1 - x - cfg.l1x2 - 100)
  x2, y21, y22 = y1x2.device(x2, y2, 1)

  dy = cfg.ch - dci.offset
  ch = cfg.ch - cfg.d1x2

  x3, y31 = dci.sbend(x1, y11, 45, dy, 1,  1)
  x3, y32 = dci.sbend(x1, y12, 45, dy, 1, -1)
  x4, y41 = dev.sbend(x2, y21, 45,  ch)
  x4, y42 = dev.sbend(x2, y22, 45, -ch)

  xl = np.sqrt(0.5) * cfg.eg

  xa = (x3 + x1) * 0.5 - xl
  xb = (x4 + x2) * 0.5 - xl
  ya = (y31 + y41) * 0.5 + xl
  yb = (y32 + y42) * 0.5 - xl

  dxf.tilts('core', xa, ya, cfg.eg * 2, cfg.wg, -45)
  dxf.tilts('core', xb, yb, cfg.eg * 2, cfg.wg,  45)

  x5, _ = dev.sline(x4, y41, x3 - x4)
  x5, _ = dev.sline(x4, y42, x3 - x4)

  dy = cfg.ch * 0.5 - dci.offset

  x6, _ = dci.sbend(x5, y31, 45, dy, -1, -1)
  x6, _ = dci.sbend(x5, y32, 45, dy, -1, -1)
  x6, _ = dci.sbend(x5, y41, 45, dy, -1,  1)
  x6, _ = dci.sbend(x5, y42, 45, dy, -1,  1)

  x7, y71, y72 = dci.device(x6, y + cfg.ch)
  x7, y73, y74 = dci.device(x6, y - cfg.ch)

  x8, _ = dci.sbend(x7, y71, 45, dy, 1,  1)
  x8, _ = dci.sbend(x7, y72, 45, dy, 1, -1)
  x8, _ = dci.sbend(x7, y73, 45, dy, 1,  1)
  x8, _ = dci.sbend(x7, y74, 45, dy, 1, -1)

  return x8, y

def chip(x, y, lchip):

  y = y + cfg.ch * 1.5

  ch = cfg.ch * 0.5

  idev = len(cfg.data)
  x1, _ = device(x, y)
  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y + ch, ltip, -1)
  x7, t1 = tip.fiber(x5, y - ch, ltip, -1)

  for i in [3,1,-1,-3]: x8, t2 = tip.fiber(x6, y + ch * i, ltip, 1)

  s = 'iq-dc-' + str(round(cfg.spacing, 2))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y + cfg.ch * 1.5

if __name__ == '__main__':

  chip(0, 0, 0)
  
  dev.saveas(cfg.work + 'qdc')