# LANE — Kelas Jalur
# Menggabungkan JalurDLL (antrian) dengan info jalur

from structure.dll import DoubleLaneDLL
from structure.queue import QueuePrioritas

class Lane:
    # Satu jalur di persimpangan.
    # nama: "Utara" | "Timur" | "Selatan" | "Barat"
    # antrian: JalurDLL (double linked list)

    DURASI_HIJAU_BASE = 10   # detik per siklus (bisa dinamis)
    KAPASITAS_MAX     = 20

    def __init__(self, nama):
        self.nama             = nama
        self.antrian          = DoubleLaneDLL()        # Double Linked List (FIFO biasa)
        self.antrian_darurat  = QueuePrioritas() # Queue Prioritas
        self.total_kendaraan_lewat = 0

    def durasi_hijau_optimal(self):
        # durasi hijau optimal berdasarkan jumlah kendaraan
        return min(self.DURASI_HIJAU_BASE + self.antrian.ukuran * 1.5, 30)

    def tambah_kendaraan(self, vehicle):
        total = self.antrian.ukuran + self.antrian_darurat.ukuran()
        if total >= self.KAPASITAS_MAX:
            return False, "Jalur penuh!"
        vehicle.jalur = self.nama
        # Ambulans → masuk antrian darurat (Priority Queue)
        # Selain itu → masuk antrian biasa (Double LL / FIFO)
        if vehicle.jenis == "ambulans":
            self.antrian_darurat.enqueue(vehicle)
            return True, f"[DARURAT] {vehicle.vid} masuk antrian prioritas {self.nama}."
        else:
            self.antrian.enqueue(vehicle)
            return True, f"Kendaraan {vehicle.vid} masuk antrian {self.nama}."

    def lepas_kendaraan(self):
        # keluarkan kendaraan dengan prioritas: darurat dulu, baru biasa
        if not self.antrian_darurat.kosong():
            v = self.antrian_darurat.dequeue()
        else:
            v = self.antrian.dequeue()
        if v:
            v.update_tunggu()
            v.sudah_lewat = True
            self.total_kendaraan_lewat += 1
        return v

    def total_antrian(self):
        # jumlah semua kendaraan (darurat + biasa)
        return self.antrian.ukuran + self.antrian_darurat.ukuran()

    def status_antrian(self):
        # gabungan semua kendaraan: darurat duluan, lalu biasa
        return self.antrian_darurat.ke_list() + self.antrian.ke_list()

    def kepadatan(self):
        # persentase kepadatan jalur (total kedua antrian)
        return self.total_antrian() / self.KAPASITAS_MAX * 100

    def __str__(self):
        # fungsi menampilkan status jalur dengan bar visual dan info jumlah kendaraan
        total   = self.total_antrian()
        darurat = self.antrian_darurat.ukuran()
        bar     = "█" * total + "░" * (self.KAPASITAS_MAX - total)
        tag     = f" [{darurat} darurat!]" if darurat > 0 else ""
        return (f"  {self.nama:<7} [{bar}] "
                f"{total:>2}/{self.KAPASITAS_MAX} "
                f"({self.kepadatan():.0f}%){tag}")