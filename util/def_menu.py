# Fungsi Menu

import random
from structure.dll import DoubleLaneDLL
from structure.oop import Kendaraan
from util.id_gen import buat_vid, _vid_counter
from util.merge_sort import merge_sort_tunggu
from util.searching import linear_search_vid, binary_search_tunggu
from util.user_interface import judul, input_int, baris

def menu_tambah_kendaraan(lanes, ht, undo_stack, tree):
    """Tambah kendaraan ke jalur tertentu."""
    judul("TAMBAH KENDARAAN")
    print("  Jalur: 1=Utara  2=Timur  3=Selatan  4=Barat")
    pilih = input_int("  Pilih jalur: ", 1, 4)
    if pilih is None:
        return
    nama_jalur = ["Utara", "Timur", "Selatan", "Barat"][pilih - 1]

    print(f"\n  Jenis kendaraan: {', '.join(Kendaraan.kendaraan)}")
    jenis = input("  Jenis (Enter=mobil): ").strip().lower() or "mobil"
    if jenis not in Kendaraan.kendaraan:
        print(f"  ✗ Jenis tidak valid. Gunakan: {', '.join(Kendaraan.kendaraan)}")
        return

    kec_default = {"mobil": 60, "motor": 80, "truk": 40, "bus": 50, "ambulans": 100}
    kecepatan = input_int(f"  Kecepatan km/h (Enter={kec_default[jenis]}): ",
                           minimum=1, maksimum=200)
    if kecepatan is None:
        kecepatan = kec_default[jenis]

    vid = buat_vid()
    v   = Kendaraan(vid, jenis, kecepatan)
    lane = lanes[nama_jalur]
    ok, pesan = lane.tambah_kendaraan(v)

    if ok:
        ht.insert(v)
        undo_stack.push(v, nama_jalur)
        tree.tambah_vehicle(v)          # masukkan ke N-ary Tree klasifikasi
        print(f"\n  ✔ {pesan}")
        # Tampilkan info tetangga (Double Linked List)
        depan, belakang = lane.antrian.cek_jarak(vid)
        if depan:
            print(f"     Kendaraan di depannya : {depan.vid} ({depan.jenis})")
        if belakang:
            print(f"     Kendaraan di belakangnya: {belakang.vid} ({belakang.jenis})")
    else:
        print(f"  ✗ {pesan}")
        _vid_counter[0] -= 1   # rollback counter


def menu_tambah_batch(lanes, ht, undo_stack, tree):
    """Tambah kendaraan secara otomatis (random) untuk simulasi cepat."""
    judul("TAMBAH KENDARAAN OTOMATIS (BATCH)")
    jumlah = input_int("  Jumlah kendaraan yang akan ditambah: ", 1, 50)
    if jumlah is None:
        return

    jenis_list = list(Kendaraan.kendaraan)
    nama_jalur = ["Utara", "Timur", "Selatan", "Barat"]
    berhasil = 0

    for _ in range(jumlah):
        jenis = random.choice(jenis_list)
        kec   = random.randint(40, 100)
        jalur = random.choice(nama_jalur)
        vid   = buat_vid()
        v     = Kendaraan(vid, jenis, kec)
        ok, _ = lanes[jalur].tambah_kendaraan(v)
        if ok:
            ht.insert(v)
            undo_stack.push(v, jalur)
            tree.tambah_vehicle(v)
            berhasil += 1
        else:
            _vid_counter[0] -= 1

    print(f"  ✔ {berhasil} kendaraan berhasil ditambahkan.")


