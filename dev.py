import cfg
import dxf
import tip
import euler as er
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

  core = er.bends[str(er.radius) + '_' + str(angle) + '_' + cfg.draft]
  edge = er.bends[str(er.radius) + '_' + str(angle) + '_' + 'edge']

  x1, y1 = dxf.bends('edge', x, y, edge, rotate, sign)
  x1, y1 = dxf.bends('core', x, y, core, rotate, sign)

  return x1, y1

def sbend(x, y, offset, angle, rotate, shape):

  core = er.bends[str(er.radius) + '_' + str(angle) + '_' + cfg.draft]
  edge = er.bends[str(er.radius) + '_' + str(angle) + '_' + 'edge']

  x1, y1 = dxf.sbend('edge', x, y, offset, edge, rotate, shape)
  x1, y1 = dxf.sbend('core', x, y, offset, core, rotate, shape)

  return x1, y1

def rectangles(x, y):

  d, w = 50, 125

  xp = np.arange(0, cfg.size, w) + x + (w - d) * 0.5
  yp = np.arange(0, cfg.size, w) + y + (w - d) * 0.5

  for j in yp:
    for i in xp:
      dxf.crect('recs', i, j, i+d, j+d)

  for j in yp[:-1] + w * 0.5:
    for i in xp[:-1] + w * 0.5:
      dxf.crect('recs', i, j, i+d, j+d)

def texts(x, y, title, scale, align):

  if align[0] == 'l': x = x + 10
  if align[0] == 'r': x = x - 10

  l, w = dxf.texts('core', x, y, title, scale, align)

  if align[0] == 'l': xalign = x - 10
  if align[0] == 'c': xalign = x - l * 0.5 - 10
  if align[0] == 'r': xalign = x - l - 10

  dxf.srect('edge', xalign, y, l + 20, w + 20)

def arange(start, stop, step):

  return np.arange(start, stop + step * 0.5, step)

def move(idev, x, xp, length):

  ltip = (length - xp + x) * 0.5

  if ltip < tip.ltip: ltip = tip.ltip

  xtip, _ = dxf.move(idev, x, 0, xp, 0, ltip, 0, 0)

  return xtip, ltip

def saveas(filename):

  fp = dxf.start(filename)
  dxf.conversion(fp)
  dxf.close(fp)

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

  saveas('sbend')