import cfg
import dxf
import dev
import key
import ohm
import pbs
import qsk
import tip
import ssc
import tap
import icr
import dci
import qdc
import q2x2
import y1x2
import y2x2

# key.frame(layer, quadrant, key position)
# 'recs' layer : stress released patterns
# 'fill' layer : filled with soild
# 'none' layer : not filled

xk = key.wbar + key.wkey
yk = key.wbar + key.wkey

def mask_1(fp):

  key.frame(1, 1)
  key.frame(2, 2)
  tip.scuts(xk, yk)
  dev.cover(xk, yk, 'block')

  cfg.layer['core'] = 1
  cfg.layer['edge'] = 1
  cfg.layer['sio2'] = 0
  cfg.layer['recs'] = 1

  _, y1 = ohm.chips(xk, yk + 200)
  _, y1 = y1x2.chips(xk, y1 + 300, dev.arange(16, 18, 1))
  _, y1 = y2x2.chips(xk, y1 + 50, dev.arange(49, 53, 0.5))
  _, y1 = dci.chips(xk, y1, dev.arange(0.86, 0.92, 0.01))
  _, y1 = tip.chips(xk, y1 - 50, dev.arange(0.2, 0.4, 0.02))
  _, y1 = ssc.chips(xk, y1, dev.arange(600, 900, 50))
  _, y1 = tap.chips(xk, y1 + 50, dev.arange(1.16, 1.46, 0.1))
  _, y1 = dev.sline(xk, y1 - 50, cfg.size)

  dxf.conversion(fp)

def mask_2(fp):

  key.frame(2, 1)
  tip.scuts(xk, yk)
  dev.cover(xk, yk, 'block')

  cfg.layer['core'] = 2
  cfg.layer['edge'] = 2
  cfg.layer['recs'] = 2
  
  _, y1 = pbs.chips(xk, yk + cfg.ch , dev.arange(54.5, 57.5, 1))
  _, y1 = qsk.chips(xk, y1 + cfg.ch * 2.5, dev.arange(77.5, 95, 2.5))
  
  dxf.conversion(fp)

def mask_3(fp):

  key.frame(3, 1)
  key.frame(4, 2)
  tip.scuts(xk, yk)
  dev.cover(xk, yk, 'none')

  cfg.layer['core'] = 3
  cfg.layer['edge'] = 3
  cfg.layer['sio2'] = 0
  cfg.layer['recs'] = 3

  pbs.chips(xk, yk + cfg.ch, dev.arange(40, 80, 2))

  dxf.conversion(fp)

def mask_4(fp):

  key.frame(4, 1)
  tip.scuts(xk, yk)
  dev.cover(xk, yk, 'block')

  cfg.layer['core'] = 4
  cfg.layer['edge'] = 4
  cfg.layer['gold'] = 0
  cfg.layer['recs'] = 4

  icr.chips(xk, yk + cfg.size * 0.5)

  dxf.conversion(fp)

def mask_4_icr(fp):

  key.frame(4, 1)
  tip.scuts(xk, yk)
  dev.cover(xk, yk, 'block')

  cfg.layer['core'] = 4
  cfg.layer['edge'] = 4
  cfg.layer['gold'] = 0
  cfg.layer['recs'] = 4

  icr.chips(xk, yk + cfg.size * 0.5)

  dxf.conversion(fp)

if __name__ == '__main__':

  cfg.draft = 'draft' # draft or mask

  fp = dxf.start(cfg.work + cfg.draft)
  key.cross(0, 0)
  dxf.conversion(fp)

  ok = 0
  
  if ok == 0 or ok == 1: mask_1(fp)
  if ok == 0 or ok == 2: mask_2(fp)
  if ok == 0 or ok == 3: mask_3(fp)
  if ok == 0 or ok == 4: mask_4(fp)

  dxf.close(fp)
  dev.removes('__pycache__/')