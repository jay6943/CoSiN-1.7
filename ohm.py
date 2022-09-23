import cfg
import dev
import tip
import euler as er

xsize = cfg.size
ysize = cfg.ch * 2

def device(x, y, angle):

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

    l = er.bends[str(er.radius) + '_180_' + cfg.draft]['r'] + 80

    for _ in range(10):
      x1, y1 = dev.sline(x, y, l)
      x2, y2 = dev.bends(x1, y1, 180, 0, 1)
      x3, y3 = dev.sline(x2, y2, -50)
      x4, y4 = dev.bends(x3, y3, 180, 180, -1)
      x5, y5 = dev.sline(x4, y4, l * 2)
      x6, y6 = dev.bends(x5, y5, 180, 0, -1)
      x7, y7 = dev.sline(x6, y6, -50)
      x8, y8 = dev.bends(x7, y7, 180, 180, 1)
      x, y = dev.sline(x8, y8, l)

  if angle == 0:

    x, y = dev.sline(x, y, l)

  if angle == 1:

    x1, y1 = dev.sline(x, y, 8000)
    x2, y2 = dev.bends(x1, y1, 180, 0, 1)
    x3, y3 = dev.sline(x2, y2, -8000)
    x4, y4 = dev.bends(x3, y3, 180, 180, -1)
    x , y  = dev.sline(x4, y4, 8000)

  if angle == 2:

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

def chip(x, y, lchip, angle):

  idev = len(cfg.data)
  x2, y2 = device(x, y, angle)
  x4, ltip = dev.move(idev, x, x2, lchip)

  x5, _, t1 = tip.fiber(x,  y,  ltip, -1)
  x5, _, t2 = tip.fiber(x4, y2, ltip,  1)
  
  if angle > 2:
    r = str(er.radius) + 'r-' + str(angle)
    dev.texts(t1, y - cfg.ch * 0.5, r, 0.5, 'lc')
    dev.texts(t2, y - cfg.ch * 0.5, r, 0.5, 'rc')
    print(r, int(x5 - x))

  return x5, y

def chips(x, y):

  _, y = chip(x, y, xsize, 0)
  _, y = chip(x, y + cfg.ch, xsize, 1)
  _, y = chip(x, y + ysize, xsize, 2)
  er.radius = 50
  _, y = chip(x, y + cfg.ch * 3, xsize, 180)
  er.radius = 75
  _, y = chip(x, y + cfg.ch, xsize, 180)
  er.radius = 100
  _, y = chip(x, y + cfg.ch, xsize, 180)
  er.radius = 125
  _, y = chip(x, y + cfg.ch * 2, xsize, 180)
  _, y = chip(x, y + ysize, xsize, 90)
  _, y = chip(x, y + ysize, xsize, 45)

  return x + xsize, y

if __name__ == '__main__':

  chips(0, 0)

  dev.saveas('ohm')