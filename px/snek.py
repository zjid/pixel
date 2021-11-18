import cv2
from numpy import abs, array, clip, ones, zeros, uint8
from numpy.random import choice, randint
from .warna import warna

# Field need to be set as 'arena' object on script.
field = None

# Dictionary of objects.
daftar_kodok = {}
daftar_ular = {}

# 4 directions.
arah = ['atas', 'bawah', 'kiri', 'kanan']

class arena:

  def __init__(self, tinggi, lebar):
    '''Height and width respectively.'''
    self.tinggi, self.lebar = tinggi, lebar
    self.ukuran = array([tinggi, lebar])
    self.luas = tinggi * lebar
    self.arena = zeros([tinggi, lebar, 3], uint8)
    self.update()

  def _keterisian(self):
    '''Pixels occupied by objects.'''
    self.isi_kodok = []
    for dok in daftar_kodok.values():
      self.isi_kodok.append(dok.posisi)
      [y, x] = dok.posisi
      self.next[y, x] = dok.warna
    self.isi_ular = []
    for lar in daftar_ular.values():
      self.isi_ular.extend(lar.tubuh)
      for i,tubuh in enumerate(lar.tubuh[1:]):
        [y, x] = tubuh
        self.next[y, x] = lar.warna_badan[i]
      [y, x] = lar.tubuh[0]
      try: self.next[y, x] = lar.warna_kepala
      except: pass
    self.isi_tembok = []
    self.isi_halangan = self.isi_ular + self.isi_tembok
    self.isi = self.isi_kodok + self.isi_halangan
    self.densitas = len(self.isi) / self.luas
    # self.map_kodok = zeros([self.tinggi, self.lebar], bool)
    # for [y, x] in self.isi_kodok: self.map_kodok[y, x] = True
    # self.map_ular = zeros([self.tinggi, self.lebar], bool)

  def update(self):
    '''Update what's inside the arena.'''
    self.next = self.arena.copy()
    self._keterisian()

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
        return
    self.id = self.__repr__().split('object at ')[-1].replace('>','')
    daftar_kodok.update({self.id: self})
    self.kelincahan = kelincahan
    self.nutrisi = kelincahan + 1
    self.warna = 200 - ones(3, uint8) * kelincahan * 10

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

def ternak_kodok(jumlah, kelincahan = 0):
  '''Put a number of frogs at once arbitrarily.'''
  sebelum = len(daftar_kodok)
  for i in range(jumlah): kodok(kelincahan)
  return len(daftar_kodok) - sebelum

def kodok_lompat():
  '''Simultaneusly call melompat() for all frogs.'''
  [dok.melompat() for dok in daftar_kodok.values()]

