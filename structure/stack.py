# 4. Stack - Emergency Undo Input Kendaraan

class NodeStack:
    def __init__(self, data):
        self.data = data
        self.next = None

class UndoStack:
    # Stack berbasis Single Linked List dengan menyimpan 
    # (vehicle, nama_jalur) untuk dibatalkan jika salah input.

    def __init__(self):
        self.top  = None
        self.size = 0

    def push(self, vehicle, nama_jalur):
        node      = NodeStack((vehicle, nama_jalur))
        node.next = self.top
        self.top  = node
        self.size += 1

    def pop(self):
        if self.is_empty():
            return None, None
        data     = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data   # (vehicle, nama_jalur)

    def peek(self):
        if self.is_empty():
            return None, None
        return self.top.data

    def is_empty(self):
        return self.top is None
    
    def kosong(self):
        return self.is_empty()