import cfg
import dev
import dci
import tip

xsize = cfg.size
ysize = 200

def chip(x, y, lchip):
  
  ch = 50
  y1 = y + ch
  y2 = y - ch

  idev = len(cfg.data)

  x1, _ = dev.sline(x, y2, 50)
  x1, _ = dci.device(x1, y, ch, 20)
  x2, _ = dev.sline(x1, y1, 50)
  x2, _ = dev.sline(x1, y2, 50)

  x5, x6, ltip = dev.center(idev, x, x2, lchip)

  x7, t1 = tip.fiber(x5, y2, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = 'tap-' + str(round(cfg.dc, 2))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y + ysize

def chips(x, y, arange):

  var = cfg.dc

  for cfg.dc in arange: _, y = chip(x, y, xsize)

  cfg.dc = var

  return x + xsize, y

if __name__ == '__main__':

  # chip(0, 0, 3000)

  chips(0, 0, dev.arange(1.1, 1.3, 0.1))

  dev.saveas(cfg.work + 'tap')