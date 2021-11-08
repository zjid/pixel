import cv2
from domestik import px

sawah = px.snek.field = px.snek.arena(90, 90)
judul = 'ular oop'
px.jendela.skala(judul, 10 * sawah.ukuran)
cv2.imshow(judul, sawah.arena)
px.snek.ternak_ular(1)

while True:
  k = cv2.waitKey(500)
  if k == ord('q'): break

  cv2.imshow(judul, sawah.next)
  px.snek.ular_melata()
  sawah.update()

cv2.destroyAllWindows()

