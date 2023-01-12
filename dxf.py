import cfg
import txt
import numpy as np

def start(filename):

  fp = open(filename + '.dxf', 'w')

  fp.write('0\nSECTION\n')
  fp.write('2\nHEADER\n')
  fp.write('0\nENDSEC\n')
  fp.write('0\nSECTION\n')
  fp.write('2\nTABLES\n')
  fp.write('0\nENDSEC\n')
  fp.write('0\nSECTION\n')
  fp.write('2\nENTITIES\n')

  return fp

def polyline(fp, layer):

  fp.write('0\nPOLYLINE\n')
  fp.write('8\n' + layer + '\n')
  fp.write('66\n1\n')
  fp.write('10\n0\n')
  fp.write('20\n0\n')
  fp.write('70\n1\n')
  
def vertex(fp, layer, x, y):

  xstr = str(round(x, 6))
  ystr = str(round(y, 6))

  if xstr[-2:] == '.0': xstr = xstr[:-2]
  if ystr[-2:] == '.0': ystr = ystr[:-2]

  fp.write('0\nVERTEX\n8\n' + layer + '\n')
  fp.write('10\n' + xstr + '\n')
  fp.write('20\n' + ystr + '\n')
  
def seqend(fp, layer):

  fp.write('0\nSEQEND\n')
  fp.write('8\n' + layer + '\n')

def close(fp):

  fp.write('0\nENDSEC\n')
  fp.write('0\nEOF\n')

  fp.close()

def conversion(fp):

  for device in cfg.data:

    layer = device[0]

    if layer in cfg.layer:
      if cfg.layer[layer] > 0:

        dx = cfg.area[cfg.layer[layer]][0] * cfg.mask
        dy = cfg.area[cfg.layer[layer]][1] * cfg.mask

        polyline(fp, layer)
        for [x, y] in device[1:]: vertex(fp, layer, x + dx, y + dy)
        seqend(fp, layer)
    
    else: print('There is NO layer ----', layer, '----')

  cfg.data.clear()

def copier(fp, layer, area):

  i = 0

  for device in cfg.data:

    if layer == device[0]:

      dx = cfg.area[area][0] * cfg.mask
      dy = cfg.area[area][1] * cfg.mask

      polyline(fp, layer)
      
      for [x, y] in device[1:]: vertex(fp, layer, x + dx, y + dy)                    
          
      seqend(fp, layer)
  
    i += 1

def rmatrix(rotate):
  
  arg = rotate * np.pi / 180

  rcos = np.cos(arg)
  rsin = np.sin(arg)

  return np.array([[rcos, -rsin], [rsin, rcos]])
  
def rotator(xp, yp, rotate):

  [xp, yp] = rmatrix(rotate) @ np.array([xp, yp])

  return xp, yp

def move(idev, x, y, xt, yt, dx, dy, rotate):

  for data in cfg.data[idev:len(cfg.data)]:
    xy = np.array(data[1:]).transpose()
    
    if rotate != 0:
      xy = rmatrix(rotate) @ xy
      s = rmatrix(rotate) @ [[x], [y]]
      t = rmatrix(rotate) @ [[xt], [yt]]
    else:
      s = [[x], [y]]
      t = [[xt], [yt]]
    
    px = x - s[0][0] + dx
    py = y - s[1][0] + dy
    
    xy = xy.transpose() + [px, py]
    
    data[1:] = xy.tolist()
  
  return t[0][0] + px, t[1][0] + py

def xreverse(idev, x, y, xt):
  
  for data in cfg.data[idev:len(cfg.data)]:
    xy = np.array(data[1:]) - [x, 0]
    xy = xy * [-1, 1]
    xy = xy + [xt, 0]

    data[1:] = xy.tolist()

  return x + xt, y

def yreverse(idev, x, y, xt):
  
  for data in cfg.data[idev:len(cfg.data)]:
    xy = np.array(data[1:])
    xy = xy * [1, -1]

    data[1:] = xy.tolist()

  return x + xt, y

