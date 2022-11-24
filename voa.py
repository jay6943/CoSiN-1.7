import cfg
import dxf
import dev
import tip
import pad
import y1x2

xsize = cfg.size
ysize = cfg.ch * 4

def arm(x, y, sign):

  x1, y = dev.sline(x, y, cfg.lvoa)
  
  pad.electrode('gold', x, y, cfg.lvoa, cfg.wg + 2, sign)
  pad.electrode('edge', x, y, cfg.lvoa, cfg.eg, sign)

  return x1, y

def device(x, y):

  ch = cfg.ch * 0.5

  x2, y1, y2 = y1x2.device(x, y, 1)

  x3, y3 = dev.sbend(x2, y1,  ch, 45, 0, 1)
  x3, y4 = dev.sbend(x2, y2, -ch, 45, 0, 1)

  x5, y3 = arm(x3, y3,  1)
  x5, y4 = arm(x3, y4, -1)

  x9, y1 = dev.sbend(x5, y3, -ch, 45, 0, 1)
  x9, y2 = dev.sbend(x5, y4,  ch, 45, 0, 1)

  x10, y1, y2 = y1x2.device(x9, y, -1)

  return x10, y

def chip(x, y, lchip):

  ch = cfg.ch * 0.5

  idev = len(cfg.data)
  x1, _ = device(x, y)
  x2, ltip = dev.move(idev, x, x1, lchip)

  x3, _, t2 = tip.fiber(x, y, ltip, -1)
  x3, _, t3 = tip.fiber(x2, y, ltip, 1)

  s = 'voa-' + str(int(cfg.lvoa))
  dev.texts(t2, y + ch, s, 0.5, 'lc')
  dev.texts(t2, y - ch, s, 0.5, 'lc')
  dev.texts(t3, y + ch, s, 0.5, 'rc')
  dev.texts(t3, y - ch, s, 0.5, 'rc')
  print(s, int(x3 - x))

  return x3, y + ysize

# def chips(x, y, arange):

#   var = cfg.lvoa

#   y1 = y + cfg.ch * 2
#   l1 = tip.ltip + 300

#   for cfg.lvoa in arange:
    
#     x1, t2 = tip.fiber(x, y1, l1, -1)
#     x2, y1 = device(x1, y1)
#     x3, t3 = tip.fiber(x2, y1, xsize - x2 + x, 1)

#     s = 'voa-' + str(int(cfg.lvoa))
#     dev.texts(t2, y1 + cfg.ch * 0.5, s, 0.5, 'lc')
#     dev.texts(t2, y1 - cfg.ch * 0.5, s, 0.5, 'lc')
#     dev.texts(t3, y1 + cfg.ch * 0.5, s, 0.5, 'rc')
#     dev.texts(t3, y1 - cfg.ch * 0.5, s, 0.5, 'rc')

#     y1 = y1 + cfg.ch * 2
#     l1 = l1 + x2 - x1

#     print(s, int(x3 - x))

#   cfg.lvoa = var

#   return x + xsize, y1

def chips(x, y, arange):

  var = cfg.lvoa

  x1, y1, _ = tip.fiber(x, y + cfg.ch * 2, tip.ltip + 900, -1)

  for cfg.lvoa in arange:
    
    x2, y1 = device(x1, y1)
    dev.texts((x2 + x1) * 0.5, y1, str(int(cfg.lvoa)), 1, 'cc')
    dxf.srect('edge', (x2 + x1 - cfg.lvoa) * 0.5, y1, cfg.lvoa, 120)
    x1, y1 = dev.sline(x2, y1, 600)

  x1, y1, _ = tip.fiber(x1, y1, xsize - x1 + x, 1)

  print('VOA', int(x1 - x))

  cfg.lvoa = var

  return x1, y1

if __name__ == '__main__':

  # chip(0, 0, 0)
  
  chips(0, 0, dev.arange(200, 500, 100))

  dev.saveas(cfg.work + 'voa')