import cfg
import dxf
import dev

ltip = 800
lcut = 400

xsize = cfg.size
ysize = 100

def device(x, y, lchip, wtip, sign):
  
  lext = lchip - ltip

  w = [wtip, 0.5, 0.8, cfg.wg]
  l = [ltip - 75, 50, 20, 5]

  if sign < 0:
    x1, y = dev.srect(x,  y, l[0], w[0])
    x2, y = dev.taper(x1, y, l[1], w[0], w[1])
    x3, y = dev.taper(x2, y, l[2], w[1], w[2])
    x4, y = dev.taper(x3, y, l[3], w[2], w[3])
    if lext > 0: x5, y = dev.sline(x4, y, lext)
    else: x5 = x4
  else:
    if lext > 0: x1, _ = dev.sline(x, y, lext)
    else: x1 = x
    x2, y = dev.taper(x1, y, l[3], w[3], w[2])
    x3, y = dev.taper(x2, y, l[2], w[2], w[1])
    x4, y = dev.taper(x3, y, l[1], w[1], w[0])
    x5, y = dev.srect(x4, y, l[0], w[0])

  return x5, y, x4 if sign < 0 else x1

def fiber(x, y, lchip, sign):

  return device(x, y, lchip, 0.36, sign)

def pd(x, y, lchip, sign):

  return device(x, y, lchip, 0.36, sign)

def scuts(x, y):

  t = ltip - 600 + 2.5
  w = cfg.size

  dxf.crect('recs', x + t, y, x + t + 2.5, y + w)
  dxf.crect('recs', x - t + w, y, x - t + w - 2.5, y + w)

  s = t + 5.5

  dxf.crect('edge', x + s, y, x + s + 54, y + w)
  dxf.crect('edge', x - s + w, y, x - s + w - 54, y + w)
  
  s = t - 57

  dxf.crect('edge', x + s, y, x + s + 54, y + w)
  dxf.crect('edge', x - s + w, y, x - s + w - 54, y + w)
  
def sline(x, y, lchip):

  wtip = 0.36

  x1, _, _ = device(x, y, 0, wtip, -1)
  x1, _, _ = device(x1, y, lchip - x1 + x, wtip, 1)

def chip(x, y, lchip, wtip):

  x1, _, _ = device(x, y, 0, wtip, -1)
  x2, _, _ = device(x1, y, lchip - x1 + x, wtip, 1)

  s = 'tip-' + str(round(wtip, 6))
  dev.texts(x  + ltip, y - 50, s, 0.5, 'lc')
  dev.texts(x2 - ltip, y - 50, s, 0.5, 'rc')
  print(s, int(x2 - x))

  return x2, y + ysize

def chips(x, y, arange):
  
  for w in arange: x1, y = chip(x, y, xsize, w)

  return x1, y

if __name__ == '__main__':

  # chip(0, 0, 0)

  chips(0, 0, dev.arange(0.2, 0.4, 0.05))

  dev.saveas(cfg.work + 'tip')