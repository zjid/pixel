import cv2
import numpy as np
from numpy.random import randint
from domestik import px

# print(port.jendela.skala)

judul = 'bakteri'
sisi = 60
luas = sisi * sisi

px.jendela.skala(judul, [600,600])
dasar = np.zeros([sisi, sisi], np.uint8)

class sel:
  def __init__(self, y = -1, x = -1, warna = -1):
    if y < 0 or y >= sisi: y = randint(sisi)
    if x < 0 or x >= sisi: x = randint(sisi)
    if warna < 1 or warna > 255: warna = randint(10, 256)
    self.hidup = [ [y,x] ]
    self.mati = []
    self.anggota = self.hidup + self.mati
    self.warna = warna

  def tumbuh(self):
    if self.hidup:
      ruang = []
      for [y,x] in self.hidup:
        arah = [ [y-1,x], [y+1,x], [y,x-1], [y,x+1] ]
        for [q,p] in arah[:]:
          if q < 0 or q >= sisi: arah.remove([q,p])
          elif p < 0 or p >= sisi: arah.remove([q,p])
          elif [q,p] in self.anggota: arah.remove([q,p])
        if arah: ruang += arah
        else:
          self.mati.append([y,x])
          self.hidup.remove([y,x])
      if ruang:
        baru = ruang[randint(len(ruang))]
        self.hidup.append(baru)
        self.anggota.append(baru)
    
bakteri = sel()

while True:
  k = cv2.waitKey(10)
  if k == ord('q'): break

  cawan = dasar.copy()
  for [y,x] in bakteri.anggota:
    cawan[y,x] = bakteri.warna

  cv2.imshow(judul, cawan)
  cv2.displayStatusBar(judul, f'Sel {len(bakteri.anggota)}/{luas}')

  bakteri.tumbuh()

cv2.destroyAllWindows()