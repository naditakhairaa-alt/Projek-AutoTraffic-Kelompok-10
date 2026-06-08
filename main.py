from structure.sll import LogSLL
from structure.stack import UndoStack
from structure.hash import HashTableKendaraan
from structure.bst import BSTWaktuTunggu
from structure.tree import TreeKlasifikasi
from structure.graph import GraphPeta

from util.lane import Lane
from util.lampu_lalin import LampuLalin
from util.user_interface import judul, baris, tampil_dashboard
from util.file_handler import simpan_json, muat_json, simpan_laporan_txt
from util.def_menu import (menu_tambah_kendaraan, menu_tambah_batch, menu_undo, menu_simulasi_lampu, inisialisasi_graph_default)
from util.def_menu import (menu_lihat_antrian, menu_priority_queue, menu_tree, menu_cari_kendaraan, menu_sort_tunggu, menu_rute_graph, menu_log)
from util.id_gen import sinkron_vid
from util.file_handler import FILE_JSON, FILE_LAPORAN

jalur = {
    "Utara"  : Lane("Utara"),
    "Timur"  : Lane("Timur"),
    "Selatan": Lane("Selatan"),
    "Barat"  : Lane("Barat"),
}
lalin      = LampuLalin()          # Circular LL untuk rotasi lampu
log_sll    = LogSLL()              # Single Linked List log kronologis
undo_stack = UndoStack()           # Stack emergency undo
ht         = HashTableKendaraan()  # Hash table index kendaraan
bst        = BSTWaktuTunggu()      # BST sorting waktu tunggu
tree       = TreeKlasifikasi()     # Tree klasifikasi kendaraan
graph      = GraphPeta()           # Graph peta rute

# Inisialisasi graph default
inisialisasi_graph_default(graph)

# Muat data dari file jika ada
if muat_json(jalur, log_sll, graph, ht):
    sinkron_vid(ht)
    # Bangun ulang tree dari data yang dimuat
    for lane in jalur.values():
        for v in lane.status_antrian():
            tree.tambah_vehicle(v)
    print("Memuat data...\n")

# ── Loop utama ────────────────────────────────────────────────────────
while True:
    print()
    tampil_dashboard(jalur, lalin)
    print()
    judul("MENU UTAMA — AUTOTRAFFIC", "─", 70)
    print("\n1. Tambah Kendaraan (Manual)")
    print("2. Tambah Kendaraan Otomatis (Batch / Random)")
    print("3. Emergency Undo (Batalkan Input Terakhir)")
    print("4. Simulasi Pergantian Lampu Hijau")
    print("5. Lihat Detail Antrian Jalur")
    print("6. Antrian Prioritas Darurat (Priority Queue)")
    print("7. Klasifikasi Kendaraan (N-ary Tree)")
    print("8. Cari Kendaraan")
    print("9. Ranking Waktu Tunggu")
    print("10. Peta Rute (Graph)")
    print("11. Log Kendaraan yang Sudah Melintas")
    print("12. Simpan Laporan TXT")
    print("13. Simpan Data (JSON)")
    print("0. Keluar")
    baris("─", 70)

    pilih = input("Pilih menu: ").strip()
    print()

    if pilih == "1":
        menu_tambah_kendaraan(jalur, ht, undo_stack, tree)
    elif pilih == "2":
        menu_tambah_batch(jalur, ht, undo_stack, tree)
    elif pilih == "3":
        menu_undo(jalur, ht, undo_stack)
    elif pilih == "4":
        menu_simulasi_lampu(jalur, lalin, log_sll, ht, bst, tree)
    elif pilih == "5":
        menu_lihat_antrian(jalur)
    elif pilih == "6":
        menu_priority_queue(jalur)
    elif pilih == "7":
        menu_tree(jalur, tree)
    elif pilih == "8":
        menu_cari_kendaraan(jalur, ht)
    elif pilih == "9":
        menu_sort_tunggu(jalur, bst)
    elif pilih == "10":
        menu_rute_graph(graph)
    elif pilih == "11":
        menu_log(log_sll)
    elif pilih == "12":
        simpan_laporan_txt(jalur, log_sll, lalin, bst)
        print(f"Laporan disimpan ke '{FILE_LAPORAN}'")
    elif pilih == "13":
        simpan_json(jalur, log_sll, graph)
        print(f"Data disimpan ke '{FILE_JSON}'")
    elif pilih == "0":
        simpan_json(jalur, log_sll, graph)
        print("Data tersimpan (JSON). Sampai jumpa!\n")
        break
    else:
        print("Masukkan angka!")