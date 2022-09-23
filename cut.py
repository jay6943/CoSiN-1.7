import cfg
import dxf
import dev
import key
import numpy as np

radius = 150e3 * 0.5
wbar = 400
size = wbar + cfg.size
rmax = radius + 5000
wcut = 0.1

fontsize = 25

def wafer(layer):
  
  a = np.linspace(-70, 250, 81) * np.pi / 180
  
  xp = radius * np.cos(a)
  yp = radius * np.sin(a)

  data = np.array([xp, yp]).transpose()
  cfg.data.append([layer] + data.tolist())

  t = 4000

  dxf.crect('fill', -rmax, -rmax, t-rmax, t-rmax)
  dxf.crect('fill', -rmax,  rmax, t-rmax, rmax-t)
  dxf.crect('fill',  rmax, -rmax, rmax-t, t-rmax)
  dxf.crect('fill',  rmax,  rmax, rmax-t, rmax-t)

def tooling(layer, x, y, title, ix, jy):

  for i in range(5):
    xp = i * size + x
    for j in range(5):
      if i != ix or j != jy:
        yp = (j + 0.5) * size + y
        dxf.srect(layer, xp, yp, size, size)
        dxf.texts('text', xp + size * 0.5, yp, title, fontsize, 'cc')

def dicing(x, y, ix, jy):

  dx = 400
  dy = 400 + cfg.size * 0.5

  for i in range(5):
    xp = i * size + x
    for j in range(5):
      if i != ix or j != jy:
        yp = j * size + y
        key.bars(xp, yp)
        dxf.srect('recs', xp + dx, yp + dy, cfg.size, cfg.size)

def toolings(x, y):

  s = -5 * size
  d = size * 0.5

  tooling('core', x + s, y + d, '01', 0, 4)
  tooling('keys', x + 0, y + d, '03-04', 4, 4)
  tooling('slab', x + s, y + s - d, '02', 0, 0)
  tooling('gold', x + 0, y + s - d, '03-04', 4, 0)

  for i in range(10):
    xp = (i - 5) * size + x
    dxf.srect('recs', xp, y, size, size)

  dev.saveas('tooling')

def cuttings(x, y):

  s = -5 * size
  d = size * 0.5

  dicing(x + s, y + d, 0, 4)
  dicing(x + 0, y + d, 4, 4)
  dicing(x + s, y + s - d, 0, 0)
  dicing(x + 0, y + s - d, 4, 0)

  dxf.crect('cuts', -rmax, 0, rmax, wcut)

  for i in range(10):
    xp = (i - 5) * size + x
    dxf.srect('cuts', xp + wbar + 100, y, wcut, rmax * 2)
    dxf.srect('cuts', xp + size - 100, y, wcut, rmax * 2)

  dev.saveas('scribing')

if __name__ == '__main__':

  wafer('edge')

  toolings(0, 0)
  cuttings(0, 0)