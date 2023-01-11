import cfg
import dxf
import dev
import dci
import elr
import tip

def sbend(x, y, angle, dy):

  x1, y1 = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wr)
  x2, y2 = dev.sbend(x1, y1, angle, dy)
  x3, y3 = dev.taper(x2, y2, cfg.ltpr, cfg.wr, cfg.wg)

  return x3, y3

def ybend(x, y, dy):

  angle = 4
  core = elr.update(dci.wg, dci.radius, angle)
  sio2 = elr.update(cfg.sg, dci.radius, angle)

  x1, y1 = dxf.sbend('core', x, y, core, angle, dy)
  x1, y1 = dxf.sbend('sio2', x, y, sio2, angle, dy)

  return x1, y1

def arm(x, y, ch, sign):

  wdc, ltaper = 0.8, 5

  x1, y1 = ybend(x, y + cfg.spacing * sign, ch * sign)
  x2, y2 = dxf.taper('core', x1, y1, ltaper, dci.wg, wdc)
  if sign > 0: x2, y2 = dxf.srect('core', x2, y2, cfg.lpbs, wdc)
  x3, y3 = dxf.taper('core', x2, y2, ltaper, wdc, dci.wg)
  if sign < 0: x3, y3 = dxf.srect('core', x3, y3, cfg.lpbs, dci.wg)
  x4, y4 = ybend(x3, y3, -ch * sign)

  return x4, y4

def mzi(x, y, ch, sign):

  ch = 1.5

  x1, y1 = arm(x, y, ch, sign)
  x2, y2 = ybend(x1, y1,  ch * 2 * sign)
  x3, y4 = arm(x2, y2 + cfg.spacing * sign, ch,  1)
  x3, y5 = arm(x2, y2 + cfg.spacing * sign, ch, -1)
  x4, y6 = ybend(x3, y4,  ch)
  x5, y7 = ybend(x3, y5, -ch)
  x5, y7 = ybend(x4, y6, -cfg.spacing - ch)

  ybend(x1, y2 + (cfg.spacing * 2 + ch * 2) * sign, -ch * 2 * sign)

  return x5, y7

def device(x, y):

  ch = 1.5

  x2, y1 = dci.dc(x, y, -1,  1)
  x2, y2 = dci.dc(x, y, -1, -1)
  x3, y1 = mzi(x2, y, ch,  1)
  x3, y2 = mzi(x2, y, ch, -1)
  x4, y1 = dxf.taper('core', x3, y1, 50, 0.4, cfg.wg)
  x4, y2 = dxf.taper('core', x3, y2, 50, 0.4, cfg.wg)

  dxf.srect('edge', x2, y, x4 - x2, 40)

  return x4, y1, y2

def chip(x, y, lchip):
  
  angle, ch = 20, cfg.sch * 0.5

  y1 = y + ch
  y2 = y - ch

  idev = len(cfg.data)

  x1, _ = dci.sbend(x, y1, angle, ch - dci.offset, -1, -1)
  x1, _ = dci.sbend(x, y2, angle, ch - dci.offset, -1,  1)
  x2, y3, y4 = device(x1, y)
  x3, y5 = sbend(x2, y3, angle, y + ch - y3)
  x4, y6 = sbend(x2, y4, angle, y - ch - y4)

  x5, x6, ltip = dev.center(idev, x, x4, lchip)

  x7, t1 = tip.fiber(x5, y1, ltip, -1)
  x7, t1 = tip.fiber(x5, y2, ltip, -1)
  x8, t2 = tip.fiber(x6, y1, ltip, 1)
  x8, t2 = tip.fiber(x6, y2, ltip, 1)

  s = 'pbs-dc-' + str(round(cfg.lpbs, 2))
  dev.texts(t1, y, s, 0.2, 'lc')
  dev.texts(t2, y, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  y = y - cfg.sch * 1.5

  var = cfg.lpbs
  for cfg.lpbs in arange: _, y = chip(x, y + cfg.sch * 2, cfg.size)
  cfg.lpbs = var

  return x + cfg.size, y - cfg.sch * 0.5

if __name__ == '__main__':

  # chip(0, 0, 2500)

  chips(0, 0, dev.arange(10, 20, 1))

  dev.saveas(cfg.work + 'pdc')