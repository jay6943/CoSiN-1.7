import cfg
import dev
import tip

xsize = cfg.size
ysize = 200

def device(x, y, dy, l1, l2, h):

  sign = 1 if dy > 0 else -1

  x1, y1 = dev.sline(x, y + dy, l1)
  x2, y2 = dev.bends(x1, y1, 90, 0, 1, sign)
  x3, y3 = dev.tline(x2, y2, h * sign)

  x3, y3 = dev.sline(x, y, l2)

  return x3, y3

def chip(x, y, lchip, dy):
  
  idev = len(cfg.data)
  x1, y1 = dev.sline(x, y + dy, 100)
  x2, y2 = dev.sbend(x1, y1, 100 - dy, 20)
  x2, y1 = dev.sline(x, y, x2 - x)
  x5, x6, ltip = dev.center(idev, x, x2, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip,  1)
  x8, t2 = tip.fiber(x6, y2, ltip,  1)

  s = 'tap-' + str(dy)
  dev.texts(t1, y1 - 50, s, 0.2, 'lc')
  dev.texts(t2, y2 - 50, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  for dy in arange: _, y = chip(x, y + ysize, xsize, dy)

  return x + xsize, y

if __name__ == '__main__':

  # chip(0, 0, 3000)

  chips(0, 0, dev.arange(2, 4, 1))

  dev.saveas(cfg.work + 'tap')