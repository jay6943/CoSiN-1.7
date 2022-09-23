import os
import cfg
import numpy as np

def save(fp, r, start, stop, draft, wg, m):

  angle = abs(stop - start)
  width = wg[draft] * 0.5

  n = int(m[draft] * angle / 45)
  t = np.linspace(start, stop, n) * np.pi / 180

  x = np.cos(t)
  y = np.sin(t)

  xinner = (r - width) * x - r * x[0]
  yinner = (r - width) * y - r * y[0]
  xouter = (r + width) * x - r * x[0]
  youter = (r + width) * y - r * y[0]

  df = {}
  df['n'] = n
  df['m'] = m
  df['x'] = np.append(xinner, xouter[::-1])
  df['y'] = np.append(yinner, youter[::-1])
  df['r'] = r
  df['w'] = wg[draft]
  df['dx'] = x[-1] * r
  df['dy'] = y[-1] * r
  df['angle'] = angle
  df['start'] = start
  df['stop'] = stop

  np.save(fp, df)

  print('circular', r, start, stop, draft)

  return df

def update(wg, r, start, stop):

  obj = {}

  w = {'mask':wg, 'draft':wg, 'edge':cfg.eg}
  m = {'mask':1000, 'draft':25, 'edge':25}

  for draft in ['mask', 'draft', 'edge']:
    i = str(start) + '_' + str(stop) + '_' + draft
    fp = cfg.libs + 'r' + str(r) + '_' + i + '.npy'

    changed = False
    if os.path.isfile(fp):
      df = np.load(fp, allow_pickle=True).item()
      if df['m'] != m: changed = True
      if df['r'] != r: changed = True
      if df['w'] != w[draft]: changed = True
      if df['start'] != start: changed = True
      if df['stop'] != stop: changed = True
    else: changed = True

    obj[i] = save(fp, r, start, stop, draft, w, m) if changed else df

  return obj

r5 = update(cfg.wg, 5, 0, 90)