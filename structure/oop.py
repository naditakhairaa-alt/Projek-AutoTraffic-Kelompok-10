# 1. OOP - Dasaar menggunakan @staticmethod

import time

class Kendaraan:
    """
    Representasi satu kendaraan di persimpangan.
    Atribut: ID unik, jenis, kecepatan, waktu_masuk, waktu_tunggu.
    """
    kendaraan = ("mobil", "motor", "truk", "bus", "ambulans")

    def __init__(self, vid, jenis="mobil", kecepatan=60):
        if jenis not in self.kendaraan:
            raise ValueError(f"Jenis kendaraan tidak valid: {jenis}")
        self.vid          = vid           # ID unik, contoh: "V-001"
        self.jenis        = jenis
        self.kecepatan    = kecepatan     # km/jam
        self.waktu_masuk  = time.time()   # timestamp saat masuk antrian
        self.waktu_tunggu = 0             # detik menunggu (diupdate simulasi)
        self.jalur        = None          # nama jalur (diset saat join lane)
        self.sudah_lewat  = False         # flag: sudah melewati persimpangan

    def update_tunggu(self):
        """Perbarui waktu tunggu berdasarkan waktu sejak masuk."""
        if not self.sudah_lewat:
            self.waktu_tunggu = time.time() - self.waktu_masuk

    def prioritas(self):
        """Kendaraan darurat (ambulans/bus) dapat prioritas tinggi."""
        return 0 if self.jenis in ("ambulans",) else 1

    def __str__(self):
        return (f"[{self.vid}] {self.jenis.upper():<8} "
                f"v={self.kecepatan}km/h  "
                f"tunggu={self.waktu_tunggu:.1f}s")

    def ke_dict(self):
        return {
            "vid"          : self.vid,
            "jenis"        : self.jenis,
            "kecepatan"    : self.kecepatan,
            "waktu_masuk"  : self.waktu_masuk,
            "waktu_tunggu" : self.waktu_tunggu,
            "jalur"        : self.jalur,
            "sudah_lewat"  : self.sudah_lewat,
        }

    @staticmethod # untuk membuat objek Kendaraan dari dict (saat load dari file)
    def dari_dict(d):
        v = Kendaraan(d["vid"], d["jenis"], d["kecepatan"])
        v.waktu_masuk  = d["waktu_masuk"]
        v.waktu_tunggu = d["waktu_tunggu"]
        v.jalur        = d["jalur"]
        v.sudah_lewat  = d["sudah_lewat"]
        return v