import cfg
import dxf
import dev
import tip

xsize = cfg.size
ysize = cfg.ch

def taper(x, y, wstart, wstop):

  x1, _ = dxf.taper('core', x,  y, cfg.ltpr, wstart, cfg.wt)
  x2, _ = dxf.srect('core', x1, y, 50 - cfg.ltpr * 2, cfg.wt)
  x3, _ = dxf.taper('core', x2, y, cfg.ltpr, cfg.wt, wstop)

  return x3, y

def device(x, y, sign):
  
  y1 = y + cfg.d1x2
  y2 = y - cfg.d1x2
  
  if sign > 0:
    x1, _ = taper(x, y, cfg.wg, cfg.wtpr)
    x2, _ = dxf.srect('core', x1, y, cfg.l1x2, cfg.w1x2)
    x3, _ = taper(x2, y1, cfg.wtpr, cfg.wg)
    x3, _ = taper(x2, y2, cfg.wtpr, cfg.wg)
  else:
    x1, _ = taper(x, y1, cfg.wg, cfg.wtpr)
    x1, _ = taper(x, y2, cfg.wg, cfg.wtpr)
    x2, _ = dxf.srect('core', x1, y, cfg.l1x2, cfg.w1x2)
    x3, _ = taper(x2, y, cfg.wtpr, cfg.wg)
  
  dxf.srect('edge', x, y, x3 - x, cfg.w1x2 + cfg.eg)

  return x3, y1, y2

def chip(x, y, lchip):

  idev = len(cfg.data)
  
  x1, _ = taper(x, y, cfg.wg, cfg.wtpr)
  for i in range(10):
    x2, _ = dxf.srect('core', x1, y, cfg.l1x2, cfg.w1x2)
    x3, _ = taper(x2, y + cfg.d1x2, cfg.wtpr, cfg.wtpr)
    x3, _ = taper(x2, y - cfg.d1x2, cfg.wtpr, cfg.wtpr)
    x4, _ = dxf.srect('core', x3, y, cfg.l1x2, cfg.w1x2)
    if i < 9: x1, _ = taper(x4, y, cfg.wtpr, cfg.wtpr)
  x2, _ = taper(x4, y, cfg.wtpr, cfg.wg)

  dxf.srect('edge', x, y, x2 - x, cfg.w1x2 + cfg.eg)

  x3, ltip = dev.move(idev, x, x2, lchip)

  x4, _, t1 = tip.fiber(x,  y, ltip, -1)
  x4, _, t2 = tip.fiber(x3, y, ltip,  1)

  s = '1x2-' + str(int(cfg.l1x2))
  dev.texts(t1, y - ysize * 0.5, s, 0.5, 'lc')
  dev.texts(t2, y - ysize * 0.5, s, 0.5, 'rc')
  print(s, int(x4 - x))

  return x4, y + ysize

def chips(x, y, arange):

  var = cfg.l1x2

  for cfg.l1x2 in arange: _, y = chip(x, y, xsize)

  cfg.l1x2 = var

  return x + xsize, y

if __name__ == '__main__':

  chip(0, 0, 4000)
  
  # chips(0, 0, dev.arange(16, 20, 1))

  dev.saveas('y1x2')