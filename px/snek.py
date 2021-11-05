import cv2
from numpy import array, clip, ones, zeros, uint8
from numpy.random import choice, randint
from .warna import warna

# Field need to be set as 'arena' object on script.
field = None

# Dictionary of objects.
daftar_kodok = {}
daftar_ular = {}

class arena:

  def __init__(self, tinggi, lebar):
    '''Height and width respectively.'''
    self.tinggi, self.lebar = tinggi, lebar
    self.ukuran = array([tinggi, lebar])
    self.luas = tinggi * lebar
    self.arena = zeros([tinggi, lebar, 3], uint8)

  def _keterisian(self):
    '''Pixels occupied by objects.'''
    self.isi_kodok = [dok.posisi for dok in daftar_kodok.values()]
    self.isi_ular = []
    for lar in daftar_ular.values():
      self.isi_ular += lar.tubuh
    self.isi_tembok = []
    self.isi = self.isi_kodok + self.isi_ular + self.isi_tembok
    self.densitas = len(self.isi) / self.luas
    self.map_kodok = zeros([self.tinggi, self.lebar], bool)
    for [y, x] in self.isi_kodok: self.map_kodok[y, x] = True
    # self.map_ular = zeros([self.tinggi, self.lebar], bool)

  def update(self):
    '''Update what's inside the arena.'''
    self._keterisian()
    self.next = self.arena.copy()

  def dalamkah(self, posisi):
    '''Identify if a position is inside arena.'''
    [y, x] = posisi
    return all([ 0 <= y < self.tinggi, 0 <= x < self.lebar ])

class kodok:

  def __init__(self, kelincahan = 0, posisi = []):
    '''Put a frog with agility at position [y,x].'''
    if posisi:
      self.posisi = posisi
    else:
      dapat = False
      for i in range(10):
        y, x = randint(field.tinggi), randint(field.lebar)
        if not [y, x] in field.isi:
          self.posisi = [y, x]
          dapat = True
          break
      if not dapat:
        print('[W] Failed to put a new frog.')
        return 0
    self.id = self.__repr__().split('object at ')[-1].replace('>','')
    daftar_kodok.update({self.id: self})
    self.kelincahan = kelincahan
    self.nutrisi = kelincahan + 1
    self.warna = 200 - ones(3, uint8) * kelincahan * 10
    return 1

  def melompat(self):
    '''The frog jumps or not.'''
    if self.kelincahan < 1: return
    tujuan = [ self.posisi ]
    [y, x] = self.posisi
    for i in range(1, self.kelincahan + 1):
      for titik in [ [y-i,x], [y+i,x], [y,x-i], [y,x+i] ]:
        if field.dalamkah(titik) and not titik in field.isi:
          tujuan.append(titik)
    self.posisi = tujuan[randint(len(tujuan))]

class ular:

  def __init__(self, posisi = []):
    '''Put a snake at position [y,x].'''
    if posisi:
      self.kepala = posisi
    else:
      dapat = False
      for i in range(10):
        y, x = randint(field.tinggi), randint(field.lebar)
        if not [y, x] in field.isi:
          self.kepala = [y, x]
          dapat = True
          break
      if not dapat:
        print('[W] Failed to put a new snake.')
        return 0
    self.id = self.__repr__().split('object at ')[-1].replace('>','')
    daftar_ular.update({self.id: self})
    self.tubuh = [self.kepala, self.kepala]
    self.warna_kepala = warna[choice(list(warna.keys()))] + randint(27, size=3)
    self.warna_kepala = uint8(clip(self.warna_kepala, 0, 227))
    self.warna_badan = [ self._catbadan() ]
    self.gerak = True
    self.skor = 0

  def update(self):
    '''Check if the snake is eating or dead.'''
    # If the snake is eating
    for i, dok in daftar_kodok.items():
      if self.kepala == dok.posisi:
        self.skor += dok.nutrisi
        self.tubuh.insert(0, self.kepala)
        self.warna_badan.insert(0, self._catbadan())

  def _catbadan(self):
    '''Bodypaint the snake neck, body, and tail.'''
    return uint8( self.warna_kepala + randint(27, size=3) )

def ternak_kodok(jumlah, kelincahan = 0):
  '''Put a number of frogs at once arbitrarily.'''
  penambahan = 0
  for i in range(jumlah): penambahan += kodok(kelincahan)
  return penambahan

def kodok_lompat():
  '''Simultaneusly call melompat() for all frogs.'''
  [dok.melompat() for dok in daftar_kodok.values()]

