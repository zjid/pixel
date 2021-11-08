import cv2
from domestik import px

sawah = px.snek.field = px.snek.arena(90, 90)
judul = 'ular oop'
px.jendela.skala(judul, 10 * sawah.ukuran)
cv2.imshow(judul, sawah.arena)
print(px.snek.ternak_kodok(5))
print(px.snek.ternak_kodok(5, 1))
print(px.snek.ternak_kodok(5, 2))
print(px.snek.ternak_kodok(5, 3))

while True:
  k = cv2.waitKey(200)
  if k == ord('q'): break

  cv2.imshow(judul, sawah.next)
  px.snek.kodok_lompat()
  sawah.update()

cv2.destroyAllWindows()

