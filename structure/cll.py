# 6. Circular Linked List — Rotasi Lampu Hijau

class NodeCLL:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularRotasi:
    # untuk rotasi urutan lampu hijau, setiap node = nama jalur (Utara, Timur, Selatan, Barat).
    # next() → majukan ke jalur berikutnya, selalu berputar.

    def __init__(self, urutan):
        self.current = None
        self.ukuran  = 0
        for item in urutan:
            self._append(item)

    def _append(self, data):
        node = NodeCLL(data)
        if self.current is None:
            node.next    = node
            self.current = node
        else:
            node.next          = self.current.next
            self.current.next  = node
            self.current       = node
        self.ukuran += 1

    def jalur_aktif(self):
        # jalur yang sedang hijau
        return self.current.next.data # head (pertama dimasukkan)

    def rotasi(self):
        # putar ke jalur berikutnya
        self.current = self.current.next
        return self.current.data

    def semua_urutan(self):
        # kembalikan urutan lengkap rotasi
        hasil, cur = [], self.current.next
        for _ in range(self.ukuran):
            hasil.append(cur.data)
            cur = cur.next
        return hasil