def menu_undo(lanes, ht, undo_stack):
    """Emergency undo: hapus kendaraan terakhir yang diinput."""
    judul("EMERGENCY UNDO")
    if undo_stack.kosong():
        print("  ✗ Tidak ada operasi yang bisa dibatalkan.")
        return

    v, nama_jalur = undo_stack.peek()
    print(f"  Kendaraan terakhir: {v} di jalur {nama_jalur}")
    konfirm = input("  Batalkan input ini? (y/n): ").strip().lower()
    if konfirm != "y":
        print("  Dibatalkan.")
        return

    undo_stack.pop()
    lane = lanes[nama_jalur]

    # Hapus dari belakang antrian (kendaraan baru ada di belakang)
    daftar = lane.antrian.ke_list()
    if daftar and daftar[-1].vid == v.vid:
        # Rebuild antrian tanpa elemen terakhir
        lane.antrian = DoubleLaneDLL()
        for kend in daftar[:-1]:
            lane.antrian.enqueue(kend)
        ht.hapus(v.vid)
        print(f"  ✔ Kendaraan {v.vid} berhasil dibatalkan dari jalur {nama_jalur}.")
    else:
        print(f"  ✗ Kendaraan {v.vid} tidak ada di belakang antrian (mungkin sudah bergerak).")


def menu_simulasi_lampu(lanes, traffic_light, log_sll, ht, bst, tree):
    """
    Proses pergantian lampu dan keluarkan kendaraan dari jalur hijau.
    Kendaraan darurat (Priority Queue) dilepas lebih dulu dari biasa.
    """
    judul("SIMULASI PERGANTIAN LAMPU")
    print("  Ganti lampu hijau ke jalur berikutnya dan proses kendaraan.\n")

    jalur_sekarang = traffic_light.jalur_hijau()
    lane_aktif     = lanes[jalur_sekarang]
    durasi         = lane_aktif.durasi_hijau_optimal()
    kapasitas_lewat = max(1, int(durasi / 2))

    darurat_ada = lane_aktif.antrian_darurat.ukuran()
    print(f"  Jalur hijau saat ini   : {jalur_sekarang}")
    print(f"  Durasi hijau optimal   : {durasi:.1f} detik")
    print(f"  Kendaraan akan dilepas : maks {kapasitas_lewat} kendaraan")
    if darurat_ada > 0:
        print(f"  ⚠ Antrian darurat      : {darurat_ada} kendaraan → didahulukan!\n")
    else:
        print()

    dilepas = 0
    for _ in range(kapasitas_lewat):
        if lane_aktif.total_antrian() == 0:
            break
        for v in lane_aktif.status_antrian():
            v.update_tunggu()
        v = lane_aktif.lepas_kendaraan()
        if v:
            log_sll.tambah(v, jalur_sekarang)
            bst.insert(v)
            ht.hapus(v.vid)
            tree.hapus_vehicle(v.vid)   # hapus dari N-ary Tree
            tag = " ⚠ [DARURAT]" if v.jenis == "ambulans" else ""
            print(f"  → {v.vid} ({v.jenis}) melintas dari {jalur_sekarang}. "
                  f"Tunggu: {v.waktu_tunggu:.1f}s{tag}")
            dilepas += 1

    if dilepas == 0:
        print(f"  (Tidak ada kendaraan di jalur {jalur_sekarang})")

    jalur_baru = traffic_light.ganti_lampu()
    print(f"\n  ✔ {dilepas} kendaraan dilepas.")
    print(f"  Lampu berputar → jalur [{jalur_baru}] kini HIJAU.")


def menu_lihat_antrian(lanes):
    """Tampilkan detail antrian satu jalur."""
    judul("DETAIL ANTRIAN JALUR")
    print("  1=Utara  2=Timur  3=Selatan  4=Barat  5=Semua")
    pilih = input_int("  Pilih: ", 1, 5)
    if pilih is None:
        return

    if pilih == 5:
        target = list(lanes.values())
    else:
        nama   = ["Utara", "Timur", "Selatan", "Barat"][pilih - 1]
        target = [lanes[nama]]

    for lane in target:
        print(f"\n  ┌─ Jalur {lane.nama} ─ {lane.total_antrian()} kendaraan ─ "
              f"Durasi hijau optimal: {lane.durasi_hijau_optimal():.1f}s")
        # Antrian darurat dulu
        darurat = lane.antrian_darurat.ke_list()
        if darurat:
            print(f"  │  [ANTRIAN DARURAT — dilepas duluan]")
            for i, v in enumerate(darurat, 1):
                v.update_tunggu()
                print(f"  │  [{i:>2} ⚠] {v}")
        # Antrian biasa
        biasa = lane.antrian.ke_list()
        if biasa:
            print(f"  │  [ANTRIAN BIASA — FIFO]")
            for i, v in enumerate(biasa, 1):
                v.update_tunggu()
                posisi = "DEPAN" if i == 1 else f"  {i}"
                print(f"  │  [{posisi}] {v}")
        if not darurat and not biasa:
            print("  │  (kosong)")
        print(f"  └─ Total lewat: {lane.total_kendaraan_lewat} kendaraan")


