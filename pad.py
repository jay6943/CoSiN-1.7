import cfg
import dxf
import dev
import numpy as np

xaxis = 200
yaxis = 100

def line(w1, w2, sign):

  a = xaxis + sign * w1 * 0.5
  b = yaxis + sign * w2 * 0.5

  xp = np.log10(np.linspace(1, 10, 40)) * a
  if sign < 0: xp = xp[::-1]
  yp = np.sqrt(b * b * (1 - xp * xp / (a * a)))

  return xp, yaxis - yp

def wire(layer, x, y, w1, w2, xsign, ysign):
  
  radius = 100

  x1, y1 = line(w1, w2,  1)
  x2, y2 = line(w1, w2, -1)

  if layer == 'gold':
    t = (np.linspace(0, 320, 33) - 70) * np.pi / 180
  else:
    t = (np.linspace(0, 320, 33) - 72) * np.pi / 180
    x1, y1 = x1[:-4], y1[:-4]
    x2, y2 = x2[4: ], y2[4: ]

  r = 0 if layer == 'gold' else cfg.eg

  x3 = (radius + r) * np.cos(t) + xaxis
  y3 = (radius + r) * np.sin(t) + yaxis + radius

  x1, y1 = x + xsign * x1, y + ysign * y1
  x2, y2 = x + xsign * x2, y + ysign * y2
  x3, y3 = x + xsign * x3, y + ysign * y3

  xp = x1.tolist() + x3.tolist() + x2.tolist()
  yp = y1.tolist() + y3.tolist() + y2.tolist()

  data = np.array([xp, yp]).transpose()
  cfg.data.append([layer] + data.tolist())

  return x + xaxis, y + yaxis

def electrode(layer, x, y, length, width, sign):

  w = 50 if layer == 'gold' else 50 + cfg.eg

  wire(layer, x, y, w, width, -1, sign)
  dxf.srect(layer, x, y, length, width)
  wire(layer, x + length, y, w, width, 1, sign)

if __name__ == '__main__':

  electrode('gold', 0, 0, 100, 2, 1)
  electrode('edge', 0, 0, 100, cfg.eg, 1)

  dev.saveas(cfg.work + 'pad')