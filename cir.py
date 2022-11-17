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

def update(wg, radius, angle, draft):

  m = 25 if draft != 'mask' else 1000
  w = wg if draft != 'edge' else cfg.eg

  ip = str(radius) + '_' + str(angle) + '_' + draft
  fp = cfg.libs + 'cir_' + ip + '.npy'

  changed = False
  if os.path.isfile(fp):
    df = np.load(fp, allow_pickle=True).item()
    if df['m'] != m: changed = True
    if df['w'] != w: changed = True
  else: changed = True

  return save(fp, w, radius, angle, m) if changed else df