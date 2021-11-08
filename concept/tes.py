angka = [1, 2, 3]
huruf = ['a', 'b', 'c']
daftar = zip(angka, huruf)
huruf.reverse()
for kombinasi in daftar:
  print(kombinasi)

import numpy as np
kumpulan = [
  [-5,-5],
  [-5, 5],
  [5, -5],
  [5, 5]
]
acuan = [1,2]
kumpulan = np.array(kumpulan)
acuan = np.array(acuan)
print(kumpulan - acuan)