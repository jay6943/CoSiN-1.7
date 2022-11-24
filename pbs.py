import cfg
import dxf
import dev
import cir
import tip

xsize = cfg.size
ysize = 200

def taper(x, y, sign):

  w1 = cfg.wg if sign < 0 else cfg.wtpr
  w2 = cfg.wtpr if sign < 0 else cfg.wg

  if sign < 0:
    x, _ = dxf.taper('core', x, y, 5, cfg.wg, cfg.wt)
    x, _ = dxf.srect('core', x, y, 40, cfg.wt)
    x, _ = dxf.taper('core', x, y, 5, cfg.wt, cfg.wg)
    x, _ = dxf.sline('core', x, y, 10)
  x, _ = dxf.taper('core', x, y, cfg.ltpr, w1, w2)

  return x, y

def arm(x, y, length, width):

  l, w, ltaper = 40, width, 10

  x1, _ = dxf.taper('core', x, y, cfg.ltpr, cfg.wtpr, cfg.wg)
  x2, _ = dxf.srect('core', x1, y, l, cfg.wg)
  x3, _ = dxf.taper('core', x2, y, ltaper, cfg.wg, w)
  
  if length > 0:
    x4, _ = dxf.srect('core', x3, y, length, w)
  else:
    l = l + length + cfg.lpbs
    x4 = x3
  
  x5, _ = dxf.taper('core', x4, y, ltaper, w, cfg.wg)
  x6, _ = dxf.srect('core', x5, y, l, cfg.wg)
  x7, _ = dxf.taper('core', x6, y, cfg.ltpr, cfg.wg, cfg.wtpr)

  return x7, y

def tail(x, y, angle, rotate, port, sign):

  core = cir.update(cfg.wg, 5, angle, 'draft')

  x1, y1 = dxf.taper('core', x, y, sign * cfg.ltpr, cfg.wg, cfg.wtpr)
  x1, y1 = dxf.bends('core', x, y, core, rotate, port)

  w = cfg.wg * 0.5
  s = 1 if rotate != 90 else -1

  data = ['core']
  data.append([x1 + w, y1])
  data.append([x1 + 0.05, y1 + s * port * 5])
  data.append([x1 - 0.05, y1 + s * port * 5])
  data.append([x1 - w, y1])
  cfg.data.append(data)

  return x1, y1

def mzi(x, y, inport, outport):

  y1 = y + cfg.d2x2
  y2 = y - cfg.d2x2
  y3 = y + inport * cfg.d2x2
  y4 = y - outport * cfg.d2x2

  x1, _ = taper(x, y3, -1)
  x2, _ = dxf.srect('core', x1, y, cfg.l2x2, cfg.w2x2)

  x5, _ = arm(x2, y1, 0, cfg.wpbs)
  x5, _ = arm(x2, y2, cfg.lpbs, cfg.wpbs)

  x6, _ = dxf.srect('core', x5, y, cfg.l2x2, cfg.w2x2)

  tail(x1 - 5, y - inport * cfg.d2x2, 90, 90, inport, 1)
  
  if outport == 0:
    x7, _ = taper(x6, y1, 1)
    x7, _ = taper(x6, y2, 1)
  else:
    x7, _ = taper(x6, y4, 1)
    tail(x6 + 5, y + outport * cfg.d2x2, 90, 270, outport, -1)
  
  dxf.srect('edge', x, y, x7 - x, cfg.w2x2 + cfg.eg)

  return x7, y1, y2

def device(x, y):

  ch = 50

  x3, y31, y32 = mzi(x, y + cfg.d2x2, -1, 0)

  x4, y41 = dev.sbend(x3, y31, ch, 20, 0,  1)
  x4, y42 = dev.sbend(x3, y32, ch, 20, 0, -1)
  x5, _, y51 = mzi(x4, y41 - cfg.d2x2, 1,  1)
  x5, y52, _ = mzi(x4, y42 - cfg.d2x2, 1, -1)

  return x5, y51, y52

def chip(x, y, lchip):

  ch = 50

  idev = len(cfg.data)
  x1, _, _ = device(x, y)
  x2, ltip = dev.move(idev, x, x1, lchip)

  _ , _, t3 = tip.fiber(x, y, ltip, -1)
  x4, _, t4 = tip.fiber(x2, y + ch, ltip, 1)
  x4, _, t4 = tip.fiber(x2, y - ch, ltip, 1)

  s = 'pbs-' + str(round(cfg.lpbs,1))
  dev.texts(t3, y - ch, s, 0.5, 'lc')
  dev.texts(t3, y + ch, s, 0.5, 'lc')
  dev.texts(t4, y, s, 0.5, 'rc')
  print(s, int(x4 - x))

  return x4, y + ysize

def chips(x, y, arange):

  var = cfg.lpbs

  for cfg.lpbs in arange: _, y = chip(x, y, xsize)

  cfg.lpbs = var

  return x + xsize, y - cfg.ch * 1.5

if __name__ == '__main__':

  # chip(0, 0, 3000)

  chips(0, 0, dev.arange(20, 58, 2))

  dev.saveas(cfg.work + 'pbs')