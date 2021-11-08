import cv2
from domestik import px

sawah = px.snek.field = px.snek.arena(900, 1600)
judul = 'ular oop'
px.jendela.skala(judul, geser=[0, 1920])
cv2.imshow(judul, sawah.arena)

mc = px.snek.ular(0, [sawah.tinggi//2, sawah.lebar//2])
lawan = px.snek.ular(2)
px.snek.ternak_ular(3, 2)
px.snek.ternak_kodok(3)
sawah.update()

while True:
  skor_lawan = sum([lar.skor for lar in px.snek.daftar_ular.values()]) - mc.skor
  ada_lawan = sum([lar.hidup for lar in px.snek.daftar_ular.values()]) - 1

  t = max(1, 100 - max(mc.skor, skor_lawan))
  k = cv2.waitKey(t)
  if k == ord('q'): break

  if not sawah.isi_kodok:
    px.snek.ternak_kodok(2, 2)
    px.snek.ternak_kodok(2, 1)
    px.snek.ternak_kodok(2)

  if ada_lawan < 1:
    px.snek.ternak_ular(2, 2)
    px.snek.ternak_ular(3)

  cv2.imshow(judul, sawah.next)
  cv2.displayStatusBar(judul, f'skor kamu / skor lawan = {mc.skor} / {skor_lawan}')
  px.snek.kodok_lompat()
  px.snek.ular_melata(k)
  # print(k, mc.hidup, mc.arah, mc.kepala, mc.tubuh)
  # print(lawan.hidup, lawan.arah, lawan.kepala)
  sawah.update()

print(f'Skor kamu {mc.skor} / skor lawan {skor_lawan}')
cv2.waitKey()
cv2.destroyAllWindows()