def menu_cari_kendaraan(lanes, ht):
    """Pencarian kendaraan dengan linear dan binary search."""
    judul("CARI KENDARAAN")
    print("  1. Cari berdasarkan ID / jenis (linear search)")
    print("  2. Cari berdasarkan ID persis (hash table O(1))")
    print("  3. Cari berdasarkan waktu tunggu (binary search)")
    pilih = input("  Pilih: ").strip()

    semua_v = []
    for lane in lanes.values():
        for v in lane.status_antrian():
            v.update_tunggu()
            semua_v.append(v)

    if pilih == "1":
        kunci = input("  Kata kunci (ID atau jenis): ").strip()
        hasil = linear_search_vid(semua_v, kunci)
        if not hasil:
            print("  Tidak ditemukan.")
        else:
            print(f"\n  Ditemukan {len(hasil)} kendaraan:")
            for v in hasil:
                print(f"  → {v}")

    elif pilih == "2":
        vid = input("  ID Kendaraan (contoh: V-0001): ").strip().upper()
        v   = ht.cari(vid)
        if v:
            v.update_tunggu()
            print(f"\n  ✔ Ditemukan: {v}")
            # Cek tetangga di jalur (double linked list)
            if v.jalur and v.jalur in lanes:
                depan, belakang = lanes[v.jalur].antrian.cek_jarak(vid)
                if depan:
                    print(f"     Kendaraan di depan  : {depan.vid} ({depan.jenis})")
                if belakang:
                    print(f"     Kendaraan di belakang: {belakang.vid} ({belakang.jenis})")
        else:
            print("  ✗ Tidak ditemukan.")

    elif pilih == "3":
        target = input("  Waktu tunggu (detik): ").strip()
        try:
            target = float(target)
        except ValueError:
            print("  ✗ Masukkan angka.")
            return
        terurut = merge_sort_tunggu(semua_v)
        hasil   = binary_search_tunggu(terurut, target)
        if hasil:
            print(f"  ✔ Ditemukan: {hasil}")
        else:
            print(f"  Tidak ada kendaraan dengan waktu tunggu ≈ {target}s")


def menu_sort_tunggu(lanes, bst):
    """Tampilkan ranking waktu tunggu."""
    judul("RANKING WAKTU TUNGGU KENDARAAN")
    semua_v = []
    for lane in lanes.values():
        for v in lane.status_antrian():
            v.update_tunggu()
            semua_v.append(v)

    if not semua_v:
        print("  (Tidak ada kendaraan dalam antrian)")
        return

    print("  1. BST Inorder (ascending — terlama menunggu terakhir)")
    print("  2. Merge Sort Descending (terlama menunggu duluan)")
    pilih = input("  Pilih: ").strip()

    if pilih == "1":
        bst.bangun(semua_v)
        terurut = bst.inorder()
        label   = "BST Inorder (paling sebentar dulu)"
    else:
        terurut = merge_sort_tunggu(semua_v, descending=True)
        label   = "Merge Sort Descending (paling lama tunggu dulu)"

    print(f"\n  Urutan: {label}")
    baris("─", 60)
    print(f"  {'No':>4}  {'ID':<10} {'Jenis':<10} {'Jalur':<10} {'Tunggu':>8}")
    baris("─", 60)
    for i, v in enumerate(terurut, 1):
        print(f"  {i:>4}. {v.vid:<10} {v.jenis:<10} {v.jalur or '?':<10} "
              f"{v.waktu_tunggu:>6.1f}s")
    baris("─", 60)


