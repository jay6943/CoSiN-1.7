import cfg
import dxf
import dev
import key
import mask
import numpy as np

radius = 150 * 0.5 * 1000
wbar = 400
size = wbar + cfg.size
rmax = radius + 5000
wcut = 1

fontsize = 25

def wafer(x, y):
  
  a = np.linspace(-70, 250, 81) * np.pi / 180
  
  xp = x + radius * np.cos(a)
  yp = y + radius * np.sin(a)

  data = np.array([xp, yp]).transpose()
  cfg.data.append(['edge'] + data.tolist())

  t = 4000

  dxf.crect('fill', x - rmax, y - rmax, t - rmax, t - rmax)
  dxf.crect('fill', x - rmax, y + rmax, t - rmax, rmax - t)
  dxf.crect('fill', x + rmax, y - rmax, rmax - t, t - rmax)
  dxf.crect('fill', x + rmax, y + rmax, rmax - t, rmax - t)

def cells(x, y, n, title, fp):

  cs = cfg.size * 0.5
  dx, dy = 400, 400 + cs

  for i in range(n):
    xp = x + size * (i - n * 0.5)
    key.bars(xp, y)
    dxf.srect('recs', xp + dx, y + dy, cfg.size, cfg.size)
    dxf.texts('text', xp + cs, y + cs, title, 40, 'cc')

def tooling(x, y):

  fp = cfg.work + 'wafer'

  for i in range(11):
    dy, n = size * (i - 5.5), 10 if i % 10 else 8
    cells(x, y + dy, n, '0' + str(i % 4 + 1), fp)
  
  a = cfg.size * 6
  b = cfg.size * 2

  dxf.crect('cuts', x - rmax, y + a, rmax, wcut + a)
  dxf.crect('cuts', x - rmax, y + b, rmax, wcut + b)
  dxf.crect('cuts', x - rmax, y - b, rmax, wcut - b)
  dxf.crect('cuts', x - rmax, y - a, rmax, wcut - a)

  for i in range(11):
    xp = (i - 5) * size + x
    dxf.srect('cuts', xp + wbar - 200, y, wcut, rmax * 2)

  wafer(0, 0)

  dev.saveas(fp)

if __name__ == '__main__': tooling(0, 0)