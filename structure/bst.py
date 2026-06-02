# 7. BST - Sorting antrian berdasarkan waktu tunggu

class NodeBST:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.kiri    = None
        self.kanan   = None

class BSTWaktuTunggu:
    # BST berbasis waktu_tunggu kendaraan
    
    def __init__(self):
        self.root = None

    def insert(self, vehicle):
        self.root = self._insert(self.root, vehicle)

    def _insert(self, node, vehicle):
        # rekursif insert BST
        if node is None:
            return NodeBST(vehicle)
        if vehicle.waktu_tunggu <= node.vehicle.waktu_tunggu:
            node.kiri  = self._insert(node.kiri,  vehicle)
        else:
            node.kanan = self._insert(node.kanan, vehicle)
        return node

    def inorder(self):
        # return list kendaraan diurutkan berdasarkan waktu tungu
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, node, hasil):
        # rekursif traversal inorder
        if node is None:
            return
        self._inorder(node.kiri, hasil)
        hasil.append(node.vehicle)
        self._inorder(node.kanan, hasil)

    def bangun(self, daftar):
        self.root = None
        for v in daftar:
            self.insert(v)