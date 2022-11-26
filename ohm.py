import cfg
import dxf
import dev
import tip
import euler as elr

xsize = cfg.size
ysize = 200

def devsbends(x, y, core, edge, rotate, sign):

  x1, y1 = dxf.bends('edge', x, y, edge, rotate, sign)
  x1, y1 = dxf.bends('core', x, y, core, rotate, sign)

  return x1, y1

def device(x, y, radius, angle):

  l = 25

  if angle == 45:
    
    for _ in range(10):
      x1, y1 = dev.sline(x, y, l)
      x2, y2 = dev.sbend(x1, y1, cfg.ch * 0.5, 45, 0, 1)
      x3, y3 = dev.sline(x2, y2, l * 2)
      x4, y4 = dev.sbend(x3, y3, -cfg.ch * 0.5, 45, 0, 1)
      x, y = dev.sline(x4, y4, l)

  if angle == 90:

    for _ in range(10):
      x1, y1 = dev.sline(x, y, l)
      x2, y2 = dev.sbend(x1, y1, cfg.ch, 90, 0, 1)
      x3, y3 = dev.sline(x2, y2, l * 2)
      x4, y4 = dev.sbend(x3, y3, -cfg.ch, 90, 0, 1)
      x, y = dev.sline(x4, y4, l)

  if angle == 180:

    core = elr.update(cfg.wg, radius, 180, cfg.draft)
    edge = elr.update(cfg.wg, radius, 180, 'edge')

    l = core['r'] + 80

    for _ in range(10):
      x1, y1 = dev.sline(x, y, l)
      x2, y2 = devsbends(x1, y1, core, edge, 0, 1)
      x3, y3 = dev.sline(x2, y2, -50)
      x4, y4 = devsbends(x3, y3, core, edge, 180, -1)
      x5, y5 = dev.sline(x4, y4, l * 2)
      x6, y6 = devsbends(x5, y5, core, edge, 0, -1)
      x7, y7 = dev.sline(x6, y6, -50)
      x8, y8 = devsbends(x7, y7, core, edge, 180, 1)
      x, y = dev.sline(x8, y8, l)

  if angle == 1:

    x, y = dev.sline(x, y, l)

  if angle == 2:

    x1, y1 = dev.sline(x, y, 8000)
    x2, y2 = dev.bends(x1, y1, 180, 0, 1)
    x3, y3 = dev.sline(x2, y2, -8000)
    x4, y4 = dev.bends(x3, y3, 180, 180, -1)
    x , y  = dev.sline(x4, y4, 8000)

  if angle == 3:

    x1, y1 = dev.sline(x, y, 8000)
    x2, y2 = dev.bends(x1, y1, 180, 0, 1)
    x3, y3 = dev.sline(x2, y2, -8000)
    x4, y4 = dev.bends(x3, y3, 180, 180, -1)
    x5, y5 = dev.sline(x4, y4, 8000)
    x6, y6 = dev.bends(x5, y5, 180, 0, 1)
    x7, y7 = dev.sline(x6, y6, -8000)
    x8, y8 = dev.bends(x7, y7, 180, 180, -1)
    x, y = dev.sline(x8, y8, 8000)

  return x, y

def chip(x, y, lchip, radius, angle):

  idev = len(cfg.data)
  x2, y2 = device(x, y, radius, angle)
  x5, x6, ltip = dev.xshift(idev, x, x2, lchip)

  x7, t1 = tip.fiber(x5, y,  ltip, -1)
  x8, t2 = tip.fiber(x6, y2, ltip,  1)
  
  if angle > 3:
    r = str(radius) + 'r-' + str(angle)
    dev.texts(t1, y - 50, r, 0.5, 'lc')
    dev.texts(t2, y - 50, r, 0.5, 'rc')
    print(r, int(x5 - x))
  else:
    a = (angle * 2 - 1) * 8000 + 2000
    b = (angle - 1) * 2 * 3.14 * 125
    r = str(int((a + b)))
    dev.texts(t1, y  - 50, r, 0.5, 'lc')
    dev.texts(t2, y2 - 50, r, 0.5, 'rc')
    print(r, int(x6 - x5), int(x8 - x7))

  return x + lchip, y

def chips(x, y):

  ch = 100

  _, y = dev.sline(x, y, xsize)
  _, y = dev.sline(x, y + ch, xsize)

  _, y = chip(x, y + ch, xsize, 0, 1)
  _, y = chip(x, y + ch, xsize, 0, 2)
  _, y = chip(x, y + ch * 4, xsize, 0, 3)

  _, y = chip(x, y + ch * 7, xsize, 50, 180)
  _, y = chip(x, y + ch * 2, xsize, 75, 180)
  _, y = chip(x, y + ch * 3, xsize, 100, 180)
  
  _, y = chip(x, y + ch * 3, xsize, 125, 180)
  _, y = chip(x, y + ch * 4, xsize, 125, 90)
  _, y = chip(x, y + ch * 4, xsize, 125, 45)

  return x + xsize, y

if __name__ == '__main__':

  chips(0, 0)

  dev.saveas(cfg.work + 'ohm')