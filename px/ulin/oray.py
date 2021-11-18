from numpy.random import choice, randint
from numpy import abs, array, clip, ones, zeros, uint8

# Initialize
tinggi_sawah = 60
lebar_sawah = 60

# Constants
arah = ['atas', 'bawah', 'kiri', 'kanan']
warna = []

# Global variables
daftar_kodok = {}
daftar_ular = {}

class arena:

  def __init__(self, tinggi, lebar):
    '''Height and width respectively.'''
    # Specifications: [height, width] and area
    self.tinggi, self.lebar = tinggi, lebar
    self.ukuran = array([tinggi, lebar])
    self.luas = tinggi * lebar
    # Arrays of base and show
    self.dasar = zeros([tinggi, lebar, 3], uint8)
    self.tampil = self.dasar.copy()
    # List of occupied points
    self.isi_kodok = []
    for dok in daftar_kodok.values():
      self.isi_kodok.append(dok.posisi)
      [y, x] = dok.posisi
      self.tampil[y, x] = dok.warna
    self.isi_ular = []
    for lar in daftar_ular.values():
      self.isi_ular.extend(lar.tubuh)
      for i, tubuh in enumerate(lar.tubuh[1:]):
        [y, x] = tubuh
        self.tampil[y, x] = lar.warna_badan[i]
      [y, x] = lar.tubuh[0]
      try: self.tampil[y, x] = lar.warna_kepala
      except: pass
    self.isi_tembok = []
    self.isi_halangan = self.isi_ular + self.isi_tembok
    self.isi = self.isi_kodok + self.isi_halangan
    # Stats
    self.densitas = len(self.isi) / self.luas
    # Sensing methods
    def didalamkah(): pass
    def nabrakkah(): pass # Called by frog and snake objects.
    # Actions
    def nembok():
      '''Snake corpses become obstacles.'''
      # Find dead snakes.
      pass # Consider dead snakes as walls.

sawah = arena(tinggi_sawah, lebar_sawah)

def registrasi(obj, kamus):
  '''Register object into dictionary.'''
  kamus.update({id(obj): obj})

class kodok:
  def __init__(self, kelincahan = 0, posisi = []):
    '''Put a frog with agility at position [y, x].'''
    # State
    if posisi: self.posisi = posisi
    else:
      dapat = False
      for i in range(10):
        y, x = randint(sawah.tinggi), randint(sawah.lebar)
    # State
    self.posisi
    # Specification
    self.kelincahan
    self.nutrisi
    self.warna
    # Actions
    self.melompat()

class ular:
  def __init__(self):
    # State
    self.kepala
    self.tubuh
    self.hidup
    self.skor
    self.arah
    self.incaran
    self.mogok
    # Specification
    self.warna_kepala
    self.warna_badan
    self.kecerdasan
    # Actions
    self.registrasi()
    self.catbadan()
    self.mikir()
    self.melata()
    # Sensing
    self.makankah()
    self.matikah()
    self.carimangsa()


# Global actions
def ternak_kodok(): pass
def ternak_ular(): pass
def kodok_lompat(): pass
def ular_melata(): pass
def update(): pass # Call all action functions and methods.