import cfg
import dev
import tip

xsize = cfg.size
ysize = 200

def device(x, y, l1, l2, dy, sign):

  x1, y1 = dev.sline(x, y + dy, l1)
  x1, y2 = dev.bends(x1, y1, 90, 0, sign)
  x1, y1 = dev.sline(x, y, l2)

  return x1, y2

def chip(x, y, lchip, dy):
  
  idev = len(cfg.data)
  x1, y1 = dev.sline(x, y + dy, 100)
  x2, y2 = dev.sbend(x1, y1, 100 - dy, 20, 0, 1)
  x2, y1 = dev.sline(x, y, x2 - x)
  x3, ltip = dev.move(idev, x, x2, lchip)

  x6, _, t1 = tip.fiber(x,  y,  ltip, -1)
  x6, _, t2 = tip.fiber(x3, y,  ltip,  1)
  x6, _, t2 = tip.fiber(x3, y2, ltip,  1)

  s = 'tap-' + str(dy)
  dev.texts(t1, y - 50, s, 0.5, 'lc')
  print(s, int(x6 - x))

  return x6, y

def chips(x, y, arange):

  for dy in arange: _, y = chip(x, y + ysize, xsize, dy)

  return x + xsize, y

if __name__ == '__main__':

  # device(0, 0, 1500, -1)
  # chip(0, 0, 3000)

  chips(0, 0, dev.arange(2, 4, 1))

  dev.saveas('tap')