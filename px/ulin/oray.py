# Initialize
sawah = None

# Constants
arah = ['atas', 'bawah', 'kiri', 'kanan']
warna = []

# Global variables
daftar_kodok = {}
daftar_ular = {}

class arena:
  def __init__(self):
    # Specifications
    self.tinggi
    self.lebar
    self.ukuran
    self.luas
    # Arrays of base and show
    self.dasar
    self.tampil
    # List of occupied points
    self.isi_kodok
    self.isi_ular
    self.isi_tembok
    self.isi_halangan
    self.isi
    # Stats
    self.densitas
    # Sensing methods
    self.didalamkah()
    self.nabrakkah()
    # Actions
    self.nembok() # Consider dead snakes as walls

class kodok:
  def __init__(self):
    # State
    self.posisi
    # Specification
    self.kelincahan
    self.nutrisi
    self.warna
    # Actions
    self.registrasi()
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