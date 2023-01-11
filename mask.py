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
import voa
import q2x2
import y1x2
import y2x2

# key.frame(layer, quadrant, key position)
# 'recs' layer : stress released patterns
# 'fill' layer : filled with soild
# 'none' layer : not filled

xo = key.xorg
yo = key.yorg

def mask_1(fp):

  key.frame(1, 1)
  key.frame(2, 2)
  tip.scuts(xo, yo)
  dev.cover(xo, yo, 'fill')

  cfg.layer['core'] = 1
  cfg.layer['edge'] = 1
  cfg.layer['sio2'] = 0
  cfg.layer['recs'] = 1

  _, y1 = tip.chip(xo, yo + cfg.sch, cfg.size, 0.36)
  _, y1 = ohm.chips(xo, yo + cfg.sch * 2)
  _, y1 = y1x2.chips(xo, y1 + cfg.sch * 3, dev.arange(16, 18, 1))
  _, y1 = y2x2.chips(xo, y1 + cfg.sch * 1.5, dev.arange(48, 52, 0.5))
  _, y1 = dci.chips(xo, y1 + cfg.sch, dev.arange(0.86, 0.92, 0.01))
  _, y1 = tip.chips(xo, y1 + cfg.sch, dev.arange(0.2, 0.4, 0.02))
  _, y1 = ssc.chips(xo, y1 + cfg.sch, dev.arange(500, 900, 50))
  _, y1 = tap.chips(xo, y1 + cfg.sch, dev.arange(2.2, 2.8, 0.2))
  _, y1 = tip.chip(xo, yo + cfg.size - cfg.sch, cfg.size, 0.36)

  dxf.conversion(fp)

def mask_2_hybrid(fp):

  key.frame(2, 1)
  tip.scuts(xo, yo)
  dev.cover(xo, yo, 'fill')

  cfg.layer['core'] = 2
  cfg.layer['edge'] = 2
  cfg.layer['recs'] = 2
  
  _, y1 = tip.chip(xo, yo + cfg.sch, cfg.size, 0.36)
  _, y1 = y2x2.chip(xo, y1 + cfg.sch * 1.5, cfg.size)
  _, y1 = q2x2.chip(xo, y1 + cfg.sch * 0.5 + cfg.ch, cfg.size)
  _, y1 = qdc.chip(xo, y1 + cfg.ch, cfg.size)
  _, y1 = qsk.chips(xo, y1 + cfg.ch, dev.arange(84, 96, 3))
  _, y1 = q2x2.chip(xo, y1 + cfg.ch, cfg.size)
  _, y1 = voa.chips(xo, y1 + cfg.ch * 2.5, dev.arange(200, 500, 100))
  _, y1 = y2x2.chip(xo, y1 + cfg.ch * 3, cfg.size)
  _, y1 = tip.chip(xo, yo + cfg.size - cfg.sch, cfg.size, 0.36)
  
  dxf.conversion(fp)

def mask_3_pbs(fp):

  key.frame(3, 1)
  key.frame(4, 2)
  tip.scuts(xo, yo)
  dev.cover(xo, yo, 'fill')

  cfg.layer['core'] = 3
  cfg.layer['edge'] = 3
  cfg.layer['sio2'] = 0
  cfg.layer['recs'] = 3

  _, y1 = tip.chip(xo, yo + cfg.sch, cfg.size, 0.36)
  _, y1 = pbs.chips(xo, y1 + cfg.sch, dev.arange(10, 50, 2))
  _, y1 = tip.chip(xo, yo + cfg.size - cfg.sch, cfg.size, 0.36)

  dxf.conversion(fp)

def mask_4_icr(fp):

  key.frame(4, 1)
  tip.scuts(xo, yo)
  dev.cover(xo, yo, 'fill')

  cfg.layer['core'] = 4
  cfg.layer['edge'] = 4
  cfg.layer['gold'] = 0
  cfg.layer['recs'] = 4

  icr.chips(xo, yo + cfg.size * 0.5)

  dxf.conversion(fp)

def mask_4_key(fp):

  key.frame(4, 1)
  dev.cover(key.xorg, key.yorg, 'none')

  cfg.layer['core'] = 4

  key.contact_align_keys('core', key.xorg, key.yorg, 1)

  dxf.conversion(fp)

if __name__ == '__main__':

  cfg.draft = 'mask' # draft or mask

  fp = dxf.start(cfg.work + cfg.draft)
  key.cross(0, 0)
  dxf.conversion(fp)

  ok = 0
  
  if ok == 0 or ok == 1: mask_1(fp)
  if ok == 0 or ok == 2: mask_2_hybrid(fp)
  if ok == 0 or ok == 3: mask_3_pbs(fp)
  if ok == 0 or ok == 4: mask_4_key(fp)

  dxf.close(fp)
  dev.removes('__pycache__/')