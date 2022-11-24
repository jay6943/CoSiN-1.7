import cfg
import dxf
import dev
import cir
import euler as elr
import numpy as np

lwg = 10

def angle_45(filename):

  x, y = dev.sline(0, 0, lwg)
  x, y = dev.sbend(x, y, 0, 45, 0, 1)
  x, y = dev.sline(x, y, lwg)

  dev.saveas(filename)

def angle_45_taper(filename):

  x, y = dev.srect(0, 0, lwg, cfg.wt)
  x, y = dev.taper(x, y, cfg.ltpr, cfg.wt, cfg.wg)
  x, y = dev.sbend(x, y, cfg.ch * 0.5, 45, 0, 1)
  x, y = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wt)
  x, y = dev.srect(x, y, lwg, cfg.wt)

  dev.saveas(filename)

def angle_90(filename):

  x, y = dev.sline(0, 0, lwg)
  x, y = dev.bends(x, y, 90, 0, 1)
  x, y = dev.tline(x, y, lwg)

  dev.saveas(filename)

def angle_180(filename):

  w1 = 0.3
  w2 = 6

  s1 = elr.update(w1, 100, 180, 'mask')
  s2 = elr.update(w2, 100, 180, 'mask')

  x1, y1 = dxf.srect('core', 0, 0, lwg, w1)
  x1, y1 = dxf.srect('clad', 0, 0, lwg, w2)
  x2, y2 = dxf.bends('core', x1, y1, s1, 0, 1)
  x2, y2 = dxf.bends('clad', x1, y1, s2, 0, 1)
  x3, y3 = dxf.srect('core', x2, y2, -lwg, w1)
  x3, y3 = dxf.srect('clad', x2, y2, -lwg, w2)

  dev.saveas(filename)

def angle_180_taper(filename):

  x, y = dev.srect(0, 0, lwg, cfg.wt)
  x, y = dev.taper(x, y, cfg.ltpr, cfg.wt, cfg.wg)
  x, y = dev.bends(x, y, 180, 0, 1)
  x, y = dev.taper(x, y, -cfg.ltpr, cfg.wg, cfg.wt)
  x, y = dev.srect(x, y, -lwg, cfg.wt)

  dev.saveas(filename)

def angle_90x2(filename):

  x, y = dev.sline(0, 0, lwg)
  x, y = dev.bends(x, y, 90, 0, 1)
  x, y = dev.tline(x, y, lwg)
  x, y = dev.bends(x, y, 90, 90, 1)
  x, y = dev.sline(x, y, -lwg)

  dev.saveas(filename)

def sbend(filename, radius, angle):

  df = elr.update(cfg.wg, radius, angle, 'mask')

  x, y = dxf.sline('core', 0, 0, lwg)
  x, y = dxf.sbend('core', x, y, 50, df, angle, 1)
  x, y = dxf.sline('core', x, y, lwg)

  dev.saveas(filename)

def dc(filename):

  df = cir.update(cfg.wg, 20, 90, 'mask')

  dxf.bends('core', 0, 0, df, 90, 1)
  dev.saveas(filename + '-in')

  dxf.bends('core', 0, 0, df, 270, 1)
  dev.saveas(filename + '-out')

  df = elr.update(cfg.wg, 20, 5, 'mask')

  x, y = dxf.sbend('core', 0, 0, 1, df, 0, 1)
  x, y = dxf.sline('core', x, y, 10)
  dev.saveas(filename + '-1')

  x, y = dxf.sbend('core', 0, 0, 1, df, 0, -1)
  x, y = dxf.sline('core', x, y, 10)
  dev.saveas(filename + '-2')

def tap_device(x, y, sign):

  wg = 0.38
  ch =  cfg.ch * 0.5

  s1 = elr.update(wg, 50, 3, 'mask')
  s2 = elr.update(cfg.wg, 125, 42, 'mask')
  s3 = elr.update(cfg.wg, 125, 45, 'mask')

  x1, y1 = dxf.bends('core', x, y, s1, 0, sign)

  idev = len(cfg.data)
  x2, y2 = dxf.taper('core', x1, y1, 20, wg, cfg.wg)
  x3, y3 = dxf.move(idev, x1, y1, x2, y2, 0, 0, sign * 3)

  x4, y4 = dxf.bends('core', x3, y3, s2, 3, sign)

  l = np.sqrt(2) * (y + sign * (ch - s3['dy']) - y4)

  idev = len(cfg.data)
  x5, y5 = dxf.sline('core', x4, y4, l)
  x6, y6 = dxf.move(idev, x4, y4, x5, y5, 0, 0, sign * 45)
  
  x7, y7 = dxf.bends('core', x6, y6, s3, 315, -sign)

  return x7, y7

def tap(filename):

  wg = 0.38
  ch = 1
  cf = cir.update(wg, 5, 90, 'mask')
  df = elr.update(wg, 50, 3, 'mask')

  dxf.sbend('core', 0, 0, -ch, df, 0, 1)
  dev.saveas(filename + '-1')

  dxf.sbend('core', 0, 0, ch, df, 0, 1)
  dev.saveas(filename + '-2')

  dxf.bends('core', 0, 0, cf, 90, 1)
  dev.saveas(filename + '-3')

def y2x2_arm(x, y, wg, df, sign):

  l, h = 19, 1

  x1, y1 = dxf.taper('core', x, y, 20, cfg.wg, wg)
  x2, y2 = dxf.sbend('core', x1, y1, -h, df, 0, sign)
  x3, y3 = dxf.srect('core', x2, y2, l, wg)
  x4, y4 = dxf.sbend('core', x3, y3,  h, df, 0, sign)
  x5, y5 = dxf.taper('core', x4, y4, 20, wg, cfg.wg)

  return x5, y5

def y2x2(filename):

  wg = 0.38
  dy = 2
  df = elr.update(wg, 50, 3, 'mask')

  y2x2_arm(0,  dy, wg, df,  1)
  y2x2_arm(0, -dy, wg, df, -1)

  dev.saveas(filename)

def soa(filename):

  wg = 0.8
  df = elr.update(cfg.wg, 100, 7, 'mask')

  x1, y1 = dev.sline(-5, 0, 10)
  x2, y2 = dev.bends(x1, y1, 7, 0, 1)

  idev = len(cfg.data)
  x3, y3 = dev.taper(x2, y2, 200, cfg.wg, wg)
  x4, y4 = dev.srect(x3, y3, 10, wg)
  dxf.move(idev, x2, y2, x4, y4, 0, 0, 7)

  dev.saveas(filename)

if __name__ == '__main__':

  cfg.draft = 'mask'

  # angle_45('D:/ansys/Euler/45')
  # angle_90('D:/ansys/Euler/90')
  angle_180('C:/Git/mask/SiN-1.7/180')
  # angle_90x2('D:/ansys/Euler/90x2')
  # sbend('D:/ansys/tap/sbend', 45)
  # dc('D:/Git/mask/dc')
  # soa('D:/ansys/LD/soa')
  # tap('D:/ansys/coupler/sym')
  # y2x2('D:/Git/mask/2x2')
  # soa('D:/ansys/SOA/soa')