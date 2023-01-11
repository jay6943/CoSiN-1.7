import cfg
import dxf
import dev
import tip

def taper(x, y, wstart, wstop):

  x1, _ = dxf.taper('core', x,  y, cfg.ltpr, wstart, cfg.wg)
  x2, _ = dxf.srect('core', x1, y, 50 - cfg.ltpr * 2, cfg.wg)
  x3, _ = dxf.taper('core', x2, y, cfg.ltpr, cfg.wg, wstop)

  return x3, y

def device(x, y):

  y1 = y + cfg.d2x2
  y2 = y - cfg.d2x2

  x1, _ = taper(x, y1, cfg.wr, cfg.wtpr)
  x1, _ = taper(x, y2, cfg.wr, cfg.wtpr)
  x2, _ = dxf.srect('core', x1, y, cfg.l2x2, cfg.w2x2)
  x3, _ = taper(x2, y1, cfg.wtpr, cfg.wr)
  x3, _ = taper(x2, y2, cfg.wtpr, cfg.wr)

  dxf.srect('edge', x, y, x3 - x, cfg.w2x2 + cfg.eg)
  dxf.srect('sio2', x, y, x3 - x, cfg.w2x2 + cfg.sg)

  return x3, y1, y2

def chip(x, y, lchip):

  ch = 50
  dh = ch - cfg.d2x2

  y1 = y + ch
  y2 = y - ch
  
  idev = len(cfg.data)

  x1, y1 = dev.sbend(x, y1, 20, -dh)
  x1, y2 = dev.sbend(x, y2, 20,  dh)
  x2, y3, y4 = device(x1, y)
  x3, y1 = dev.sbend(x2, y3, 20,  dh)
  x3, y2 = dev.sbend(x2, y4, 20, -dh)
  
  x5, x6, ltip = dev.center(idev, x, x3, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x7, t1 = tip.fiber(x5, y2, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = '2x2-' + str(round(cfg.l2x2, 1))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  y = y - cfg.sch * 1.5

  var = cfg.l2x2
  for cfg.l2x2 in arange: _, y = chip(x, y + cfg.sch * 2, cfg.size)
  cfg.l2x2 = var

  return x + cfg.size, y + cfg.sch * 0.5

if __name__ == '__main__':

  # chip(0, 0, xsize)

  chips(0, 0, dev.arange(49, 53, 1))

  dev.saveas(cfg.work + '2x2')