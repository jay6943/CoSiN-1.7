import cfg
import dev
import pbs
import voa
import psk
import tip

yqpsk = cfg.ch * 2

xsize = cfg.size
ysize = cfg.ch * 8

def chip(x, y, lchip):

  idev = len(cfg.data)

  x2, y1 = voa.device(x, y + cfg.ch)
  x3, y1 = dev.sline(x2, y1, 100)
  x3, y2 = dev.sline(x, y - cfg.ch, x3 - x)

  x4, y41, y42 = pbs.device(x3, y1)
  x4, y43, y44 = pbs.device(x3, y2)

  x5, _ = dev.taper(x4, y41, cfg.ltpr, cfg.wt, cfg.wg)
  x5, _ = dev.taper(x4, y42, cfg.ltpr, cfg.wt, cfg.wg)
  x5, _ = dev.taper(x4, y43, cfg.ltpr, cfg.wt, cfg.wg)
  x5, _ = dev.taper(x4, y44, cfg.ltpr, cfg.wt, cfg.wg)

  x6, y71 = dev.sbend(x5, y41,  cfg.ch, 45, 0, 1)
  x6, y74 = dev.sbend(x5, y44, -cfg.ch, 45, 0, 1)
  x7, y72 = dev.sbend(x5, y42, -yqpsk, 45, 0, 1)
  x7, y73 = dev.sbend(x5, y43,  yqpsk, 45, 0, 1)

  x8, _ = dev.taper(x6, y71, cfg.ltpr, cfg.wg, cfg.wt)
  x8, _ = dev.taper(x6, y74, cfg.ltpr, cfg.wg, cfg.wt)
  x9, _ = dev.taper(x7, y72, cfg.ltpr, cfg.wg, cfg.wt)
  x9, _ = dev.taper(x7, y73, cfg.ltpr, cfg.wg, cfg.wt)

  x9, _ = dev.srect(x8, y71, x9 - x8, cfg.wt)
  x9, _ = dev.srect(x8, y74, x9 - x8, cfg.wt)

  x10, _ = psk.device(x9, y + yqpsk)
  x10, _ = psk.device(x9, y - yqpsk)

  x11, x12, ltip = dev.xshift(idev, x, x10, lchip)

  x13, _ = tip.fiber(x11, y1, ltip, -1)
  x13, _ = tip.fiber(x11, y2, ltip, -1)

  for i in range(8):
    x14, _ = tip.fiber(x12, y + (i - 3.5) * cfg.ch, ltip, 1)

  print('DP-QPSK', int(x12 - x11), int(x14 - x13))

  return x + lchip, y

def chips(x, y):

  for i in range(4):
    chip(x, y + i * ysize, xsize)
    chip(x + xsize, y + i * ysize, xsize)

if __name__ == '__main__':

  chip(0, 0, xsize)

  dev.saveas(cfg.work + 'qpsk')