def circle(layer, x, y, radius, n):

  t = np.linspace(0, np.pi * 2, n)

  xp = x + radius * np.cos(t)
  yp = y + radius * np.sin(t)

  data = np.array([xp, yp]).transpose()
  cfg.data.append([layer] + data.tolist())

  return x, y

def crect(layer, x1, y1, x2, y2):

  data = [layer]

  data.append([x1, y1])
  data.append([x2, y1])
  data.append([x2, y2])
  data.append([x1, y2])

  cfg.data.append(data)

  return x2, y2

def srect(layer, x, y, length, width):

  w = width * 0.5

  data = [layer]

  data.append([x, y - w])
  data.append([x + length, y - w])
  data.append([x + length, y + w])
  data.append([x, y + w])

  cfg.data.append(data)

  return x + length, y

def taper(layer, x, y, length, wstart, wstop):

  data = [layer]

  data.append([x, y - wstart * 0.5])
  data.append([x + length, y - wstop * 0.5])
  data.append([x + length, y + wstop * 0.5])
  data.append([x, y + wstart * 0.5])

  cfg.data.append(data)

  return x + length, y

def sline(layer, x, y, length):

  srect(layer, x, y, length, cfg.wg)
  
  return x + length, y

def tline(layer, x, y, length):

  w = cfg.wg * 0.5

  crect(layer, x - w, y, x + w, y + length)

  return x, y + length

def bends(layer, x, y, df, rotate, xsign, ysign):

  n = df['n']

  xp = np.array(df['x'])
  yp = np.array(df['y'])

  if rotate > 0: xp, yp = rotator(xp, yp, rotate)

  xp = x + xp * xsign
  yp = y + yp * ysign

  xo = (xp[n-1] + xp[n]) * 0.5
  yo = (yp[n-1] + yp[n]) * 0.5

  data = np.array([xp, yp]).transpose()
  cfg.data.append([layer] + data.tolist())

  return xo, yo

def sbend(layer, x, y, df, angle, dy):

  sign = 1 if dy > 0 else -1

  yo = dy - df['dy'] * 2 * sign
  xo = yo * sign / np.tan(angle / 180 * np.pi)

  data = [layer]

  x1, y1 = df['x'][df['n']-1], df['y'][df['n']-1] * sign
  x2, y2 = df['x'][df['n']  ], df['y'][df['n']  ] * sign
  x3, y3 = df['dx'] * 2 + xo - x1, dy - y1
  x4, y4 = df['dx'] * 2 + xo - x2, dy - y2

  data.append([x + x1, y + y1])
  data.append([x + x2, y + y2])
  data.append([x + x3, y + y3])
  data.append([x + x4, y + y4])
  
  cfg.data.append(data)

  x1, y1 = bends(layer, x, y, df, 0, 1, sign)
  x2, y2 = x1 + df['dx'] + xo, y1 + df['dy'] * sign + yo
  x3, y3 = bends(layer, x2, y2, df, 0, -1, -sign)

  return x3 + df['dx'], y3 + df['dy'] * sign

def tilts(layer, x, y, length, width, rotate):

  w = width * 0.5

  xp = np.array([0, length, length, 0])
  yp = np.array([w, w, -w, -w])

  xp, yp = rotator(xp, yp, rotate)
  xp, yp = xp + x, yp + y

  data = np.array([xp, yp]).transpose()
  cfg.data.append([layer] + data.tolist())

  return (xp[1] + xp[2]) * 0.5, (yp[1] + yp[2]) * 0.5

def texts(layer, x, y, title, scale, align):

  l = 0
  for c in title: l += txt.size[c] if c in txt.size else 50
  l = (l + 25 * (len(title) - 1)) * scale

  x -= txt.xalign[align[0]] * l
  y -= txt.yalign[align[1]] * scale * 100
  
  for c in title:
    if c in txt.size:
      xp = x + txt.x[c] * scale
      yp = y + txt.y[c] * scale
      data = np.array([xp, yp]).transpose()
      cfg.data.append([layer] + data.tolist())
      x += (txt.size[c] + 25) * scale
    else: x += 50 * scale

  return l, scale * 100