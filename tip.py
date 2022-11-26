import cfg
import dxf
import dev

lcut = 400

xsize = cfg.size
ysize = 100

def device(x, y, ltip, wtip, sign):
  
  w = [cfg.wg, 0.8, 0.5, wtip]
  l = [ltip, 5, 20, 50, 800]
  t = l[0] - sum(l[1:])

  if t > 0: x, _ = dev.sline(x, y, t * sign)
  x1, _ = dxf.taper('core', x,  y, sign * l[1], w[0], w[1])
  x2, _ = dxf.taper('core', x1, y, sign * l[2], w[1], w[2])
  x3, _ = dxf.taper('core', x2, y, sign * l[3], w[2], w[3])
  x4, _ = dxf.srect('core', x3, y, sign * l[4], w[3])

  dxf.srect('edge', x, y, x4 - x, cfg.eg)
  
  return x4, x

def fiber(x, y, ltip, sign):

  return device(x, y, ltip, 0.36, sign)

def diode(x, y, ltip, sign):

  return device(x, y, ltip, 0.36, sign)

def scuts(x, y):

  t, w, d = 200, cfg.size, 1

  dxf.srect('edge', x + t - d, y + w * 0.5, d * 2, w)
  dxf.srect('edge', x - t - d + w, y + w * 0.5, d * 2, w)
  
def sline(x, y, lchip):

  wtip = 0.36

  x1, _ = device(x, y, 0, wtip, -1)
  x1, _ = device(x1, y, lchip - x1 + x, wtip, 1)

def chip(x, y, lchip, wtip):

  idev = len(cfg.data)
  x1, _ = dev.sline(x, y, 1000)
  x2, x3, ltip = dev.xshift(idev, x, x1, lchip)

  x4, t1 = device(x2, y, ltip, wtip, -1)
  x5, t2 = device(x3, y, ltip, wtip,  1)

  s = 'tip-' + str(round(wtip, 6))
  dev.texts(t1, y - 50, s, 0.2, 'lc')
  dev.texts(t2, y - 50, s, 0.2, 'rc')
  print(s, int(x3 - x2), int(x5 - x4))

  return x2, y + ysize

def chips(x, y, arange):
  
  for w in arange: x1, y = chip(x, y, xsize, w)

  return x1, y

if __name__ == '__main__':

  # chip(0, 0, 0)

  chips(0, 0, dev.arange(0.2, 0.4, 0.05))

  dev.saveas(cfg.work + 'tip')