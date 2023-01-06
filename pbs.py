import cfg
import dxf
import dev
import cir
import tip
import elr

xsize = cfg.size
ysize = 200

def taper(x, y, sign):

  w1 = cfg.wt if sign < 0 else cfg.wtpr
  w2 = cfg.wtpr if sign < 0 else cfg.wt

  if sign < 0:
    x, _ = dxf.taper('core', x, y, 5, cfg.wg, cfg.wt)
    x, _ = dxf.srect('core', x, y, 40, cfg.wt)
  x, _ = dxf.taper('core', x, y, cfg.ltpr, w1, w2)

  return x, y

def arm(x, y, sign):

  angle, dy, ltaper = 2, 1, 10

  core = elr.update(cfg.wt, cfg.radius, angle)

  x1, _ = dxf.taper('core', x, y, cfg.ltpr, cfg.wtpr, cfg.wt)
  x2, y2 = dxf.sbend('core', x1, y, core, angle, -dy * sign)
  x3, y2 = dxf.taper('core', x2, y2, ltaper, cfg.wt, cfg.wpbs)
  
  if sign > 0: x3, _ = dxf.srect('core', x3, y2, cfg.lpbs, cfg.wpbs)
  
  x4, _ = dxf.taper('core', x3, y2, ltaper, cfg.wpbs, cfg.wt)
  if sign < 0: x4, _ = dxf.srect('core', x4, y2, cfg.lpbs, cfg.wt)
  x5, _ = dxf.sbend('core', x4, y2, core, angle, dy * sign)
  x6, _ = dxf.taper('core', x5, y, cfg.ltpr, cfg.wt, cfg.wtpr)

  return x6, y

def tail(x, y, angle, rotate, port, sign):

  core = cir.update(cfg.wt, 5, angle)

  x1, y1 = dxf.taper('core', x, y, sign * cfg.ltpr, cfg.wt, cfg.wtpr)
  x1, y1 = dxf.bends('core', x, y, core, rotate, 1, port)

  w = cfg.wt * 0.5
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

  if outport == 0: x1, _ = taper(x, y3, -1)
  else: x1, _ = dxf.taper('core', x, y3, cfg.ltpr, cfg.wt, cfg.wtpr)
  x2, _ = dxf.srect('core', x1, y, cfg.l2x2, cfg.w2x2)

  x5, _ = arm(x2, y1, -1)
  x5, _ = arm(x2, y2,  1)

  x6, _ = dxf.srect('core', x5, y, cfg.l2x2, cfg.w2x2)

  tail(x1 - 5, y - inport * cfg.d2x2, 90, 90, inport, 1)
  
  if outport == 0:
    x7, _ = taper(x6, y1, 1)
    x7, _ = taper(x6, y2, 1)
  else:
    x7, _ = taper(x6, y4, 1)
    x7, _ = dxf.srect('core', x7, y4, 40, cfg.wt)
    x7, _ = dxf.taper('core', x7, y4, cfg.ltpr, cfg.wt, cfg.wg)
    tail(x6 + 5, y + outport * cfg.d2x2, 90, 270, outport, -1)
  
  dxf.srect('edge', x, y, x7 - x, cfg.w2x2 + cfg.eg)
  dxf.srect('sio2', x, y, x7 - x, cfg.w2x2 + cfg.eg)

  return x7, y1, y2

def sbend(x, y, dy):

  radius, angle = 100, 10

  core = elr.update(cfg.wt, radius, angle)
  edge = elr.update(cfg.eg, radius, angle)
  sio2 = elr.update(cfg.sg, radius, angle)

  x1, y1 = dxf.sbend('edge', x, y, edge, angle, dy)
  x1, y1 = dxf.sbend('core', x, y, core, angle, dy)
  x1, y1 = dxf.sbend('sio2', x, y, sio2, angle, dy)

  return x1, y1

def device(x, y):

  ch = 50

  x3, y31, y32 = mzi(x, y + cfg.d2x2, -1, 0)
  x4, y41 = sbend(x3, y31,  ch)
  x4, y42 = sbend(x3, y32, -ch)
  x5, _, y51 = mzi(x4, y41 - cfg.d2x2, 1,  1)
  x5, y52, _ = mzi(x4, y42 - cfg.d2x2, 1, -1)

  return x5, y51, y52

def chip(x, y, lchip):

  ch = 50

  idev = len(cfg.data)
  x1, _, _ = device(x, y)
  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y, ltip, -1)
  x8, t2 = tip.fiber(x6, y + ch, ltip, 1)
  x8, t2 = tip.fiber(x6, y - ch, ltip, 1)

  s = 'pbs-' + str(round(cfg.lpbs))
  dev.texts(t1, y - ch, s, 0.2, 'lc')
  dev.texts(t1, y + ch, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y + ysize

def chips(x, y, arange):

  var = cfg.lpbs
  for cfg.lpbs in arange: _, y = chip(x, y, xsize)
  cfg.lpbs = var

  return x + xsize, y - cfg.ch * 1.5

if __name__ == '__main__':

  chip(0, 0, 3000)

  # chips(0, 0, dev.arange(20, 58, 2))

  dev.saveas(cfg.work + 'pbs')