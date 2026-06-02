# 10. Graph - Peta rute antar persimpangan

class GraphPeta:
    def __init__(self):
        self.adj = {}    # { node: [(tujuan, jarak, kapasitas), ...] }

    def tambah_node(self, nama):
        if nama not in self.adj:
            self.adj[nama] = []

    def tambah_edge(self, dari, ke, jarak, kapasitas=100):
        self.tambah_node(dari)
        self.tambah_node(ke)
        # Hindari duplikasi
        for i, (t, j, k) in enumerate(self.adj[dari]):
            if t == ke:
                self.adj[dari][i] = (ke, jarak, kapasitas)
                return
        self.adj[dari].append((ke, jarak, kapasitas))

    def tetangga(self, nama):
        return self.adj.get(nama, [])

    def semua_node(self):
        return list(self.adj.keys())

    def dfs_rute(self, asal, tujuan):
        # DFS rekursif untuk menemukan SATU rute dari asal ke tujuan.
        dikunjungi = set()
        return self._dfs(asal, tujuan, dikunjungi, [asal], 0)

    def _dfs(self, current, tujuan, dikunjungi, rute, jarak_total):
        """Rekursif DFS."""
        if current == tujuan:
            return rute[:], jarak_total
        dikunjungi.add(current)
        for (nbr, jarak, _) in self.adj.get(current, []):
            if nbr not in dikunjungi:
                rute.append(nbr)
                hasil = self._dfs(nbr, tujuan, dikunjungi, rute, jarak_total + jarak)
                if hasil[0] is not None:
                    return hasil
                rute.pop()
        dikunjungi.discard(current)
        return None, -1

    def semua_rute_dfs(self, asal, tujuan):
        # temukan SEMUA rute dari asal ke tujuan (rekursif DFS)
        semua  = []
        self._semua_dfs(asal, tujuan, set(), [asal], 0, semua)
        return semua

    def _semua_dfs(self, cur, tujuan, visited, rute, jarak, semua):
        if cur == tujuan:
            semua.append((rute[:], jarak))
            return
        visited.add(cur)
        for (nbr, j, _) in self.adj.get(cur, []):
            if nbr not in visited:
                rute.append(nbr)
                self._semua_dfs(nbr, tujuan, visited, rute, jarak + j, semua)
                rute.pop()
        visited.discard(cur)

    def tampilkan(self):
        print(f"\n  {'Dari':<15} → {'Ke':<15} {'Jarak':>8} {'Kapasitas':>10}")
        print("  " + "─" * 50)
        for dari, edges in self.adj.items():
            for (ke, jarak, kap) in edges:
                print(f"  {dari:<15} → {ke:<15} {jarak:>6.1f}km {kap:>8} kend")