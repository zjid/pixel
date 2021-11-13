import cv2
from domestik import px

sawah = px.snek.field = px.snek.arena(180, 320)
judul = 'ular oop'
px.jendela.skala(judul, geser=[0, 1920])
cv2.imshow(judul, sawah.arena)

def muncul():
  u, k = 0, 0
  if sum([lar.kecerdasan for lar in px.snek.daftar_ular.values() if lar.hidup]) < 5:
    px.snek.ternak_ular(1)
    px.snek.ternak_ular(1, 2)
    px.snek.ternak_ular(1, 3)
    u = 3
  if not sawah.isi_kodok:
    px.snek.ternak_kodok(2)
    px.snek.ternak_kodok(1, 1)
    px.snek.ternak_kodok(1, 2)
    k = 4
  return u, k

total_ular, total_kodok = 0, 0
u, k = muncul()
total_ular += u
total_kodok += k
sawah.update()

while True:
  
  k = cv2.waitKey(1)
  if k == ord('q'): break

  u, k = muncul()
  total_ular += u
  total_kodok += k
  teks = f'Total {total_ular} ular dan {total_kodok} kodok.'

  cv2.imshow(judul, sawah.next)
  cv2.displayStatusBar(judul, teks)
  px.snek.kodok_lompat()
  px.snek.ular_melata(k)
  sawah.update()

print(teks)
cv2.waitKey()
cv2.destroyAllWindows()

