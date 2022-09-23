import cfg
import dxf
import dev

ltip = 800
lcut = 400

xsize = cfg.size
ysize = cfg.ch

def device(x, y, lchip, wtip, sign):
  
  lext = lchip - ltip
  wext = 125

  w = [wtip, 0.5, 0.8, cfg.wg]
  l = [50, 20, 5]
  t = sum(l)
  l.insert(0, ltip - t)

  if sign < 0:
    x1, y = dxf.srect('core', x,  y, l[0], w[0])
    x1, y = dxf.srect('edge', x,  y, l[0], wext)
    x2, y = dxf.taper('core', x1, y, l[1], w[0], w[1])
    x3, y = dxf.taper('core', x2, y, l[2], w[1], w[2])
    x4, y = dxf.taper('core', x3, y, l[3], w[2], w[3])
    x4, y = dxf.taper('edge', x1, y, t, wext, cfg.eg)
    if lext > 0: x5, y = dev.sline(x4, y, lext)
    else: x5 = x4
  else:
    if lext > 0: x1, _ = dev.sline(x, y, lext)
    else: x1 = x
    x2, y = dxf.taper('core', x1, y, l[3], w[3], w[2])
    x3, y = dxf.taper('core', x2, y, l[2], w[2], w[1])
    x4, y = dxf.taper('core', x3, y, l[1], w[1], w[0])
    x4, y = dxf.taper('edge', x1, y, t, cfg.eg, wext)
    x5, y = dxf.srect('core', x4, y, l[0], w[0])
    x5, y = dxf.srect('edge', x4, y, l[0], wext)

  return x5, y, x4 if sign < 0 else x1

def fiber(x, y, lchip, sign):

  return device(x, y, lchip, 0.36, sign)

def pd(x, y, lchip, sign):

  return device(x, y, lchip, 0.36, sign)

def scuts(x, y):

  t = (ltip + 12.5) * 0.5
  w = cfg.size

  for i in [t - j for j in [0, 100, 200, 300]]:
    dxf.srect('cuts', x + i - 1, y + w * 0.5, 2, w)
    dxf.srect('tops', x + i - 20, y + w * 0.5, 40, w)
    dxf.srect('cuts', x + w - i - 1, y + w * 0.5, 2, w)
    dxf.srect('tops', x + w - i - 20, y + w * 0.5, 40, w)

def sline(x, y, lchip):

  wtip = 0.36

  x1, _, _ = device(x, y, 0, wtip, -1)
  x1, _, _ = device(x1, y, lchip - x1 + x, wtip, 1)

def chip(x, y, lchip, wtip):

  x1, _, _ = device(x, y, 0, wtip, -1)
  x2, _, _ = device(x1, y, lchip - x1 + x, wtip, 1)

  s = 'tip-' + str(round(wtip, 6))
  dev.texts(x  + ltip, y - cfg.ch * 0.5, s, 0.5, 'lc')
  dev.texts(x2 - ltip, y - cfg.ch * 0.5, s, 0.5, 'rc')
  print(s, int(x2 - x))

  return x2, y

def chips(x, y, arange):
  
  for w in arange: x1, y = chip(x, y + cfg.ch, xsize, w)

  return x1, y

if __name__ == '__main__':

  # chip(0, 0, 0)

  chips(0, 0, dev.arange(0.2, 0.4, 0.05))

  dev.saveas('tip')