def menu_priority_queue(lanes):
    """Tampilkan dan kelola antrian prioritas kendaraan darurat."""
    judul("ANTRIAN PRIORITAS DARURAT (Priority Queue)")
    print("  1=Utara  2=Timur  3=Selatan  4=Barat  5=Semua jalur")
    pilih = input_int("  Pilih jalur: ", 1, 5)
    if pilih is None:
        return

    if pilih == 5:
        target = list(lanes.values())
    else:
        nama   = ["Utara", "Timur", "Selatan", "Barat"][pilih - 1]
        target = [lanes[nama]]

    for lane in target:
        print(f"\n  ┌─ Jalur {lane.nama} — Antrian Prioritas")
        pq = lane.antrian_darurat
        if pq.kosong():
            print("  │  (Tidak ada kendaraan darurat)")
        else:
            print(f"  │  {'Pos':>4}  {'ID':<10} {'Jenis':<10} {'Level':>6}")
            print("  │  " + "─" * 36)
            for i, (lvl, _, v) in enumerate(pq._data, 1):
                tag = "  ← DILEPAS PERTAMA" if i == 1 else ""
                print(f"  │  {i:>4}. {v.vid:<10} {v.jenis:<10} {lvl:>6}{tag}")
        print(f"  │")
        print(f"  ├─ Antrian Biasa (FIFO):")
        biasa = lane.antrian.ke_list()
        if not biasa:
            print("  │  (Kosong)")
        else:
            for i, v in enumerate(biasa, 1):
                print(f"  │  {i:>4}. {v.vid:<10} {v.jenis:<10}")
        print(f"  └─ Total: {lane.total_antrian()} kendaraan  "
              f"({lane.antrian_darurat.ukuran()} darurat + {lane.antrian.ukuran} biasa)")


def menu_tree(lanes, tree):
    """Tampilkan N-ary Tree klasifikasi kendaraan."""
    judul("KLASIFIKASI KENDARAAN — N-ARY TREE")

    # Bangun ulang tree dari semua kendaraan aktif
    semua_v = []
    for lane in lanes.values():
        semua_v.extend(lane.status_antrian())
    tree.bangun_ulang(semua_v)

    total = tree.hitung_total()   # rekursif dari root
    print(f"  Total kendaraan aktif di persimpangan: {total}\n")
    print("  Struktur klasifikasi:")
    print("  " + "─" * 55)
    tree.tampilkan()
    print("  " + "─" * 55)

    # Info tambahan: cari node jenis tertentu
    print("\n  Cari detail per jenis (Enter untuk skip):")
    jenis = input("  Jenis kendaraan: ").strip().lower()
    if jenis in Kendaraan.kendaraan:
        node = tree.cari_jenis(jenis)   # rekursif DFS
        if node:
            jumlah = tree.hitung_total(node)
            print(f"\n  Node '{jenis}' ditemukan — {jumlah} kendaraan aktif:")
            for anak in node.anak:
                v = anak.vehicle
                if v:
                    v.update_tunggu()
                    print(f"    • {v.vid:<10} jalur={v.jalur or '?'}  "
                          f"kec={v.kecepatan}km/h  tunggu={v.waktu_tunggu:.1f}s")
            if not node.anak:
                print("    (tidak ada kendaraan jenis ini)")
    elif jenis:
        print(f"  ✗ Jenis '{jenis}' tidak dikenal.")


