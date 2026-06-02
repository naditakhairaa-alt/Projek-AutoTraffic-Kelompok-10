# 9. Tree - Klasifikasi Kendaraan

# Hierarki klasifikasi kendaraan:

#              [Kendaraan]                 <- root
#             /     |     \
#      [Darurat]  [Umum]  [Pribadi]        <- level 1 (kategori)
#        /       /   \         /  \
#  [ambulans] [bus] [truk] [mobil] [motor] <- level 2 (jenis)
#               |
#          [V-0001, V-0002, ...]           <- level 3 (kendaraan aktual)

class NodeTree:
    def __init__(self, label, tipe="kategori"):
        self.label    = label       # nama node, misal "Darurat" / "ambulans" / "V-0001"
        self.tipe     = tipe        # "root" | "kategori" | "jenis" | "kendaraan"
        self.anak     = []          # list NodeTree (N-ary)
        self.vehicle  = None        # diisi jika tipe == "kendaraan"

    def tambah_anak(self, node):
        self.anak.append(node)
        return node

class TreeKlasifikasi:
    KATEGORI_MAP = {
        "ambulans": "Darurat",
        "bus"     : "Umum",
        "truk"    : "Umum",
        "mobil"   : "Pribadi",
        "motor"   : "Pribadi",
    }

    def __init__(self):
        # Bangun kerangka tree saat inisialisasi
        self.root = NodeTree("Semua Kendaraan", "root")

        # Level 1: kategori
        self._darurat = self.root.tambah_anak(NodeTree("Darurat",  "kategori"))
        self._umum    = self.root.tambah_anak(NodeTree("Umum",     "kategori"))
        self._pribadi = self.root.tambah_anak(NodeTree("Pribadi",  "kategori"))

        # Level 2: jenis (daun struktur, anak dari kategori)
        self._jenis = {}
        for jenis, kat_nama in self.KATEGORI_MAP.items():
            kat_node = {
                "Darurat" : self._darurat,
                "Umum"    : self._umum,
                "Pribadi" : self._pribadi,
            }[kat_nama]
            node = kat_node.tambah_anak(NodeTree(jenis, "jenis"))
            self._jenis[jenis] = node

    def tambah_vehicle(self, vehicle):
        # sisipkan kendaraan ke node jenis yang sesuai
        jenis_node = self._jenis.get(vehicle.jenis)
        if jenis_node is None:
            return
        node_v        = NodeTree(vehicle.vid, "kendaraan")
        node_v.vehicle = vehicle
        jenis_node.tambah_anak(node_v)

    def hapus_vehicle(self, vid):
        # hapus kendaraan dari tree berdasarkan vid dengan rekursif
        self._hapus_rekursif(self.root, vid)

    def _hapus_rekursif(self, node, vid):
        # hapus anak yang labelnya = vid, dengan rekursif
        node.anak = [a for a in node.anak if a.label != vid]
        for anak in node.anak:
            self._hapus_rekursif(anak, vid)

    def bangun_ulang(self, semua_vehicle):
        # bersihkan semua kendaraan lama dan isi ulang dari list baru
        # dengan menghapus semua node kendaraan (level 3) dari setiap node jenis
        for jenis_node in self._jenis.values():
            jenis_node.anak = []
        # Isi ulang
        for v in semua_vehicle:
            self.tambah_vehicle(v)

    def hitung_total(self, node=None):
        # hitung jumlah node bertipe 'kendaraan' di bawah node,
        # tanpa memanggil argumen dan hitung dari root.
        if node is None:
            node = self.root
        if node.tipe == "kendaraan":
            return 1
        total = 0
        for anak in node.anak:
            total += self.hitung_total(anak)
        return total

    def cari_jenis(self, jenis):
        # return node jenis tertentu (rekursif DFS dari root)
        return self._cari_rekursif(self.root, jenis)

    def _cari_rekursif(self, node, target_label):
        # rekursif DFS untuk mencari node berdasarkan label
        if node.label == target_label and node.tipe == "jenis":
            return node
        for anak in node.anak:
            hasil = self._cari_rekursif(anak, target_label)
            if hasil:
                return hasil
        return None

    def tampilkan(self, node=None, prefix="", adalah_terakhir=True):
        # cetak tree secara visual dengan karakter ASCII (rekursif)
        '''
        Contoh output:
          Semua Kendaraan (5)
          ├── Darurat (1)
          │   └── ambulans (1)
          │       └── V-0003
          ├── Umum (2)
          ...
        '''

        if node is None:
            node = self.root

        # tentukan karakter cabang
        konektor = "└── " if adalah_terakhir else "├── "
        if node == self.root:
            konektor = ""
            prefix   = ""

        # label + jumlah kendaraan jika bukan node kendaraan
        if node.tipe == "kendaraan":
            label_tampil = node.label
            if node.vehicle:
                label_tampil += f"  ({node.vehicle.jenis}, {node.vehicle.kecepatan}km/h)"
        else:
            jumlah = self.hitung_total(node)
            label_tampil = f"{node.label}  [{jumlah} kendaraan]"

        print(f"  {prefix}{konektor}{label_tampil}")

        # rekursif ke anak-anak
        for i, anak in enumerate(node.anak):
            adalah_anak_terakhir = (i == len(node.anak) - 1)
            if node == self.root:
                prefix_baru = ""
            else:
                prefix_baru = prefix + ("    " if adalah_terakhir else "│   ")
            self.tampilkan(anak, prefix_baru, adalah_anak_terakhir)