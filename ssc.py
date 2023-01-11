import cfg
import dxf
import dev
import tip

def device(x, y, ltip, ltaper, sign):
  
  w = [cfg.wg, 0.5, 0.1]
  l = [ltip - tip.polished, 50, ltaper]
  t = l[0] - sum(l[1:])

  if t > 0: x, _ = dev.sline(x, y, t * sign)
  x1, _ = dxf.taper('core', x,  y, sign * l[1], w[0], w[1])
  x2, _ = dxf.taper('core', x1, y, sign * l[2], w[1], w[2])
  x3, _ = dev.srect(x2, y, sign * tip.polished, w[2])

  dxf.srect('edge', x, y, x2 - x, cfg.eg)
  dxf.srect('sio2', x, y, x2 - x, cfg.sg)

  return x2, x

def chip(x, y, lchip, ltaper):

  idev = len(cfg.data)
  x1, _ = dev.sline(x, y, 1000)
  x2, x3, ltip = dev.center(idev, x, x1, lchip)

  x4, t1 = device(x2, y, ltip, ltaper, -1)
  x5, t2 = device(x3, y, ltip, ltaper,  1)

  s = 'sio-' + str(round(ltaper))
  dev.texts(t1, y - 50, s, 0.2, 'lc')
  dev.texts(t2, y - 50, s, 0.2, 'rc')
  print(s, round(x3 - x2), round(x5 - x4))

  return x + lchip, y

def chips(x, y, arange):
  
  y = y - cfg.sch

  for ltaper in arange: _, y = chip(x, y + cfg.sch, cfg.size, ltaper)

  return x + cfg.size, y

if __name__ == '__main__':

  # chip(0, 0, 1000, 500)

  chips(0, 0, dev.arange(500, 900, 100))

  dev.saveas(cfg.work + 'ssc')