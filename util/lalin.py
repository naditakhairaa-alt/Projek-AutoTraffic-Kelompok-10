# Lampu Lalu Lintas

import time
from structure.cll import CircularRotasi

class LampuLalin:
    # Lampu lalu lintas untuk satu persimpangan.
    # Menggunakan CircularRotasi untuk menentukan urutan hijau.

    URUTAN = ["Utara", "Timur", "Selatan", "Barat"]

    def __init__(self):
        self.rotasi      = CircularRotasi(self.URUTAN)
        self.siklus      = 0     # berapa kali sudah berputar penuh
        self.waktu_mulai = None  # waktu saat hijau dimulai

    def jalur_hijau(self):
        # jalur yang sedang hijau
        return self.rotasi.jalur_aktif()

    def ganti_lampu(self):
        # Pindah ke jalur berikutnya
        jalur = self.rotasi.rotasi()
        self.siklus += 1
        self.waktu_mulai = time.time() # reset timer untuk jalur baru
        return jalur

    def urutan_rotasi(self):
        return self.rotasi.semua_urutan()

    def status_bar(self, lanes):
        # Tampilkan status lampu untuk semua jalur
        hijau = self.jalur_hijau()
        for nama in self.URUTAN:
            simbol = " " if nama == hijau else " "
            lane   = lanes.get(nama)
            antri  = lane.total_antrian() if lane else 0
            darurat = lane.antrian_darurat.ukuran() if lane else 0
            tag    = f"  ⚠ {darurat} darurat" if darurat > 0 else ""
            print(f"    {simbol} {nama:<7} | {antri:>2} kendaraan menunggu{tag}")