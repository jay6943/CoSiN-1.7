import cfg
import dxf
import dev
import key
import ohm
import pbs
import psk
import tip
import ssc
import tap
import icr
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
  tip.scuts(xk, yk)
  dev.cover(xk, yk, 'block')

  cfg.layer['core'] = 1
  cfg.layer['edge'] = 1
  cfg.layer['cuts'] = 1
  cfg.layer['tops'] = 1
  cfg.layer['sio2'] = 0
  cfg.layer['recs'] = 1

  _, y1 = ohm.chips(xk, yk + 200)
  _, y1 = tip.chips(xk, y1 + 200, dev.arange(0.2, 0.4, 0.02))
  _, y1 = y1x2.chips(xk, y1, dev.arange(15, 20, 1))
  _, y1 = y2x2.chips(xk, y1 + 50, dev.arange(48, 53, 0.5))
  _, y1 = ssc.chips(xk, y1 - 50, dev.arange(600, 900, 50))
  _, y1 = tap.chips(xk, y1 - 200, dev.arange(2, 4, 1))

  dxf.conversion(fp)

def mask_2(fp):

  key.frame(2, 1)
  tip.scuts(xk, yk)
  dev.cover(xk, yk, 'block')

  cfg.layer['core'] = 2
  cfg.layer['edge'] = 2
  cfg.layer['cuts'] = 2
  cfg.layer['tops'] = 2
  cfg.layer['recs'] = 2
  
  _, y1 = pbs.chips(xk, yk + cfg.ch , dev.arange(54.5, 57.5, 1))
  _, y1 = psk.chips(xk, y1 + cfg.ch * 2.5, dev.arange(77.5, 95, 2.5))
  
  dxf.conversion(fp)

def mask_3(fp):

  key.frame(3, 1)
  tip.scuts(xk, yk)
  dev.cover(xk, yk, 'none')

  cfg.layer['core'] = 3
  cfg.layer['edge'] = 3
  cfg.layer['cuts'] = 3
  cfg.layer['tops'] = 3
  cfg.layer['recs'] = 3

  pbs.chips(xk, yk + cfg.ch, dev.arange(30, 80, 2))

  dxf.conversion(fp)

def mask_4(fp):

  key.frame(4, 1)
  tip.scuts(xk, yk)
  dev.cover(xk, yk, 'block')

  cfg.layer['core'] = 4
  cfg.layer['edge'] = 4
  cfg.layer['gold'] = 0
  cfg.layer['cuts'] = 4
  cfg.layer['tops'] = 4
  cfg.layer['recs'] = 4

  icr.chips(xk, yk + cfg.size * 0.5)

  dxf.conversion(fp)

if __name__ == '__main__':

  cfg.draft = 'draft' # draft or mask

  fp = dxf.start(cfg.work + cfg.draft)
  key.cross(0, 0)
  dxf.conversion(fp)

  ok = 4
  
  if ok == 0 or ok == 1: mask_1(fp)
  if ok == 0 or ok == 2: mask_2(fp)
  if ok == 0 or ok == 3: mask_3(fp)
  if ok == 0 or ok == 4: mask_4(fp)

  dxf.close(fp)
  dev.removes('__pycache__/')