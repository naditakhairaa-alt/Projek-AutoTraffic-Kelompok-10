# 5. Single Linked List - Log kendaraan yang sudah lewat

import time

class NodeSLL:
    def __init__(self, data):
        self.data = data
        self.next = None

class LogSLL:
    # tambah ke belakang (tail) supaya urutan masuk = urutan tampil.
    def __init__(self):
        self.head   = None
        self.tail   = None
        self.ukuran = 0

    def tambah(self, vehicle, dari_jalur):
        # catat kendaraan yang baru saja melintas
        entri = {
            "vid"       : vehicle.vid,
            "jenis"     : vehicle.jenis,
            "jalur"     : dari_jalur,
            "tunggu"    : round(vehicle.waktu_tunggu, 2),
            "waktu"     : time.strftime("%H:%M:%S"),
        }

        node = NodeSLL(entri)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail      = node
        self.ukuran += 1

    def semua(self):
        hasil, cur = [], self.head
        while cur:
            hasil.append(cur.data)
            cur = cur.next
        return hasil

    def n_terakhir(self, n):
        semua  = self.semua()
        return semua[-n:] if len(semua) >= n else semua