import cfg
import dxf
import dev

wbar = 250
wkey = 400
lbar = cfg.mask - wbar
lkey = cfg.mask - wbar * 2
xorg = wbar + wkey
yorg = wbar + wkey

def cross(x, y):

  data = ['keys']

  data.append([x - lbar, y + wbar])
  data.append([x - wbar, y + wbar])
  data.append([x - wbar, y + lbar])
  data.append([x + wbar, y + lbar])
  data.append([x + wbar, y + wbar])
  data.append([x + lbar, y + wbar])

  data.append([x + lbar, y - wbar])
  data.append([x + wbar, y - wbar])
  data.append([x + wbar, y - lbar])
  data.append([x - wbar, y - lbar])
  data.append([x - wbar, y - wbar])
  data.append([x - lbar, y - wbar])

  cfg.data.append(data)

def bars(x, y):

  data = ['bars']

  data.append([x, y])
  data.append([x, y + lkey])
  data.append([x + wkey, y + lkey])
  data.append([x + wkey, y + wkey])
  data.append([x + lkey, y + wkey])
  data.append([x + lkey, y])

  cfg.data.append(data)

def xrect(layer, x, y, l, w, t, m):

  for i in range(m):
    xp = x + i * t
    dxf.crect(layer, xp, y, xp + l, y + w)

def yrect(layer, x, y, l, w, t, m):

  for i in range(m):
    yp = y + i * t
    dxf.crect(layer, x, yp, x + l, yp + w)

def key1(layer, x, y, align):

  xp = x + (align - 1) * 1100
  yp = y

  for i in [488, 508, 534, 938]:
    yrect(layer, xp + i, yp + 69, 4, 4, 8, 7)

  for i in [67, 93, 113]:
    xrect(layer, xp + 583.5, yp + i, 3, 4, 6, 51)

  xrect(layer, xp + 1014, yp + 93, 4, 4, 8, 7)
  xrect(layer, xp + 1145, yp + 60, 4, 70, 8, 13)
  yrect(layer, xp + 1315, yp + 45, 70, 4, 8, 13)

def key2(layer, x, y, quadrant):

  xp = x + 5060
  yp = y + 200
  
  dxf.crect('hole', xp, yp, xp + 340, yp + 50)

  xp = xp + 0.25
  yp = yp + 25

  dxf.srect(layer, xp + 302, yp, 20, 20)
  dxf.texts(layer, xp + 242, yp, '0' + str(quadrant), 0.2, 'lc')

  l, s, t = 10, 7.5, 2.5

  for i in range(1, 7):

    w = i * 0.5
    s = s + (i - 1) * 4.5 + 20

    for j in range(0, 10, 2): dxf.srect(layer, xp + s + w * j, yp - 5, w, l)
    
    dxf.srect(layer, xp + s + w * 2, yp - 5 + l, w, l)
    dxf.srect(layer, xp + s + w * 7, yp - 5 + l, w, l)

    t = t + (i - 1) * 4.5 + 20

    idev = len(cfg.data)
    dxf.texts(layer, xp, yp, str(w), 0.05, 'lb')
    dxf.move(idev, xp, yp, 0, 0, t, -10, 90)

def key3(layer, x, y):

  dxf.crect('hole', x, y, x + 340, y + 100)

  dxf.srect(layer, x + 37.5, y + 65, 10, 10)

  for i in range(11):
    dxf.srect(layer, x + 15 + i * 5.2, y + 22.5, 3, 10)
    dxf.srect(layer, x + 80, y + i * 5.2 + 39, 10, 3)
  
  for i in range(21): dxf.srect(layer, x + 119 + i * 5, y + 70, 2, 40)

  dxf.srect(layer, x + 257.5, y + 65, 20, 20)

  for i in range(11):
    w = 10 if i % 5 == 0 else 8
    dxf.srect(layer, x + 240.4 + i * 5.1, y + 17.5 - w * 0.5, 3.2, w)
    dxf.srect(layer, x + 315, y + 39.5 + i * 5.1, w, 3.2)

def frame(quadrant, align):
  
  xp = wbar - (quadrant % 2) * (wbar + lbar)
  yp = wbar if quadrant < 3 else -lbar

  bars(xp, yp)

  key1('hole', xp, yp, align)
  key2('keys', xp, yp, quadrant)
  key3('keys', xp + 7815, yp + 150)

  x4, y4 = 8750, 150
  x5, y5 = 8950, 100
  x6, y6 = 9900, 150

  dxf.crect('hole', xp + x4, yp + y4, xp + x4 + 100, yp + y4 + 100)
  dxf.crect('hole', xp + x5, yp + y5, xp + x5 + 100, yp + y5 + 200)
  dxf.crect('hole', xp + x6, yp + y6, xp + x6 + 200, yp + y6 + 100)
  dxf.srect('keys', xp + x6 + 50, yp + y6 + 50, 10, 80)
  dxf.srect('keys', xp + x6 + 100, yp + y6 + 50, 5, 80)
  dxf.srect('keys', xp + x6 + 150, yp + y6 + 50, 1, 80)

  idev = len(cfg.data)
  key1('hole', xp, yp, 1)
  dxf.move(idev, xp, yp, 0, 0, 0, align * 1100 + 800, 270)

  idev = len(cfg.data)
  key2('keys', xp, yp, quadrant)
  dxf.move(idev, xp, yp, 0, 0, 400, 0, 90)

def contact_align_key(layer, x, y, scale, sign):

  for i in [0, 1, 3, 4, 5]:
    x1, y1 = x + (70 + 260 * i) * scale, y + 130 * scale
    x2, y2 = x + 590 * scale, y + (690 - 260 * i) * scale

    l, w = 120 * scale, 28 * scale
    x3 = x1 if sign > 0 else x2
    y3 = y1 if sign > 0 else y2 - 40 * scale
    dxf.srect(layer, x3, y3, l, w)
    dxf.srect(layer, x3 + 46 * scale, y3, w, l)

    l, d = 40 * scale, 80 * scale
    x4 = x2 if sign > 0 else x1
    y4 = y2 if sign > 0 else y1 + 40 * scale
    dxf.srect(layer, x4, y4, l, l)
    dxf.srect(layer, x4 + d, y4, l, l)
    dxf.srect(layer, x4, y4 - d, l, l)
    dxf.srect(layer, x4 + d, y4 - d, l, l)

  return x, y

def contact_align_keys(layer, x, y, sign):

  xo = x + cfg.size * 0.5
  yo = y + cfg.size * 0.5

  for i in range(4):

    idev = len(cfg.data)
    
    xt, rt = xo + 1300, 1
    
    for _ in range(4):
      contact_align_key(layer, xt, yo, rt, sign)
      xt = xt + 1820 * rt
      rt = rt * 0.5
    
    dxf.move(idev, xo, yo, 0, 0, 0, 0, 90 * i)
  
  dxf.srect(layer, x, yo, cfg.size, 5)

  print('Contact Align Keys')

if __name__ == '__main__':

  # cross(0, 0)

  # frame(1, 1)
  # frame(2, 1)
  # frame(3, 2)
  # frame(4, 3)

  # dev.saveas(cfg.work + 'key')

  cfg.layer['core'] = 4
  cfg.layer['edge'] = 4

  contact_align_keys('core', 0, 0,  1)
  contact_align_keys('hole', 0, 0, -1)

  dev.saveas(cfg.work + 'key')
