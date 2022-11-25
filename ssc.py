import cfg
import dev

xsize = cfg.size
ysize = 100

def device(x, y, lchip, ldev, ltaper, sign):
  
  w = [0.1, 0.5, 0.8, cfg.wg]
  l = [ltaper, 50, 25, (lchip - ldev) * 0.5 - ltaper - 75]

  x1 = x if sign > 0 else x + lchip

  x2, y = dev.taper(x1, y, sign * l[0], w[0], w[1])
  x3, y = dev.taper(x2, y, sign * l[1], w[1], w[2])
  x4, y = dev.taper(x3, y, sign * l[2], w[2], w[3])
  
  if l[3] > 0: dev.sline(x4, y, sign * l[3])

  return x4, y

def chip(x, y, lchip, ltaper):

  ldev = 1000

  dev.sline(x + (lchip - ldev) * 0.5, y, ldev)

  x1, _ = device(x, y, lchip, ldev, ltaper,  1)
  x2, _ = device(x, y, lchip, ldev, ltaper, -1)

  s = 'sio-' + str(int(ltaper))
  dev.texts(x1, y - 50, s, 0.2, 'lc')
  dev.texts(x2, y - 50, s, 0.2, 'rc')
  print(s)

  return x + lchip, y + ysize

def chips(x, y, arange):
  
  for ltaper in arange: x1, y = chip(x, y, xsize, ltaper)

  return x1, y

if __name__ == '__main__':

  # chip(0, 0, 0)

  chips(0, 0, dev.arange(500, 900, 100))

  dev.saveas(cfg.work + 'sio')