import os
import cfg
import dxf
import euler as elr
import numpy as np

def srect(x, y, length, width):

  wg = 0 if width < cfg.wtpr else width

  x1, y1 = dxf.srect('edge', x, y, length, wg + cfg.eg)
  x1, y1 = dxf.srect('core', x, y, length, width)

  return x1, y1

def sline(x, y, length):

  x1, y1 = dxf.srect('edge', x, y, length, cfg.eg)
  x1, y1 = dxf.srect('core', x, y, length, cfg.wg)

  return x1, y1

def tline(x, y, length):

  w = cfg.wg * 0.5
  d = cfg.eg * 0.5

  x1, y1 = dxf.crect('edge', x - d, y, x + d, y + length)
  x1, y1 = dxf.crect('core', x - w, y, x + w, y + length)

  return x1 - w, y1

def tilts(x, y, length, angle):

  x1, y1 = dxf.tilts('edge', x, y, length, cfg.eg, angle)
  x1, y1 = dxf.tilts('core', x, y, length, cfg.wg, angle)

  return x1, y1

def taper(x, y, length, wstart, wstop):

  x1, y1 = dxf.srect('edge', x, y, length, cfg.eg)
  x1, y1 = dxf.taper('core', x, y, length, wstart, wstop)

  return x1, y1

def bends(x, y, angle, rotate, sign):

  core = elr.update(cfg.wg, cfg.radius, angle, cfg.draft)
  edge = elr.update(cfg.wg, cfg.radius, angle, 'edge')

  x1, y1 = dxf.bends('edge', x, y, edge, rotate, sign)
  x1, y1 = dxf.bends('core', x, y, core, rotate, sign)

  return x1, y1

def sbend(x, y, offset, angle, rotate, shape):

  core = elr.update(cfg.wg, cfg.radius, angle, cfg.draft)
  edge = elr.update(cfg.wg, cfg.radius, angle, 'edge')

  x1, y1 = dxf.sbend('edge', x, y, offset, edge, rotate, shape)
  x1, y1 = dxf.sbend('core', x, y, offset, core, rotate, shape)

  return x1, y1

def cover(x, y, pattern):

  if pattern == 'stress release':

    d, w = 50, 125

    xp = np.arange(0, cfg.size, w) + x + (w - d) * 0.5
    yp = np.arange(0, cfg.size, w) + y + (w - d) * 0.5

    for j in yp:
      for i in xp:
        dxf.crect('recs', i, j, i+d, j+d)

    for j in yp[:-1] + w * 0.5:
      for i in xp[:-1] + w * 0.5:
        dxf.crect('recs', i, j, i+d, j+d)
  
  if pattern == 'block':
    dxf.crect('recs', x, y, x + cfg.size, y + cfg.size)

def texts(x, y, title, scale, align):

  d = 10 * scale * 2 # 10 when scale = 0.5

  if align[0] == 'l': x = x + d
  if align[0] == 'r': x = x - d

  l, w = dxf.texts('core', x, y, title, scale, align)

  if align[0] == 'l': xalign = x - d
  if align[0] == 'c': xalign = x - l * 0.5 - d
  if align[0] == 'r': xalign = x - l - d

  dxf.srect('edge', xalign, y, l + d * 2, w + d * 2)

def arange(start, stop, step):

  return np.arange(start, stop + step * 0.5, step)

def center(idev, x, xt, lchip):

  ldev = xt - x
  ltip = (lchip - ldev) * 0.5

  xt, _ = dxf.move(idev, x, 0, xt, 0, ltip, 0, 0)

  return xt - ldev, xt, xt - ldev - x

def removes(folder):

  if os.path.isdir(folder):
    
    files = os.listdir(folder)
    
    for fp in files:
      if os.path.exists(folder + fp): os.remove(folder + fp)
    
    os.rmdir(folder)

def saveas(filename):

  fp = dxf.start(filename)
  dxf.conversion(fp)
  dxf.close(fp)

  removes('__pycache__/')

if __name__ == '__main__':

  cfg.draft = 'mask'

  # bends(0, 0, 45, 0, -1)
  # bends(0, 0, 45, 90, -1)
  # bends(0, 0, 45, 180, -1)
  # bends(0, 0, 45, 270, -1)

  # sbend(0, 0, 100, 90, 0, 2)
  # sbend(0, 0, 100, 90, 90, 2)
  # sbend(0, 0, 100, 90, 180, 2)
  sbend(0, 0, 100, 90, 270, 2)

  saveas(cfg.work + 'sbend')