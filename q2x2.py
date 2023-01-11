import cfg
import dxf
import dev
import elr
import pbs
import tip
import y1x2
import y2x2
import numpy as np

def sbend(x, y, angle, dy):

  core = elr.update(cfg.wg, cfg.radius, angle)
  edge = elr.update(cfg.eg, cfg.radius, angle)
  sio2 = elr.update(cfg.sg, cfg.radius, angle)

  x1, y1 = dxf.sbend('edge', x, y, edge, angle, dy)
  x1, y1 = dxf.sbend('core', x, y, core, angle, dy)
  x1, y1 = dxf.sbend('sio2', x, y, sio2, angle, dy)

  return x1, y1

def shifter(x, y):

  y1 = y + cfg.d2x2
  y2 = y - cfg.d2x2

  x1, _ = dxf.srect('core', x, y1, 50 - cfg.ltpr * 2, cfg.wg)
  x1, _ = dxf.taper('core', x1, y1, cfg.ltpr, cfg.wg, cfg.wtpr)
  x2, _ = dxf.srect('core', x1, y, cfg.l2x2, cfg.w2x2)
  x3, _ = y2x2.taper(x2, y1, cfg.wtpr, cfg.wr)
  x3, _ = y2x2.taper(x2, y2, cfg.wtpr, cfg.wr)

  pbs.tail(x1 - 5, y2, 90, 90, 1, 1)

  dxf.srect('edge', x, y, x3 - x, cfg.w2x2 + cfg.eg)
  dxf.srect('sio2', x, y, x3 - x, cfg.w2x2 + cfg.sg)

  return x3, y1, y2

def device(x, y):

  y1 = y + cfg.ch * 0.5
  y2 = y - cfg.ch * 0.5

  ch1x2 = cfg.ch - cfg.d1x2
  ch2x2 = cfg.ch - cfg.d2x2

  x1, _ = sbend(x, y1, 2, cfg.d2x2)
  x2, _ = dev.sline(x, y2, x1 - x)
  x1, y11, y12 = shifter(x1, y1)
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

  for i in [y + cfg.ch * (i - 1.5) for i in range(4)]:
    x10, _ = dev.taper(x9, i, cfg.ltpr, cfg.wr, cfg.wg)

  return x10, y

def chip(x, y, lchip):

  y = y + cfg.ch * 1.5

  ch = cfg.ch * 0.5

  idev = len(cfg.data)
  x1, _ = device(x, y)
  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y + ch, ltip, -1)
  x7, t1 = tip.fiber(x5, y - ch, ltip, -1)

  for i in [3,1,-1,-3]: x8, t2 = tip.fiber(x6, y + ch * i, ltip, 1)

  s = 'iq-2x2-' + str(round(cfg.phase))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))
  
  return x + lchip, y + cfg.ch * 1.5

if __name__ == '__main__':

  chip(0, 0, 0)
  
  dev.saveas(cfg.work + 'q2x2')