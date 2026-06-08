# SORTING — Merge Sort berdasarkan waktu tunggu

def merge_sort_tunggu(daftar, descending=False):
    # Merge Sort rekursif pada list Kendaraan berdasarkan waktu_tunggu
    if len(daftar) <= 1:
        return daftar
    mid   = len(daftar) // 2
    kiri  = merge_sort_tunggu(daftar[:mid],  descending)
    kanan = merge_sort_tunggu(daftar[mid:],  descending)
    return _merge(kiri, kanan, descending)

def _merge(kiri, kanan, descending):
    hasil = []
    i = j = 0
    while i < len(kiri) and j < len(kanan):
        cond = (kiri[i].waktu_tunggu >= kanan[j].waktu_tunggu) if descending \
               else (kiri[i].waktu_tunggu <= kanan[j].waktu_tunggu)
        if cond:
            hasil.append(kiri[i]); i += 1
        else:
            hasil.append(kanan[j]); j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil