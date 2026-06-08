# UI di menu nanti

def baris(k="═", n=70):
    print(k * n)

def judul(teks, k="═", n=70):
    baris(k, n)
    spasi = (n - len(teks) - 2) // 2
    print(f"{'':>{spasi}} {teks}")
    baris(k, n)


def input_int(prompt, minimum=None, maksimum=None):
    # input integer, opsi q = batal
    while True:
        raw = input(prompt).strip()
        if raw.lower() in ("q", "batal"):
            return None
        try:
            v = int(raw)
            if minimum is not None and v < minimum:
                print(f" Pilihan minimal {minimum}!")
                continue
            if maksimum is not None and v > maksimum:
                print(f" Pilihan maksimal {maksimum}!")
                continue
            return v
        except ValueError:
            print("Masukkan angka.")

def tampil_dashboard(lanes, traffic_light):
    # UI dasbor persimpangan: status lampu, antrian, kepadatan
    judul("DASHBOARD PERSIMPANGAN", "═", 70)
    print(f" Siklus lampu ke-{traffic_light.siklus} | "
          f"Jalur hijau: [{traffic_light.jalur_hijau()}]")
    print(f" Urutan rotasi: {' → '.join(traffic_light.urutan_rotasi())}\n")
    print(" STATUS LAMPU & ANTRIAN:")
    traffic_light.status_bar(lanes)
    print()
    print("  KEPADATAN JALUR:")
    for lane in lanes.values():
        print(lane)
    total = sum(l.total_antrian() for l in lanes.values())
    print(f"\n Total kendaraan menunggu: {total}")
    baris("─", 70)