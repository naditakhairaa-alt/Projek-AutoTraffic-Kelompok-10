# File handler - .json & .txt

import json, os, time
from structure.sll import NodeSLL
from structure.oop import Kendaraan

# from main import Kendaraan

FILE_JSON    = "data/autotraffic_data.json"
FILE_LAPORAN = "data/autotraffic_laporan.txt"

def simpan_json(jalur, log_sll, graph):
    # Simpan state persimpangan ke JSON
    data = {
        "jalur": {},
        "log"  : log_sll.semua(),
        "graph": {
            k: [(t, j, kap) for t, j, kap in v]
            for k, v in graph.adj.items()
        },
        "disimpan": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    for nama, lane in jalur.items():
        data["jalur"][nama] = {
            "antrian"              : [v.ke_dict() for v in lane.status_antrian()],
            "total_kendaraan_lewat": lane.total_kendaraan_lewat,
        }
    with open(FILE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def muat_json(jalur, log_sll, graph, ht):
    # Muat state dari JSON jika file ada
    if not os.path.exists(FILE_JSON):
        return False
    with open(FILE_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Muat antrian tiap jalur
    for nama, info in data.get("jalur", {}).items():
        if nama in jalur:
            jalur[nama].total_kendaraan_lewat = info["total_kendaraan_lewat"]
            for vd in info["antrian"]:
                v = Kendaraan.dari_dict(vd)
                jalur[nama].antrian.enqueue(v)
                ht.insert(v)

    # Muat log SLL
    for entri in data.get("log", []):
        node = NodeSLL(entri)
        if log_sll.tail is None:
            log_sll.head = log_sll.tail = node
        else:
            log_sll.tail.next = node
            log_sll.tail      = node
        log_sll.ukuran += 1

    # Muat graph
    for dari, edges in data.get("graph", {}).items():
        for ke, jarak, kap in edges:
            graph.tambah_edge(dari, ke, jarak, kap)

    return True

def simpan_laporan_txt(lanes, log_sll, traffic_light, bst):
    # simpan laporan teks
    with open(FILE_LAPORAN, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("         LAPORAN SIMULASI AUTOTRAFFIC\n")
        f.write(f"         Dibuat: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        # Status tiap jalur
        f.write("─── STATUS JALUR ───\n")
        for nama, lane in lanes.items():
            f.write(f"  {nama}: {lane.antrian.ukuran} kendaraan menunggu | "
                    f"Total lewat: {lane.total_kendaraan_lewat}\n")
            f.write(f"  Durasi hijau optimal: {lane.durasi_hijau_optimal():.1f} detik\n")
            for v in lane.status_antrian():
                f.write(f"    → {v}\n")
            f.write("\n")

        # Log kendaraan lewat
        f.write("─── LOG KENDARAAN MELINTAS ───\n")
        log = log_sll.semua()
        if not log:
            f.write("  (Belum ada kendaraan melintas)\n")
        else:
            f.write(f"  {'No':>4}  {'ID':<10} {'Jenis':<10} {'Jalur':<10} "
                    f"{'Tunggu':>8}  {'Waktu'}\n")
            f.write("  " + "─" * 60 + "\n")
            for i, e in enumerate(log, 1):
                f.write(f"  {i:>4}. {e['vid']:<10} {e['jenis']:<10} "
                        f"{e['jalur']:<10} {e['tunggu']:>6.1f}s  {e['waktu']}\n")

        f.write("\n─── RANKING WAKTU TUNGGU (BST) ───\n")
        semua_v = []
        for lane in lanes.values():
            semua_v.extend(lane.status_antrian())
        for v in semua_v:
            v.update_tunggu()
        bst.bangun(semua_v)
        terurut = bst.inorder()
        for i, v in enumerate(terurut, 1):
            f.write(f"  {i:>3}. {v.vid:<10} tunggu={v.waktu_tunggu:.1f}s\n")

        f.write("\n" + "=" * 70 + "\n")