import cfg
import dxf
import dev
import tip

xsize = cfg.size
ysize = cfg.ch * 2

def taper(x, y, wstart, wstop):

  x1, _ = dxf.taper('core', x,  y, cfg.ltpr, wstart, cfg.wt)
  x2, _ = dxf.srect('core', x1, y, 50 - cfg.ltpr * 2, cfg.wt)
  x3, _ = dxf.taper('core', x2, y, cfg.ltpr, cfg.wt, wstop)

  return x3, y

def device(x, y):

  y1 = y + cfg.d2x2
  y2 = y - cfg.d2x2

  x1, _ = taper(x, y1, cfg.wg, cfg.wtpr)
  x1, _ = taper(x, y2, cfg.wg, cfg.wtpr)
  x2, _ = dxf.srect('core', x1, y, cfg.l2x2, cfg.w2x2)
  x3, _ = taper(x2, y1, cfg.wtpr, cfg.wg)
  x3, _ = taper(x2, y2, cfg.wtpr, cfg.wg)

  dxf.srect('edge', x, y, x3 - x, cfg.w2x2 + cfg.eg)

  return x3, y1, y2

def chip(x, y, lchip):

  ch = cfg.ch * 0.5
  dh = ch - cfg.d2x2

  y1 = y + ch
  y2 = y - ch
  
  x9 = x

  idev = len(cfg.data)

  for _ in range(10):
    x1, y1 = dev.sbend(x9, y1, -dh, 45, 0, 1)
    x1, y2 = dev.sbend(x9, y2,  dh, 45, 0, 1)
    x2, y3, y4 = device(x1, y)
    x9, y1 = dev.sbend(x2, y3,  dh, 45, 0, 1)
    x9, y2 = dev.sbend(x2, y4, -dh, 45, 0, 1)
  
  x8, ltip = dev.move(idev, x, x9, lchip)

  x9, _, t1 = tip.fiber(x, y1, ltip, -1)
  x9, _, t1 = tip.fiber(x, y2, ltip, -1)
  x9, _, t2 = tip.fiber(x8, y1, ltip, 1)
  x9, _, t2 = tip.fiber(x8, y2, ltip, 1)

  s = '2x2-' + str(round(cfg.l2x2, 1))
  dev.texts(t1, y, s, 0.5, 'lc')
  dev.texts(t2, y, s, 0.5, 'rc')
  print(s, int(x9 - x))

  return x9, y + ysize

def chips(x, y, arange):

  var = cfg.l2x2

  for cfg.l2x2 in arange: _, y = chip(x, y, xsize)

  cfg.l2x2 = var

  return x + xsize, y

if __name__ == '__main__':

  # chip(0, 0, xsize)

  chips(0, 0, dev.arange(49, 53, 1))

  dev.saveas('y2x2')