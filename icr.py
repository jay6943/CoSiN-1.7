import cfg
import dxf
import dev
import pbs
import voa
import qsk
import tip
import tap
import elr
import numpy as np

yqpsk = 2400

def sbend(x, y, angle, dy):
  
  x1, y1 = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wr)
  x2, y2 = dev.sbend(x1, y1, angle, dy)
  x3, y3 = dev.taper(x2, y2, cfg.ltpr, cfg.wr, cfg.wg)

  return x3, y3

def tbend(x, y, dy, xsign):

  ysign = 1 if dy > 0 else -1

  df = elr.update(cfg.wg, cfg.radius, 45)
  dl = np.sqrt(2) * (dy * ysign - df['dx'] - df['dy'])

  a1 = 0 if xsign > 0 else 90
  a2 = 0 if xsign < 0 else 90
  xo = df['dy'] if xsign > 0 else df['dx']
  yo = df['dx'] if xsign > 0 else df['dy']

  if xsign > 0: x, y = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wr)
  x1, y1 = dev.bends(x, y, 45, a1, xsign, ysign)
  x2, y2 = dev.tilts(x1, y1, dl, cfg.wr, 45 * ysign)
  x3, y3 = x2 + xo, y2 + yo * ysign
  x4, y4 = dev.bends(x3, y3, 45, a2, xsign, -ysign)
  if xsign < 0: x3, y3 = dev.taper(x3, y3, cfg.ltpr, cfg.wr, cfg.wg)

  return x3, y3

def fiber_pd(x, y, lchip):

  idev = len(cfg.data)
  x1, _ = dev.sline(x, y, 1000)
  x2, x3, ltip = dev.center(idev, x, x1, lchip)

  tip.fiber(x2, y, ltip, -1)
  tip.diode(x3, y, ltip,  1)

  return x + lchip, y

def chip(x, y, lchip):
  
  ch, ltip = cfg.ch * 0.5, 2000

  x1 = x + ltip
  y1 = y + ch
  y2 = y - ch
  
  tip.fiber(x1, y1, ltip, -1)
  tip.fiber(x1, y2, ltip, -1)
  
  x2, y3 = sbend(x1, y1, 45,  ch * 2)
  x2, y4 = sbend(x1, y2, 45, -ch * 2)

  ######################################################
  x3, x20, y20 = tap.device(x2, y3)
  idev = len(cfg.data)
  x21, y21 = tip.diode(x20, y20, 4000 + y20 - y, 1)
  dxf.move(idev, x20, y20, x21, y21, 0, 0, -90)
  ######################################################

  x4, _ = voa.device(x3, y3)
  x4, _ = dev.sline(x2, y4, x4 - x2)

  x5, y5 = sbend(x4, y3, 45, -ch * 2)
  x5, y6 = sbend(x4, y4, 45,  ch * 2)

  x6, _ = dev.sline(x5, y5, 500)
  x6, _ = dev.sline(x5, y6, 500)

  x7, y61, y62 = pbs.device(x6, y5)
  x7, y63, y64 = pbs.device(x6, y6)

  x9, y71 = tbend(x7, y61,  ch * 2, 1)
  x8, y72 = tbend(x7, y62, -ch * 4, 1)
  x8, y73 = tbend(x7, y63,  ch * 4, 1)
  x9, y74 = tbend(x7, y64, -ch * 2, 1)

  h1 = y + yqpsk - ch - y71 - (y71 - y61)
  h2 = y + yqpsk + ch - y73 - (y73 - y63)

  _, y81 = dev.tilts(x9, y71,  h1, cfg.wr, 90)
  _, y82 = dev.tilts(x8, y72, -h2, cfg.wr, 90)
  _, y83 = dev.tilts(x8, y73,  h2, cfg.wr, 90)
  _, y84 = dev.tilts(x9, y74, -h1, cfg.wr, 90)

  x10, _ = tbend(x9, y81,  ch * 4, -1)
  x10, _ = tbend(x8, y82, -ch * 2, -1)
  x10, _ = tbend(x8, y83,  ch * 2, -1)
  x10, _ = tbend(x9, y84, -ch * 4, -1)

  x11, y7 = qsk.device(x10, y + yqpsk)
  x11, y8 = qsk.device(x10, y - yqpsk)

  ltip = lchip - x11 + x

  for i in [-3,-1,1,3]:
    x12, _ = tip.diode(x11, y7 + i * ch, ltip, 1)
    x12, _ = tip.diode(x11, y8 + i * ch, ltip, 1)

  print('ICR', round(x11 - x1), round(x12 - x))

  return x + lchip, y

def chips(x, y):

  chip(x, y, cfg.size)

  fiber_pd(x, y + cfg.ch * 3.5 + yqpsk, cfg.size)
  voa.chip(x, y - cfg.size * 0.5 + cfg.ch * 2, cfg.size)
  pbs.chip(x, y + cfg.ch * 5 + yqpsk, cfg.size)
  qsk.chip(x, y + 4500, cfg.size)

  ysize = 8000
  
  dev.sline(x, y + ysize * 0.5, cfg.size)
  dev.sline(x, y - ysize * 0.5, cfg.size)

  return x + cfg.size, y

if __name__ == '__main__':

  # chip(0, 0, xsize)

  chips(0, 0)

  dev.saveas(cfg.work + 'icr')