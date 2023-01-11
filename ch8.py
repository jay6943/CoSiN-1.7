import cfg
import dev
import pbs
import voa
import qsk
import tip

yqpsk = cfg.ch * 2

def chip(x, y, lchip):

  ch = cfg.ch * 0.5

  idev = len(cfg.data)

  x2, y1 = voa.device(x, y + cfg.ch)
  x3, y2 = dev.sline(x, y - cfg.ch, x2 - x)

  x4, y41, y42 = pbs.device(x3, y1)
  x4, y43, y44 = pbs.device(x3, y2)

  x5, y51 = dev.taper(x4, y41, cfg.ltpr, cfg.wg, cfg.wr)
  x5, y52 = dev.taper(x4, y42, cfg.ltpr, cfg.wg, cfg.wr)
  x5, y53 = dev.taper(x4, y43, cfg.ltpr, cfg.wg, cfg.wr)
  x5, y54 = dev.taper(x4, y44, cfg.ltpr, cfg.wg, cfg.wr)

  h = [y + ch * (i * 2 - 7) for i in range(8)]

  x1, y71 = dev.sbend(x5, y51, 45, h[6] - y51)
  x1, y74 = dev.sbend(x5, y54, 45, h[1] - y54)
  x2, y72 = dev.sbend(x5, y52, 45, h[2] - y52)
  x2, y73 = dev.sbend(x5, y53, 45, h[5] - y53)

  x6, y71 = dev.taper(x1, y71, cfg.ltpr, cfg.wr, cfg.wg)
  x6, y74 = dev.taper(x1, y74, cfg.ltpr, cfg.wr, cfg.wg)
  x7, y72 = dev.taper(x2, y72, cfg.ltpr, cfg.wr, cfg.wg)
  x7, y73 = dev.taper(x2, y73, cfg.ltpr, cfg.wr, cfg.wg)

  x9, _ = dev.sline(x6, y71, x7 - x6)
  x9, _ = dev.sline(x6, y74, x7 - x6)

  x10, _ = qsk.device(x9, y + yqpsk)
  x10, _ = qsk.device(x9, y - yqpsk)

  x11, x12, ltip = dev.center(idev, x, x10, lchip)

  x13, _ = tip.fiber(x11, y1, ltip, -1)
  x13, _ = tip.fiber(x11, y2, ltip, -1)

  for i in h: x14, _ = tip.diode(x12, i, ltip, 1)

  print('DP-QPSK', round(x12 - x11), round(x14 - x13))

  return x + lchip, y

if __name__ == '__main__':

  chip(0, 0, cfg.size)

  dev.saveas(cfg.work + '8ch')