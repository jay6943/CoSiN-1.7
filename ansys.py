import cfg
import dev

lwg = 10

def angle_45():
  
  x, y = dev.sline(0, 0, lwg)
  x, y = dev.sbend(x, y, 125, 45, 0, 1)
  x, y = dev.sline(x, y, lwg)

  print('ANSYS Euler s-bend ...')
  dev.saveas('45')

def angle_45_taper():
  
  x, y = dev.srect(0, 0, lwg, cfg.wt)
  x, y = dev.taper(x, y, cfg.ltpr, cfg.wt, cfg.wg)
  x, y = dev.sbend(x, y, cfg.ch * 0.5, 45, 0, 1)
  x, y = dev.taper(x, y, cfg.ltpr, cfg.wg, cfg.wt)
  x, y = dev.srect(x, y, lwg, cfg.wt)

  print('ANSYS Euler s-bend ...')
  dev.saveas('45-taper')

def angle_90():

  x, y = dev.sline(0, 0, lwg)
  x, y = dev.bends(x, y, 90, 0, 1)
  x, y = dev.tline(x, y, lwg)

  print('ANSYS Euler bend with 90-deg rotation ...')
  dev.saveas('90')

def angle_180():

  x, y = dev.sline(0, 0, lwg)
  x, y = dev.bends(x, y, 180, 0, 1)
  x, y = dev.sline(x, y, -lwg)

  print('ANSYS Euler bend with 180-deg rotation ...')
  dev.saveas('180')

def angle_180_taper():

  x, y = dev.srect(0, 0, lwg, cfg.wt)
  x, y = dev.taper(x, y, cfg.ltpr, cfg.wt, cfg.wg)
  x, y = dev.bends(x, y, 180, 0, 1)
  x, y = dev.taper(x, y, -cfg.ltpr, cfg.wg, cfg.wt)
  x, y = dev.srect(x, y, -lwg, cfg.wt)

  print('ANSYS Euler bend with 180-deg rotation ...')
  dev.saveas('180-taper')

def angle_90x2():
  
  x, y = dev.sline(0, 0, lwg)
  x, y = dev.bends(x, y, 90, 0, 1)
  x, y = dev.tline(x, y, lwg)
  x, y = dev.bends(x, y, 90, 90, 1)
  x, y = dev.sline(x, y, -lwg)

  print('ANSYS Euler bend with 2 x 90-deg rotation ...')
  dev.saveas('90x2')

if __name__ == '__main__':

  cfg.work = 'D:/ansys/Euler/'

  cfg.draft = 'mask'

  # angle_45()
  # angle_90()
  # angle_180()
  # angle_90x2()

  angle_180_taper()