import cfg
import dxf
import dev
import dci
import tip

def device(x, y):

  dy = dci.offset + cfg.tapping - cfg.spacing

  y1 = y + cfg.spacing - cfg.tapping
  y2 = y - dy

  x1, _ = dev.taper(x, y, dci.ltaper, cfg.wg, dci.wg)
  x2, _ = dev.srect(x1, y, 50, dci.wg)
  x3, _ = dev.srect(x2, y, 50, dci.wg)
  x4, _ = dev.taper(x3, y, dci.ltaper, dci.wg, cfg.wg)
  x5, _ = dev.sline(x4, y, 200)

  x6, _ = dci.arm(x2, y1, -1, -1)
  x6, _ = dci.arm(x2, y1,  1, -1)

  idev = len(cfg.data)
  x7, y7 = dev.taper(x6, y2, cfg.ltpr, cfg.wg, cfg.wr)
  x7, y7 = dev.bends(x7, y7, 90 - dci.tilted, 0, 1, -1)
  x8, y8 = dxf.move(idev, x6, y2, x7, y7, 0, 0, -dci.tilted)

  return x5, x8, y8

def chip(x, y, lchip):
  
  ch = cfg.sch * 0.5

  y1 = y + ch
  y2 = y - ch
  y3 = y1 + cfg.spacing - cfg.tapping
  dy = dci.offset + cfg.tapping - cfg.spacing

  idev = len(cfg.data)

  x1, _ = dci.sbend(x, y2, 20, ch * 2 - dy, -1,  1)
  x2, _ = dci.dc(x1, y3, -1, -1)
  x3, _ = dci.dc(x2, y3,  1, -1)
  x4, _ = dci.sbend(x3, y1 - dy, 20, ch * 2 - dy,  1, -1)

  s = 50
  l = (x4 - x - dci.ltaper * 2 - s) * 0.5

  x1, _ = dev.sline(x, y1, l)
  x2, _ = dev.taper(x1, y1, dci.ltaper, cfg.wg, dci.wg)
  x3, _ = dev.srect(x2, y1, s, dci.wg)
  x5, _ = dev.taper(x3, y1, dci.ltaper, dci.wg, cfg.wg)
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

  return x + lchip, y

def chips(x, y, arange):

  y = y - cfg.sch * 1.5

  var = cfg.tapping
  for cfg.tapping in arange: _, y = chip(x, y + cfg.sch * 2, cfg.size)
  cfg.tapping = var

  return x + cfg.size, y + cfg.sch * 0.5

if __name__ == '__main__':

  # chip(0, 0, 3000)

  chips(0, 0, dev.arange(2.4, 2.7, 0.1))

  dev.saveas(cfg.work + 'tap')