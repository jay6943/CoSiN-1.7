import cfg
import dxf
import dev
import dci
import tip

xsize = cfg.size
ysize = 200

def units(x, y, xsign):

  x1, y1 = x, y - cfg.tapping
  x2, y2 = dci.bends(x1, y1, dci.tilted, 0, xsign, -1)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, 100 * xsign, dci.wg, cfg.wg)
  x4, y4 = dev.bends(x3, y3, 90 - dci.tilted, 0, xsign, -1)
  x5, y5 = dxf.move(idev, x2, y2, x4, y4, 0, 0, -dci.tilted * xsign)

  return x5, y5

def device(x, y):

  x1, _, x2 = lines(x, y, 100)

  x3, y3 = units(x2, y, -1)
  x3, y3 = units(x2, y,  1)

  return x1, x3, y3

def chip(x, y, lchip):
  
  ch = 50
  y1 = y + ch
  y2 = y - ch
  y3 = y1 + cfg.spacing - cfg.tapping
  dy = dci.offset + cfg.tapping - cfg.spacing

  idev = len(cfg.data)

  x1, _ = dci.sbend(x, y2, 20, ch * 2 - dy, -1,  1)
  x2, _ = dci.dc(x1, y3, -1, -1)
  x3, _ = dci.dc(x2, y3,  1, -1)
  x4, _ = dci.sbend(x3, y1 - dy, 20, ch * 2 - dy,  1, -1)

  l = (x4 - x - 250) * 0.5

  x1, _ = dev.sline(x, y1, l)
  x2, _ = dev.taper(x1, y1, 100, cfg.wg, dci.wg)
  x3, _ = dev.srect(x2, y1, 50, dci.wg)
  x5, _ = dev.taper(x3, y1, 100, dci.wg, cfg.wg)
  x6, _ = dev.sline(x5, y1, l)

  x5, x6, ltip = dev.center(idev, x, x4, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x7, t1 = tip.fiber(x5, y2, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = 'tap-' + str(round(cfg.tapping, 2))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y + ysize

def chips(x, y, arange):

  var = cfg.tapping
  for cfg.tapping in arange: _, y = chip(x, y, xsize)
  cfg.tapping = var

  return x + xsize, y

if __name__ == '__main__':

  # chip(0, 0, 3000)

  chips(0, 0, dev.arange(2.4, 2.7, 0.1))

  dev.saveas(cfg.work + 'tap')