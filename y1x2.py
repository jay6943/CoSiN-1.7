import cfg
import dxf
import dev
import tip

xsize = cfg.size
ysize = 200

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

  ch = 50

  x4 = x

  idev = len(cfg.data)

  for _ in range(5):
    x1, y1, y2 = device(x4, y, 1)
    x2, y3 = dev.sbend(x1, y1,  ch, 20, 0, 1)
    x2, y4 = dev.sbend(x1, y2, -ch, 20, 0, 1)
    x3, y1 = dev.sbend(x2, y3, -ch, 20, 0, 1)
    x3, y2 = dev.sbend(x2, y4,  ch, 20, 0, 1)
    x4, y1, y2 = device(x3, y, -1) 
  
  x5, ltip = dev.move(idev, x, x4, lchip)

  x6, _, t1 = tip.fiber(x,  y, ltip, -1)
  x6, _, t2 = tip.fiber(x5, y, ltip,  1)

  s = '1x2-' + str(int(cfg.l1x2))
  dev.texts(t1, y - 50, s, 0.5, 'lc')
  dev.texts(t2, y - 50, s, 0.5, 'rc')
  print(s, int(x6 - x))

  return x6, y + ysize

def chips(x, y, arange):

  var = cfg.l1x2

  for cfg.l1x2 in arange: _, y = chip(x, y, xsize)

  cfg.l1x2 = var

  return x + xsize, y

if __name__ == '__main__':

  chip(0, 0, xsize)
  
  # chips(0, 0, dev.arange(16, 20, 1))

  dev.saveas(cfg.work + 'y1x2')