# 3. Double Linked List - Kendaraan dalam satu jalur
# Dipakai untuk melihat jarak antar kendaraan depan & blkg (head & tail)

class NodeDLL:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoubleLaneDLL:
    def __init__(self):
        self.head   = None   # kendaraan paling depan (akan jalan duluan)
        self.tail   = None   # kendaraan paling belakang (baru masuk)
        self.ukuran = 0

    def enqueue(self, vehicle):
        # tambah ke belakang antrian (tail)
        node = NodeDLL(vehicle)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev      = self.tail
            self.tail.next = node
            self.tail      = node
        self.ukuran += 1

    def dequeue(self):
        # ambil dari depan antrian (head)
        if self.head is None:
            return None
        data      = self.head.data
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.ukuran -= 1
        return data

    def peek_depan(self):
        # lihat kendaraan paling depan tanpa diambil
        return self.head.data if self.head else None

    def cek_jarak(self, vid):
        # lihat tetangga depan/belakang suatu node berdasarkan ID kendaraan
        cur = self.head
        while cur:
            if cur.data.vid == vid:
                depan    = cur.prev.data if cur.prev else None
                belakang = cur.next.data if cur.next else None
                return depan, belakang
            cur = cur.next
        return None, None

    def ke_list(self):
        # konversi isi lane ke list
        hasil, cur = [], self.head
        while cur:
            hasil.append(cur.data)
            cur = cur.next
        return hasil

    def kosong(self):
        return self.head is None