def menu_rute_graph(graph):
    """Kelola peta rute dan cari jalur antar persimpangan."""
    while True:
        judul("PETA RUTE ANTAR PERSIMPANGAN (GRAPH)")
        print("  1. Tambah persimpangan")
        print("  2. Tambah rute (edge)")
        print("  3. Tampilkan peta")
        print("  4. Cari rute (DFS)")
        print("  5. Tampilkan semua rute")
        print("  0. Kembali")
        pilih = input("  Pilih: ").strip()

        if pilih == "1":
            nama = input("  Nama persimpangan: ").strip()
            if nama:
                graph.tambah_node(nama)
                print(f"  ✔ Persimpangan '{nama}' ditambahkan.")

        elif pilih == "2":
            graph.tampilkan()
            node_ada = graph.semua_node()
            if len(node_ada) < 2:
                print("  ✗ Butuh minimal 2 persimpangan.")
                continue
            print(f"  Persimpangan tersedia: {', '.join(node_ada)}")
            dari  = input("  Dari     : ").strip()
            ke    = input("  Ke       : ").strip()
            try:
                jarak = float(input("  Jarak (km): ").strip())
                kap   = input_int("  Kapasitas max (kendaraan/jam): ", 1, 9999) or 100
                graph.tambah_edge(dari, ke, jarak, kap)
                print(f"  ✔ Rute {dari} → {ke} ({jarak}km) ditambahkan.")
            except ValueError:
                print("  ✗ Masukkan angka untuk jarak.")

        elif pilih == "3":
            if not graph.adj:
                print("  (Peta kosong. Tambahkan persimpangan dulu.)")
            else:
                graph.tampilkan()

        elif pilih == "4":
            if not graph.adj:
                print("  (Peta kosong.)")
                continue
            print(f"  Persimpangan: {', '.join(graph.semua_node())}")
            asal   = input("  Asal   : ").strip()
            tujuan = input("  Tujuan : ").strip()
            rute, jarak = graph.dfs_rute(asal, tujuan)
            if rute:
                print(f"\n  ✔ Rute ditemukan: {' → '.join(rute)}")
                print(f"     Total jarak: {jarak:.1f} km")
            else:
                print(f"  ✗ Tidak ada rute dari '{asal}' ke '{tujuan}'.")

        elif pilih == "5":
            print(f"  Persimpangan: {', '.join(graph.semua_node())}")
            asal   = input("  Asal   : ").strip()
            tujuan = input("  Tujuan : ").strip()
            semua  = graph.semua_rute_dfs(asal, tujuan)
            if not semua:
                print("  ✗ Tidak ada rute.")
            else:
                print(f"\n  Semua rute dari {asal} ke {tujuan}:")
                for i, (r, j) in enumerate(semua, 1):
                    print(f"  {i}. {' → '.join(r)}  ({j:.1f} km)")

        elif pilih == "0":
            break


def menu_log(log_sll):
    """Tampilkan log kendaraan yang sudah melintas."""
    judul("LOG KENDARAAN MELINTAS (Single Linked List)")
    n_terakhir = input_int("  Tampilkan berapa entri terakhir (Enter=semua)? ", 1, 9999)
    log = log_sll.n_terakhir(n_terakhir) if n_terakhir else log_sll.semua()

    if not log:
        print("  (Belum ada kendaraan yang melintas)")
        return

    print(f"\n  {'No':>4}  {'ID':<10} {'Jenis':<10} {'Jalur':<10} "
          f"{'Tunggu':>8}  {'Waktu'}")
    baris("─", 65)
    for i, e in enumerate(log, 1):
        print(f"  {i:>4}. {e['vid']:<10} {e['jenis']:<10} "
              f"{e['jalur']:<10} {e['tunggu']:>6.1f}s  {e['waktu']}")
    baris("─", 65)
    print(f"  Total tercatat: {log_sll.ukuran} kendaraan")


def inisialisasi_graph_default(graph):
    """Buat peta persimpangan default untuk demonstrasi."""
    persimpangan = [
        "Simpang-A", "Simpang-B", "Simpang-C",
        "Simpang-D", "Simpang-E", "Terminal",
    ]
    for p in persimpangan:
        graph.tambah_node(p)
    rute = [
        ("Simpang-A", "Simpang-B", 1.2, 200),
        ("Simpang-A", "Simpang-C", 2.5, 150),
        ("Simpang-B", "Simpang-D", 0.8, 180),
        ("Simpang-C", "Simpang-D", 1.1, 160),
        ("Simpang-D", "Simpang-E", 1.7, 220),
        ("Simpang-E", "Terminal",  0.5, 300),
        ("Simpang-B", "Terminal",  3.0, 120),
        ("Simpang-A", "Terminal",  5.0,  80),
    ]
    for d, k, j, kap in rute:
        graph.tambah_edge(d, k, j, kap)