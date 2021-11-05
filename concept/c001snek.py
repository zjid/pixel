import cv2
import numpy as np
from sys import argv
from domestik import px as pixel
skala = pixel.jendela.skala

noarg = len(argv)
if noarg == 2:
  h = w = int(argv[1])
elif noarg > 2:
  h, w = int(argv[1]), int(argv[2])
else:
  h = w = 90
py, px = int(h/2), int(w/2)

nol = np.zeros([h, w, 3], np.uint8)
judul = 'ular'
skala(judul, [10 * h, 10 * w])

snek = [[py, px], [py, px]]
last_move = None
move = None
rat = False
skor = 0
paused = False

while True:
  if paused: t = 0
  else: t = max(1, 100-skor)
  k = cv2.waitKey(t)
  paused = False
  if k == ord('q'): break
  elif k == ord('p'): paused = not paused
  elif k == 82:
    if last_move != 'down': move = 'up'
  elif k == 84:
    if last_move != 'up': move = 'down'
  elif k == 81:
    if last_move != 'right': move = 'left'
  elif k == 83:
    if last_move != 'left': move = 'right'
  
  [y0,x0] = snek[0]
  if move == 'up':
    snek.insert(0, [y0-1, x0])
    snek.pop()
  elif move == 'down':
    snek.insert(0, [y0+1, x0])
    snek.pop()
  elif move == 'left':
    snek.insert(0, [y0, x0-1])
    snek.pop()
  elif move == 'right':
    snek.insert(0, [y0, x0+1])
    snek.pop()
  last_move = move

  py = snek[0][0]
  px = snek[0][1]
  if sum([py < 0, py >= h, px < 0, px >= w, [py,px] in snek[2:]]):
    break

  nol_ = nol.copy()
  
  if not rat:
    rat_count = skor // 10 + 1
    rats = []
    while True:
      ry, rx = np.random.randint(0, h-1), np.random.randint(0, w-1)
      if not ( [ry, rx] in snek or [ry, rx] in rats ): rats.append([ry, rx])
      if len(rats) == rat_count: break
    rat = True
  else:
    for [ry, rx] in rats:
      nol_[ry, rx] = [100,100,255]
    if [py, px] in rats:
      snek.insert(0, [py,px])
      rats.remove([py, px])
      skor += 1
      if len(rats) == 0: rat = False

  for i,[ny, nx] in enumerate(snek):
    if i > 0: nol_[ny, nx] = [150,255,150]
    else: nol_[ny, nx] = [50,255,50]
  
  cv2.imshow(judul, nol_)
  teks = f'skor = {skor}'
  if paused: teks += ', press any key to unpause.'
  cv2.displayStatusBar(judul, teks)

print(f'Skor akhir {skor}')
cv2.imshow(judul, nol_)
cv2.displayStatusBar(judul, f'game over, skor = {skor}')
cv2.waitKey()
cv2.destroyAllWindows()