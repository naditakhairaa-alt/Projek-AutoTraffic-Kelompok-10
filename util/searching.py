# SEARCHING — Linear + Binary Search

def linear_search_vid(daftar, kunci):
    # Linear search berdasarkan vid atau jenis kendaraan
    kunci = kunci.lower()
    hasil = []
    for v in daftar:
        if kunci in v.vid.lower() or kunci in v.jenis.lower():
            hasil.append(v)
    return hasil

def binary_search_tunggu(daftar_terurut, target):
    # Binary search rekursif pada list terurut berdasarkan waktu_tunggu.
    return _bsearch(daftar_terurut, target, 0, len(daftar_terurut) - 1)

def _bsearch(arr, target, lo, hi):
    if lo > hi:
        return None
    mid = (lo + hi) // 2
    if abs(arr[mid].waktu_tunggu - target) < 0.5:   # toleransi 0.5 detik
        return arr[mid]
    elif arr[mid].waktu_tunggu < target:
        return _bsearch(arr, target, mid + 1, hi)
    else:
        return _bsearch(arr, target, lo, mid - 1)
