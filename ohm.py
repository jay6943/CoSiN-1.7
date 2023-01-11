import cfg
import dxf
import dev
import tip
import elr

def bends(x, y, radius, angle, rotate, xsign, ysign):

  core = elr.update(cfg.wr, radius, angle)
  edge = elr.update(cfg.eg, radius, angle)
  sio2 = elr.update(cfg.sg, radius, angle)

  x1, y1 = dxf.bends('edge', x, y, edge, rotate, xsign, ysign)
  x1, y1 = dxf.bends('core', x, y, core, rotate, xsign, ysign)
  x1, y1 = dxf.bends('sio2', x, y, sio2, rotate, xsign, ysign)

  return x1, y1

def device(x, y, radius, angle):

  l = 25

  if angle == 45:
    
    for _ in range(10):
      x1, y1 = dev.srect(x, y, l, cfg.wr)
      x2, y2 = dev.sbend(x1, y1, 45, cfg.ch * 0.5)
      x3, y3 = dev.srect(x2, y2, l * 2, cfg.wr)
      x4, y4 = dev.sbend(x3, y3, 45, -cfg.ch * 0.5)
      x, y = dev.srect(x4, y4, l, cfg.wr)

  if angle == 90:

    for _ in range(10):
      x1, y1 = dev.srect(x, y, l, cfg.wr)
      x2, y2 = dev.sbend(x1, y1, 90, cfg.ch)
      x3, y3 = dev.srect(x2, y2, l * 2, cfg.wr)
      x4, y4 = dev.sbend(x3, y3, 90, -cfg.ch)
      x, y = dev.srect(x4, y4, l, cfg.wr)

  if angle == 180:

    l = 200

    for _ in range(10):
      x1, y1 = dev.srect(x, y, l, cfg.wr)
      x2, y2 = bends(x1, y1, radius, 180, 0, 1, 1)
      x3, y3 = dev.srect(x2, y2, -50, cfg.wr)
      x4, y4 = bends(x3, y3, radius, 180, 180, 1, -1)
      x5, y5 = dev.srect(x4, y4, l * 2, cfg.wr)
      x6, y6 = bends(x5, y5, radius, 180, 0, 1, -1)
      x7, y7 = dev.srect(x6, y6, -50, cfg.wr)
      x8, y8 = bends(x7, y7, radius, 180, 180, 1, 1)
      x, y = dev.srect(x8, y8, l, cfg.wr)

  if angle == 1:

    x, y = dev.srect(x, y, 8000, cfg.wr)

  if angle == 2:

    x1, y1 = dev.srect(x, y, 8000, cfg.wr)
    x2, y2 = dev.bends(x1, y1, 180, 0, 1, 1)
    x3, y3 = dev.srect(x2, y2, -8000, cfg.wr)
    x4, y4 = dev.bends(x3, y3, 180, 0, -1, 1)
    x , y  = dev.srect(x4, y4, 8000, cfg.wr)

  if angle == 3:

    x1, y1 = dev.srect(x, y, 8000, cfg.wr)
    x2, y2 = dev.bends(x1, y1, 180, 0, 1, 1)
    x3, y3 = dev.srect(x2, y2, -8000, cfg.wr)
    x4, y4 = dev.bends(x3, y3, 180, 0, -1, 1)
    x5, y5 = dev.srect(x4, y4, 8000, cfg.wr)
    x6, y6 = dev.bends(x5, y5, 180, 0, 1, 1)
    x7, y7 = dev.srect(x6, y6, -8000, cfg.wr)
    x8, y8 = dev.bends(x7, y7, 180, 0, -1, 1)
    x, y = dev.srect(x8, y8, 8000, cfg.wr)

  return x, y

def chip(x, y, lchip, radius, angle):

  ch = cfg.sch * 0.5

  idev = len(cfg.data)
  x1, y1 = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wr)
  x2, y2 = device(x1, y1, radius, angle)
  x4, y4 = dev.taper(x2, y2, cfg.ltpr, cfg.wr, cfg.wg)
  x5, x6, ltip = dev.center(idev, x, x4, lchip)

  x7, t1 = tip.fiber(x5, y,  ltip, -1)
  x8, t2 = tip.fiber(x6, y2, ltip,  1)
  
  if angle > 3:
    r = str(radius) + 'r-' + str(angle)
    dev.texts(t1, y - ch, r, 0.2, 'lc')
    dev.texts(t2, y - ch, r, 0.2, 'rc')
    print(r, round(x5 - x))
  else:
    a = (angle * 2 - 1) * 8000 + 2000
    b = (angle - 1) * 2 * 3.14 * 125
    r = str(round(a + b))
    dev.texts(t1, y  - ch, r, 0.2, 'lc')
    dev.texts(t2, y2 - ch, r, 0.2, 'rc')
    print(r, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y):

  _, y = chip(x, y, cfg.size, 0, 1)
  _, y = chip(x, y + cfg.sch, cfg.size, 0, 2)
  _, y = chip(x, y + cfg.sch * 4, cfg.size, 0, 3)

  _, y = chip(x, y + cfg.sch * 6, cfg.size, 50, 180)
  _, y = chip(x, y + cfg.sch * 2, cfg.size, 75, 180)
  _, y = chip(x, y + cfg.sch * 3, cfg.size, 100, 180)
  
  _, y = chip(x, y + cfg.sch * 3, cfg.size, 125, 180)
  _, y = chip(x, y + cfg.sch * 4, cfg.size, 125, 90)
  _, y = chip(x, y + cfg.sch * 4, cfg.size, 125, 45)

  return x + cfg.size, y

if __name__ == '__main__':

  chips(0, 0)

  dev.saveas(cfg.work + 'ohm')