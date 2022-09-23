import cfg
import dxf
import dev
import tip

xsize = cfg.size
ysize = cfg.ch

def device(x, y, ltap, sign):

  x1, _ = dev.sline(x, y, 100)
  x2, _ = dev.sline(x, y, 500)
  
  idev = len(cfg.data)
  x3, y3 = dev.sline(x1, y, 200)
  x4, y4 = dxf.move(idev, x1, y, x3, y3, 0, 0, sign * 32)
  
  idev = len(cfg.data)
  x5, y5 = dev.bends(x4, y4, 58, 90, -1)
  x6, y6 = dxf.move(idev, x4, y4, x5, y5, 0, 0, 58)

  ltip = ltap + sign * (y - y6)

  idev = len(cfg.data)
  x7, _, y7 = tip.fiber(x6, y6, ltip, 1)
  dxf.move(idev, x6, y6, x7, y7, 0, 0, sign * 90)

  return x2, y

def optima(x, y, ltap, sign):
  
  idev = len(cfg.data)
  x1, y1 = dev.sline(x, y, 200)
  x2, y2 = dxf.move(idev, x, y, x1, y1, 0, 0, sign * 122)
  
  idev = len(cfg.data)
  x3, y3 = dev.bends(x2, y2, 32, 0, -1)
  x4, y4 = dxf.move(idev, x2, y2, x3, y3, 0, 0, 32 + 90)

  ltip = ltap + sign * (y - y4)

  idev = len(cfg.data)
  x5, _, y5 = tip.fiber(x4, y4, ltip, 1)
  dxf.move(idev, x4, y4, x5, y5, 0, 0, sign * 90)

  return x, y

def chip(x, y, lchip, angle):
  
  ichip = len(cfg.data)

  idev = len(cfg.data)
  x1, y1 = dev.sline(x, y, 200)
  x2, y2 = dxf.move(idev, x, y, x1, y1, 0, 0, angle)

  idev = len(cfg.data)
  x3, y3 = dev.bends(x2, y2, angle, 0, -1)
  x4, y4 = dxf.move(idev, x2, y2, x3, y3, 0, 0, angle)
  
  dev.sline(x, y, x4 - x)
  
  x5, ltip = dev.move(ichip, x, x4, lchip)

  x6, _, t1 = tip.fiber(x,  y,  ltip, -1)
  x6, _, t2 = tip.fiber(x5, y,  ltip,  1)
  x6, _, t2 = tip.fiber(x5, y4, ltip,  1)

  s = 'tap-' + str(angle)
  dev.texts(t1, y - ysize * 0.5, s, 0.5, 'lc')
  print(s, int(x6 - x))

  return x6, y

def chips(x, y):

  for angle in [27, 32, 37]:
    _, y = chip(x, y + ysize, xsize, angle)

  return x + xsize, y

if __name__ == '__main__':

  # device(0, 0, 1500, -1)
  # chip(0, 0, 3000)

  chips(0, 0)

  dev.saveas('tap')