class ular:

  def __init__(self, kecerdasan = 1, posisi = []):
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
    self.id = self.__repr__().split('object at ')[-1].replace('>','')
    daftar_ular.update({self.id: self})
    self.tubuh = [self.kepala, self.kepala]
    self.warna_kepala = warna[choice(list(warna.keys()))] + randint(27, size=3)
    self.warna_kepala = uint8(clip(self.warna_kepala, 0, 200))
    self.warna_badan = [ self._catbadan() ]
    self.hidup = True
    self.skor = 0
    self.arah = None
    pilihan_kendali = [self._k_kibor, self._k_acak, self._k_lapar, self._k_nembok]
    self.kecerdasan = kecerdasan
    self.melata = pilihan_kendali[clip(kecerdasan, 0, len(pilihan_kendali)-1)]
    # if kecerdasan > 1:
    self.mogok = False
    self.incaran = None
  
  def _catbadan(self):
    '''Bodypaint the snake neck, body, and tail.'''
    return uint8( clip( self.warna_kepala + randint(60, size=3), 0, 255) )

  def cek(self):
    '''Check if the snake is eating or dead.'''
    # If the snake is eating
    for (i, pos, nut) in [
      (i, dok.posisi, dok.nutrisi) for i, dok in daftar_kodok.items()
    ]:
      if self.kepala == pos:
        self.skor += nut
        self.tubuh.insert(0, self.kepala)
        self.warna_badan.insert(0, self._catbadan())
        daftar_kodok.pop(i)
    # If the snake is dead
    if self.arah and any([
      self.kepala in field.isi_ular,
      self.kepala in field.isi_tembok,
      not field.dalamkah(self.kepala)
    ]):
      self.hidup = False
      self.melata = self._diam
      self.skor -= 1
      for lar in [lar for lar in daftar_ular.values() if lar.kecerdasan == 0]:
        if lar.hidup: lar.skor += 1

  def _gerak(self, arah):
    '''Move to any of 4 directions.'''
    [y, x] = self.kepala
    if arah == 'atas' and self.arah != 'bawah': self.kepala = [y-1, x]
    elif arah == 'bawah' and self.arah != 'atas': self.kepala = [y+1, x]
    elif arah == 'kiri' and self.arah != 'kanan': self.kepala = [y, x-1]
    elif arah == 'kanan' and self.arah != 'kiri': self.kepala = [y, x+1]
    else:
      self.mogok = True
      return
    self.cek()
    if self.hidup:
      self.tubuh.insert(0, self.kepala)
      self.tubuh.pop()
      self.arah = arah

  def _k_kibor(self, tombol):
    '''Receive input from arrow buttons.'''
    if tombol == 82: self._gerak('atas')
    elif tombol == 84: self._gerak('bawah')
    elif tombol == 81: self._gerak('kiri')
    elif tombol == 83: self._gerak('kanan')
    else: self._gerak(self.arah)

  def _k_acak(self, tombol = None):
    '''Dizzy snake.'''
    self._gerak(choice(arah))

  def _mangsa_terdekat(self):
    '''Determine location and distance of the closest prey.'''
    if field.isi_kodok:
      jarak_yx = array(field.isi_kodok) - array(self.kepala)
      jarak_abs = abs(jarak_yx)
      jarak = [dy + dx for [dy, dx] in jarak_abs]
      urut = list(zip(jarak, range(len(jarak))))
      urut.sort()
      return field.isi_kodok[urut[0][1]], jarak_yx[urut[0][1]]
    else: return [0, 0], - array(self.kepala)

  def _k_lapar(self, tombol = None):
    '''Rush to the closest frog.'''
    if not self.mogok:
      (lokasi, terdekat) = self._mangsa_terdekat()
      if abs(terdekat[0]) > abs(terdekat[1]):
        if terdekat[0] < 0: self._gerak('atas')
        else: self._gerak('bawah')
      else:
        if terdekat[1] < 0: self._gerak('kiri')
        else: self._gerak('kanan')
    else:
      self._gerak(choice(arah))
      self.mogok = False

  def _k_nembok(self, tombol = None):
    '''Enjoy the humid obstacles.'''
    # Determine priority directions
    prioritas = []
    (lokasi, terdekat) = self._mangsa_terdekat()
    if terdekat[0] < 0: prioritas.append('atas')
    else: prioritas.append('bawah')
    if terdekat[1] < 0: prioritas.append('kiri')
    else: prioritas.append('kanan')
    # Detect free directions
    bebas = []
    [y, x] = self.kepala
    opsi = [[y-1, x], [y+1, x], [y, x-1], [y, x+1]]
    for i,titik in enumerate(opsi):
      if not titik in field.isi_halangan: bebas.append(arah[i])
    # Compare priority and free
    pilihan = [p for p in prioritas if p in bebas]
    if pilihan:
      self._gerak(choice(pilihan))
    elif bebas:
      self._gerak(choice(bebas))
    else: self._gerak(choice(arah))

  def _k_kelit(self, tombol = None):
    '''Quite smart snake avoid obstacles to the closest frog.'''
    # Am I in the same room with my food?

  def _diam(self, tombol = None): pass

def ternak_ular(jumlah, kecerdasan = 1):
  '''Put a number of snakes at once arbitrarily.'''
  sebelum = len(daftar_ular)
  for i in range(jumlah): ular(kecerdasan)
  return len(daftar_ular) - sebelum

def ular_melata(tombol = None):
  '''Simultaneously call melata(tombol) for all snakes.'''
  [lar.melata(tombol) for lar in daftar_ular.values()]

