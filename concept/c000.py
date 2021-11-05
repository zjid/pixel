import cv2
import numpy as np
from domestik import px
skala = px.jendela.skala

h, w = 90, 160
judul = 'sembarang'
skala(judul, [900,1600])
warna = np.random.randint(256, size=3)
dasar = np.zeros([h,w, 3]) + warna
dasar = dasar.astype(np.uint8)

cv2.imshow(judul, dasar)
cv2.displayStatusBar(judul, str(warna))
cv2.waitKey()
cv2.destroyAllWindows()
