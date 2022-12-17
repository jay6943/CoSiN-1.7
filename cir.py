import os
import cfg
import numpy as np

def save(fp, wg, radius, angle, m):

  width = wg * 0.5

  n = int(m * angle / 45)
  t = np.linspace(0, angle, n) * np.pi / 180

  x = np.cos(t)
  y = np.sin(t)

  xinner = (radius - width) * x - radius * x[0]
  yinner = (radius - width) * y - radius * y[0]
  xouter = (radius + width) * x - radius * x[0]
  youter = (radius + width) * y - radius * y[0]

  df = {}
  df['n'] = n
  df['m'] = m
  df['x'] = np.append(xinner, xouter[::-1])
  df['y'] = np.append(yinner, youter[::-1])
  df['r'] = radius
  df['w'] = wg
  df['dx'] = x[-1] * radius
  df['dy'] = y[-1] * radius
  df['angle'] = angle

  np.save(fp, df)

  print('circular', radius, angle, m)

  return df

def update(wg, radius, angle):

  m = 10 if cfg.draft != 'mask' else 20
  m = 10 if wg > cfg.wg else m

  w = str(round(wg, 4)) + '_'
  r = str(round(radius, 4)) + '_'
  a = str(round(angle, 4)) + '_'
  fp = cfg.libs + 'cir_' + w + r + a + str(m) + '.npy'

  if os.path.isfile(fp):
    df = np.load(fp, allow_pickle=True).item()
  else:
    df = save(fp, wg, radius, angle, m)

  return df