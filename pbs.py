import cfg
import dxf
import dev
import cir
import tip
import elr

def sbend(x, y, dy):

  radius, angle = 100, 10

  core = elr.update(cfg.wg, radius, angle)
  edge = elr.update(cfg.eg, radius, angle)
  sio2 = elr.update(cfg.sg, radius, angle)

  x1, y1 = dxf.sbend('edge', x, y, edge, angle, dy)
  x1, y1 = dxf.sbend('core', x, y, core, angle, dy)
  x1, y1 = dxf.sbend('sio2', x, y, sio2, angle, dy)

  return x1, y1

def arm(x, y, sign):

  wg = 1.2 if sign > 0 else cfg.wpbs

  angle, dy, ltaper = 2, 1, 10
  core = elr.update(cfg.wg, cfg.radius, angle)

  x1, y1 = dxf.taper('core', x, y, cfg.ltpr, cfg.wtpr, cfg.wg)
  x2, y2 = dxf.sbend('core', x1, y1, core, angle, dy * sign)
  x3, y2 = dxf.taper('core', x2, y2, ltaper, cfg.wg, wg)
  x3, y2 = dxf.srect('core', x3, y2, cfg.lpbs, wg)
  x4, y2 = dxf.taper('core', x3, y2, ltaper, wg, cfg.wg)
  x5, y1 = dxf.sbend('core', x4, y2, core, angle, -dy * sign)
  x6, y1 = dxf.taper('core', x5, y1, cfg.ltpr, cfg.wg, cfg.wtpr)

  return x6, y

def tail(x, y, angle, rotate, port, sign):

  core = cir.update(cfg.wg, 5, angle)

  x1, y1 = dxf.taper('core', x, y, sign * cfg.ltpr, cfg.wg, cfg.wtpr)
  x1, y1 = dxf.bends('core', x, y, core, rotate, 1, port)

  w = cfg.wg * 0.5
  s = 1 if rotate != 90 else -1

  data = ['core']
  data.append([x1 + w, y1])
  data.append([x1, y1 + s * port * 5])
  data.append([x1 - w, y1])
  cfg.data.append(data)

  return x1, y1

def mzi(x, y, inport, outport):

  y1 = y + cfg.d2x2
  y2 = y - cfg.d2x2
  y3 = y + inport * cfg.d2x2
  y4 = y - outport * cfg.d2x2

  x1, _ = dxf.srect('core', x, y3, 40, cfg.wg)
  x1, _ = dxf.taper('core', x1, y3, cfg.ltpr, cfg.wg, cfg.wtpr)
  
  tail(x1 - 5, y - inport * cfg.d2x2, 90, 90, inport, 1)
  
  x2, _ = dxf.srect('core', x1, y, cfg.l2x2, cfg.w2x2)

  x5, _ = arm(x2, y1,  1)
  x5, _ = arm(x2, y2, -1)

  x6, _ = dxf.srect('core', x5, y, cfg.l2x2, cfg.w2x2)
  x7, _ = dxf.taper('core', x6, y1, cfg.ltpr, cfg.wtpr, cfg.wg)
  x7, _ = dxf.taper('core', x6, y2, cfg.ltpr, cfg.wtpr, cfg.wg)

  if outport != 0:
    x7, _ = dxf.srect('core', x7, y4, 40, cfg.wg)
    tail(x6 + 5, y + outport * cfg.d2x2, 90, 270, outport, -1)
  
  dxf.srect('edge', x, y, x7 - x, cfg.w2x2 + cfg.eg)
  dxf.srect('sio2', x, y, x7 - x, cfg.w2x2 + cfg.eg)

  return x7, y1, y2

def device(x, y):

  ch = cfg.sch * 0.5

  x3, y31, y32 = mzi(x, y + cfg.d2x2, -1, 0)
  x4, y41 = sbend(x3, y31,  ch)
  x4, y42 = sbend(x3, y32, -ch)
  x5, _, y51 = mzi(x4, y41 - cfg.d2x2, 1,  1)
  x5, y52, _ = mzi(x4, y42 - cfg.d2x2, 1, -1)

  return x5, y51, y52

def chip(x, y, lchip):

  ch = cfg.sch * 0.5

  idev = len(cfg.data)
  x1, _, _ = device(x, y)
  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y, ltip, -1)
  x8, t2 = tip.fiber(x6, y + ch, ltip, 1)
  x8, t2 = tip.fiber(x6, y - ch, ltip, 1)

  s = 'pbs-' + str(round(cfg.l2x2)) + '-' + str(round(cfg.lpbs))
  dev.texts(t1, y - ch, s, 0.2, 'lc')
  dev.texts(t1, y + ch, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  y = y - cfg.sch * 1.5

  lpbs = cfg.lpbs
  l2x2 = cfg.l2x2

  for cfg.lpbs in arange: _, y = chip(x, y + cfg.sch * 2, cfg.size)

  for cfg.l2x2 in [49, 51, 52]:
    for cfg.lpbs in dev.arange(24, 40, 2): _, y = chip(x, y + cfg.sch * 2, cfg.size)

  cfg.lpbs = lpbs
  cfg.l2x2 = l2x2

  return x + cfg.size, y - cfg.sch * 0.5

if __name__ == '__main__':

  # chip(0, 0, 3000)

  chips(0, 0, dev.arange(20, 30, 2))

  dev.saveas(cfg.work + 'pbs')