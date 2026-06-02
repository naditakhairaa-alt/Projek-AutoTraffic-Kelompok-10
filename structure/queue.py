# 8. Queue - Antrian Darurat Kendaraan (Prioritas)
# Priority Queue mengurutkan berdasarkan tingkat prioritas kendaraan.
# Kendaraan dengan prioritas lebih tinggi selalu keluar duluan, meskipun datang belakangan.

LEVEL_PRIORITAS = {
    "ambulans": 0, # tertinggi, selalu didahulukan
    "bus"     : 1, # angkutan umum
    "truk"    : 2, # kendaraan berat
    "mobil"   : 3, # terendah
    "motor"   : 4, # terendah
}

class QueuePrioritas:
    # Priority Queue berbasis array untuk antrian kendaraan darurat.
    # Kendaraan dengan prioritas lebih tinggi (nilai level lebih kecil)
    # selalu dikeluarkan lebih dulu.
    # Jika prioritas sama, kendaraan yang lebih dulu masuk (FIFO) didahulukan,
    # maka diimplementasikan dengan menyimpan (level, urutan_masuk, vehicle).
    # misalnya kan saat lampu hijau, kendaraan darurat di antrian ini
    # dilepaskan SEBELUM antrian normal Lane.

    def __init__(self):
        self._data   = []   # list of [level, urutan, vehicle]
        self._urutan = 0    # tie-breaker FIFO

    def enqueue(self, vehicle):
        # Masukkan kendaraan, lalu geser ke posisi yang benar
        # menggunakan insertion sort (array tetap terurut ascending level)

        level  = LEVEL_PRIORITAS.get(vehicle.jenis, 99)
        entri  = [level, self._urutan, vehicle]
        self._urutan += 1
        self._data.append(entri)
        # Insertion sort: geser entri baru ke kiri selama lebih kecil
        i = len(self._data) - 1
        while i > 0:
            prev = self._data[i - 1]
            # bandingkan (level, urutan) — tuple comparison
            if (self._data[i][0], self._data[i][1]) < (prev[0], prev[1]):
                self._data[i], self._data[i - 1] = self._data[i - 1], self._data[i]
                i -= 1
            else:
                break

    def dequeue(self):
        # ambil kendaraan dengan prioritas tertinggi
        if self.is_empty():
            return None
        return self._data.pop(0)[2] # ambil objek Kendaraan-nya

    def peek(self):
        # lihat kendaraan dengan prioritas tertinggi tanpa diambil
        if self.is_empty():
            return None
        return self._data[0][2]

    def is_empty(self):
        return len(self._data) == 0

    def ukuran(self):
        return len(self._data)

    def ke_list(self):
        # return list Kendaraan sesuai urutan prioritas
        return [entri[2] for entri in self._data]

    def tampilkan(self):
        # print isi antrian prioritas dari yang tertinggi
        if self.is_empty():
            print("  (Antrian prioritas kosong)")
            return
        print(f"  {'Pos':>4}  {'ID':<10} {'Jenis':<10} {'Level Prior.':>12}")
        print("  " + "─" * 42)
        for i, (lvl, _, v) in enumerate(self._data, 1):
            tag = " ← PERTAMA" if i == 1 else ""
            print(f"  {i:>4}. {v.vid:<10} {v.jenis:<10} {lvl:>12}{tag}")
            
    def kosong(self):
        return self.is_empty()