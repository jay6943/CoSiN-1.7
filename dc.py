import cfg
import dxf
import dev
import numpy as np
import euler as elr

xsize = cfg.size
ysize = 200

def device(x, y, sign):

  wg, radius, angle = 0.38, 50, 3

  df = elr.update(wg, radius, angle, cfg.draft)
  af = elr.update(cfg.wg, cfg.radius, 45 - angle, cfg.draft)
  bf = elr.update(cfg.wg, cfg.radius, 45, cfg.draft)

  # x1, y1 = dxf.taper('core', x, y, 100, cfg.wg, wg)
  # x2, y2 = dxf.tilts('core', x1, y1, 50, wg, -angle * sign)
  # x3, y3 = dxf.bends('core', x2 + df['dx'], y2, df, 180, -sign)
  # x4, y4 = dxf.srect('core', x3 + df['dx'], y2, 19, wg)


  x1, y1 = dxf.bends('core', x, y, df, 0, sign)
  idev = len(cfg.data)
  x2, y2 = dxf.taper('core', x1, y1, 100, wg, cfg.wg)
  x3, y3 = dxf.move(idev, x1, y1, x2, y2, 0, 0, angle * sign)
  x4, y4 = dxf.bends('core', x3, y3, af, 0, sign)
  x5, y5 = dxf.bends('core', x4, y4, bf, 315, -sign)
  dxf.sbend('edge', x5, y5, 0, bf, 180, sign)

  return x5, y5

def chip(x, y, lchip):

  dy = 2

  x1, y1 = device(x, y + dy,  1)
  x2, y2 = device(x, y - dy, -1)

def chips(x, y, arange):

  var = cfg.l2x2

  for cfg.l2x2 in arange: _, y = chip(x, y, xsize)

  cfg.l2x2 = var

  return x + xsize, y

def test(x, y):

  df = elr.update(cfg.wg, cfg.radius, 45, cfg.draft)
  dxf.sbend('core', x, y, 0, df, 0, 1)

  cf = elr.curve(cfg.wg, cfg.radius, 45, 200)
  xt, yt = cf['x'] + x, cf['y'] + y

  xp, yp = xt + x, yt + y
  data = np.array([xp, yp]).transpose()
  cfg.data.append(['edge'] + data.tolist())

  xp, yp = xp + cf['xo'], yp + cf['yo']
  data = np.array([xp, yp]).transpose()
  cfg.data.append(['edge'] + data.tolist())

  n = cf['n']
  for i in range(n):
    xp[i] = xt[n - 1 - i]
    xp[i+n] = xt[2 * n - i]
  data = np.array([xp, yp]).transpose()
  cfg.data.append(['edge'] + data.tolist())

if __name__ == '__main__':

  # chip(0, 0, xsize)
  # chips(0, 0, dev.arange(49, 53, 1))

  test(0, 0)
  
  dev.saveas(cfg.work + 'dc')