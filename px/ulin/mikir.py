'''
penguji --> angka 0 atau 1
peserta --> angka 0 atau 1
kebijakan --> angka sama, peserta mendapat poin +1
belajar --> berusaha memberi angka yang sama
'''

import matplotlib.pyplot as plt
from numpy.random import choice

def aksi_tambah(x):
  return x + 1
def aksi_diam(x):
  return x
def aksi_kurang(x):
  return x - 1

def kecenderungan(galat):
  kuadrat = [g * g for g in galat]
  jml0 = sum(kuadrat)
  skor = [jml0 - k for k in kuadrat]
  jml1 = sum(skor)
  return [s / jml1 for s in skor]

class transformasi:
  def __init__(self, a, b):
    self.vmax = max(a, b)
    self.vmin = min(a, b)
    self.vrange = self.vmax - self.vmin
  def normal(self, v):
    return (v - self.vmin) / self.vrange
  def abnormal(self, n):
    return n * self.vrange + self.vmin

aksi = [aksi_tambah, aksi_diam, aksi_kurang]
# aksi = enumerate(aksi)

x = 0
# y = int(input('Nilai target = '))
y = 10
trans = transformasi(x, y)

e = trans.normal(y - x)
galat = [e, e, e]

attempt = 0
# for i in range(20):
while True:
  if abs(y - x) > 0.01:
    b = choice(range(3), p=kecenderungan(galat))
    x = aksi[b](x)
    galat[b] = trans.normal(y - x)
    attempt += 1
  else: break

print(y, x, galat, attempt)