# 2. Hash Table - Index kendaraan

def _hash_vid(vid, ukuran):
    # menggunankan hash rolling polinomial sederhana untuk string ID kendaraan.
    h, p, M = 0, 31, 10**9 + 7
    for c in vid:
        h = (h * p + ord(c)) % M
    return h % ukuran

class HashTableKendaraan:
    # Hash table untuk lookup kendaraan berdasarkan ID
    # jika terjadi collision dapat ditangani dengan chaining di list
    
    def __init__(self, ukuran=128):
        self.ukuran  = ukuran
        self.bucket  = [[] for _ in range(ukuran)]
        self.jumlah  = 0

    def _idx(self, vid):
        return _hash_vid(vid, self.ukuran)

    def insert(self, vehicle):
        idx = self._idx(vehicle.vid)
        for i, v in enumerate(self.bucket[idx]):
            if v.vid == vehicle.vid:
                self.bucket[idx][i] = vehicle   # update
                return
        self.bucket[idx].append(vehicle)
        self.jumlah += 1

    def cari(self, vid):
        idx = self._idx(vid)
        for v in self.bucket[idx]:
            if v.vid == vid:
                return v
        return None

    def hapus(self, vid):
        idx = self._idx(vid)
        for i, v in enumerate(self.bucket[idx]):
            if v.vid == vid:
                self.bucket[idx].pop(i)
                self.jumlah -= 1
                return True
        return False

    def semua(self):
        hasil = []
        for b in self.bucket:
            hasil.extend(b)
        return hasil