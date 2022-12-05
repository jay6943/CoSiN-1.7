import cfg
import dxf
import dev
import euler as elr

l = 10

def angle_45(filename):

  x, y = dev.sline(0, 0, l)
  x, y = dev.sbend(x, y, 45, 0)
  x, y = dev.sline(x, y, l)

  dev.saveas(filename)

def angle_45_taper(filename):

  x, y = dev.srect(0, 0, l, cfg.wt)
  x, y = dev.taper(x, y, cfg.ltpr, cfg.wt, cfg.wg)
  x, y = dev.sbend(x, y, 45, cfg.ch * 0.5)
  x, y = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wt)
  x, y = dev.srect(x, y, l, cfg.wt)

  dev.saveas(filename)

def angle_90(filename):

  x, y = dev.sline(0, 0, l)
  x, y = dev.bends(x, y, 90, 0, 1, 1)
  x, y = dev.tline(x, y, l)

  dev.saveas(filename)

def angle_180(filename):

  w1 = 0.3
  w2 = 6

  s1 = elr.update(w1, 100, 180, 'mask')
  s2 = elr.update(w2, 100, 180, 'mask')

  x1, y1 = dxf.srect('core', 0, 0, l, w1)
  x1, y1 = dxf.srect('clad', 0, 0, l, w2)
  x2, y2 = dxf.bends('core', x1, y1, s1, 0, 1, 1)
  x2, y2 = dxf.bends('clad', x1, y1, s2, 0, 1, 1)
  x3, y3 = dxf.srect('core', x2, y2, -l, w1)
  x3, y3 = dxf.srect('clad', x2, y2, -l, w2)

  dev.saveas(filename)

def angle_180_taper(filename):

  x, y = dev.srect(0, 0, l, cfg.wt)
  x, y = dev.taper(x, y, cfg.ltpr, cfg.wt, cfg.wg)
  x, y = dev.bends(x, y, 180, 0, 1, 1)
  x, y = dev.taper(x, y, -cfg.ltpr, cfg.wg, cfg.wt)
  x, y = dev.srect(x, y, -l, cfg.wt)

  dev.saveas(filename)

def angle_90x2(filename):

  x, y = dev.sline(0, 0, l)
  x, y = dev.bends(x, y, 90, 0, 1, 1)
  x, y = dev.tline(x, y, l)
  x, y = dev.bends(x, y, 90, 90, 1, 1)
  x, y = dev.sline(x, y, -l)

  dev.saveas(filename)

def sbend(filename):

  cfg.draft = 'mask'

  wg, radius, angle, dy = 0.42, 50, 3, 1

  df = elr.update(wg, radius, angle)

  dxf.sbend('core', 0, 0, df, angle, -dy)
  dev.saveas(filename + str(wg) + '-1')

  dxf.sbend('core', 0, 0, df, angle, dy)
  dev.saveas(filename + str(wg) + '-2')

if __name__ == '__main__':

  cfg.draft = 'mask'

  # angle_45('D:/ansys/Euler/45')
  # angle_90('D:/ansys/Euler/90')
  # angle_180('C:/Git/mask/SiN-1.7/180')
  # angle_90x2('D:/ansys/Euler/90x2')
  sbend('D:/ansys/coupler/')