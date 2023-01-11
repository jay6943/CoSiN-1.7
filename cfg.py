work = '../mask/SiN-1.7/'
libs = '../mask/SiN-1.7/lib/'

data = []

draft = 'draft' # draft: 100, mask: 1000

phase = 90

wg = 0.8
eg = 30
sg = 6
wr = 1.2
ch = 250
sch = 100

radius = 100

w1x2 = 5.6
l1x2 = 17
d1x2 = 1.46
w2x2 = 8.4
l2x2 = 50
d2x2 = 1.46
lpbs = 10
wpbs = 1.85
ltpr = 5
wtpr = 2
targ = 58
lvoa = 200
spacing = 0.89 # x 2 times
tapping = 2.6

size = 10000
mask = 10900
area = [[1, 0], [-1, 0], [0, 0], [-1, -1], [0, -1]]

layer = {} # 2 for (0, 0) mask position
layer['core'] = 2
layer['clad'] = 2
layer['edge'] = 2
layer['slab'] = 2
layer['sio2'] = 0
layer['fill'] = 2
layer['gold'] = 2
layer['keys'] = 2
layer['bars'] = 2
layer['hole'] = 2
layer['recs'] = 2
layer['text'] = 2
layer['cuts'] = 2