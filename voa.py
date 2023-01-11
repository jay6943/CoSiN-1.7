import cfg
import dev
import tip
import pad
import y1x2

def arm(x, y, sign):

  x1, y = dev.srect(x, y, cfg.lvoa, cfg.wr)
  
  pad.electrode('gold', x, y, cfg.lvoa, cfg.wg + 2, sign)
  pad.electrode('edge', x, y, cfg.lvoa, cfg.eg, sign)

  return x1, y

def device(x, y):

  ch = cfg.ch * 0.5

  x2, y1, y2 = y1x2.device(x, y, 1)

  x3, y3 = dev.sbend(x2, y1, 45,  ch)
  x3, y4 = dev.sbend(x2, y2, 45, -ch)

  x5, y3 = arm(x3, y3,  1)
  x5, y4 = arm(x3, y4, -1)

  x9, y1 = dev.sbend(x5, y3, 45, -ch)
  x9, y2 = dev.sbend(x5, y4, 45,  ch)

  x10, y1, y2 = y1x2.device(x9, y, -1)

  return x10, y

def chip(x, y, lchip):

  ch = cfg.ch * 0.5

  idev = len(cfg.data)
  x1, _ = device(x, y)
  x5, x6, ltip = dev.center(idev, x, x1, lchip)

  x7, t1 = tip.fiber(x5, y, ltip, -1)
  x8, t2 = tip.fiber(x6, y, ltip,  1)

  s = 'voa-' + str(round(cfg.lvoa))
  dev.texts(t1, y + ch, s, 0.2, 'lc')
  dev.texts(t1, y - ch, s, 0.2, 'lc')
  dev.texts(t2, y + ch, s, 0.2, 'rc')
  dev.texts(t2, y - ch, s, 0.2, 'rc')
  print(s, round(x6 - x5), round(x8 - x7))

  return x + lchip, y

def chips(x, y, arange):

  var = cfg.lvoa

  x2 = x
  idev = len(cfg.data)
  for cfg.lvoa in arange:
    x1, _ = device(x2, y)
    dev.texts((x2 + x1) * 0.5, y, str(int(cfg.lvoa)), 1, 'cc')
    x2, y = dev.sline(x1, y, 600)
  x3, x4, ltip = dev.center(idev, x, x2, cfg.size)

  x5, _ = tip.fiber(x3, y, ltip, -1)
  x6, _ = tip.fiber(x4, y, ltip, 1)

  print('VOA', round(x4 - 3), round(x6 - x5))

  cfg.lvoa = var

  return x1, y

if __name__ == '__main__':

  # chip(0, 0, 2000)
  
  chips(0, 0, dev.arange(200, 500, 100))

  dev.saveas(cfg.work + 'voa')