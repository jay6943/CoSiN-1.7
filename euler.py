import os
import cfg
import dxf
import numpy as np
import scipy.special as ss

radius = 125

def curve(wg, r, angle, m):

  width = wg * 0.5
  
  s = np.sqrt(angle / 180)
  c = np.sqrt(np.pi * 0.5)
  n = round(m * s)
  t = np.linspace(0, s, n)
  
  xt, yt = ss.fresnel(t)
  
  x = yt * c * r
  y = xt * c * r

  p = t * c

  px = np.sin(p * p)
  py = np.cos(p * p)

  rc = np.array([0] + (r / p[1:] * 0.5).tolist())
  dx = x - rc * px
  dy = y + rc * py

  xinner = dx + (rc - width) * px
  yinner = dy - (rc - width) * py
  xouter = dx + (rc + width) * px
  youter = dy - (rc + width) * py

  xp = np.append(xinner, xouter[::-1])
  yp = np.append(yinner, youter[::-1])

  df = {}
  df['n'] = n
  df['x'] = xp
  df['y'] = yp
  df['dx'] = dx[-1]
  df['dy'] = dy[-1]

  return df

def rotate(df, oxt, rxt):

  dx = df['dx'] - oxt[0]
  dy = df['dy'] - oxt[1]

  cvt = rxt @ np.array([-df['x'], df['y']])
  cvt = cvt + np.array([dx, dy]).reshape(2,1)

  n = df['n']

  xp = np.array(df['x'][:n])
  yp = np.array(df['y'][:n])
  xp = np.append(xp, cvt[0][:n][::-1])
  yp = np.append(yp, cvt[1][:n][::-1])
  xp = np.append(xp, cvt[0][n:][::-1])
  yp = np.append(yp, cvt[1][n:][::-1])
  xp = np.append(xp, df['x'][n:])
  yp = np.append(yp, df['y'][n:])

  return xp, yp

def save(fp, r, angle, draft, wg, m):
  
  rxt = dxf.rxt(angle)
  obj = curve(wg[draft], r, angle, m[draft])
  oxt = rxt @ np.array([-obj['dx'], obj['dy']]).reshape(2,1)

  xp, yp = rotate(obj, oxt, rxt)

  n = obj['n'] * 2

  df = {}
  df['n'] = n
  df['m'] = m
  df['x'] = xp
  df['y'] = yp
  df['r'] = r
  df['w'] = wg[draft]
  df['dx'] = (xp[n-1] + xp[n]) * 0.5
  df['dy'] = (yp[n-1] + yp[n]) * 0.5
  df['angle'] = angle

  np.save(fp, df)

  print('euler', angle, draft)

  return df

def update():

  obj = {}

  w = {'mask':cfg.wg, 'draft':cfg.wg, 'edge':cfg.eg}
  m = {'mask':1000, 'draft':50, 'edge':50}

  for r in [50, 75, 100, 125]:

    if r < 125: angles = [180]
    else: angles = [45, 90, 180, 27, 32, 37, 53, 58, 63]
      
    for draft in ['mask', 'draft', 'edge']:
      for angle in angles:
        i = str(r) + '_' + str(angle) + '_' + draft
        fp = cfg.libs + 'euler_' + i + '.npy'

        changed = False
        if os.path.isfile(fp):
          df = np.load(fp, allow_pickle=True).item()
          if df['m'] != m: changed = True
          if df['r'] != r: changed = True
          if df['w'] != w[draft]: changed = True
        else: changed = True
        obj[i] = save(fp, r, angle, draft, w, m) if changed else df

  return obj

bends = update()