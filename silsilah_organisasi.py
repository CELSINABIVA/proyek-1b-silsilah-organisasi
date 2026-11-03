# -*- coding: utf-8 -*-
"""
PROTOTIPE SISTEM "SILSILAH ORGANISASI" UIN SUSKA RIAU
Proyek 1b - Struktur Data: General Tree + Traversal
(Preorder, Inorder, Postorder) berbasis OOP Python.

Catatan: nama pegawai di bawah ini fiktif, hanya untuk prototipe.
"""
import time


# ======================================================================
# 1. STRUKTUR NODE
# ======================================================================
class Node:
    """Satu simpul = satu pegawai / jabatan dalam organisasi."""

    def __init__(self, id_pegawai, nama, jabatan):
        self.id = id_pegawai      # kode unik pegawai
        self.nama = nama          # nama pegawai
        self.jabatan = jabatan    # jabatan struktural
        self.atasan = None        # pointer ke parent (None jika root)
        self.anak = []            # daftar bawahan langsung (children)

    def __str__(self):
        return f"[{self.id}] {self.nama} - {self.jabatan}"


# ======================================================================
# 2. KELAS TREE
# ======================================================================
class SilsilahOrganisasi:
    """General Tree: setiap node boleh punya banyak anak."""

    def __init__(self):
        self.root = None
        self._index = {}          # kamus id -> Node (pencarian by ID O(1))

    # ---------------- INSERT ----------------
    def insert_node(self, id_atasan, id_baru, nama, jabatan):
        """Menyisipkan pegawai baru di bawah atasan tertentu.
        Untuk membuat root (tree masih kosong), isi id_atasan=None."""
        if id_baru in self._index:
            raise ValueError(f"ID {id_baru} sudah dipakai")

        node_baru = Node(id_baru, nama, jabatan)

        if self.root is None:
            if id_atasan is not None:
                raise ValueError("Tree kosong: id_atasan harus None untuk root")
            self.root = node_baru
        else:
            atasan = self._index.get(id_atasan)
            if atasan is None:
                raise ValueError(f"Atasan dengan ID {id_atasan} tidak ditemukan")
            node_baru.atasan = atasan
            atasan.anak.append(node_baru)

        self._index[id_baru] = node_baru
        return node_baru

    # ---------------- SEARCH ----------------
    def search_node(self, kata_kunci, berdasarkan="semua"):
        """Mencari pegawai berdasarkan nama atau jabatan.
        berdasarkan: "nama", "jabatan", atau "semua".
        Mengembalikan list Node yang cocok (DFS iteratif)."""
        hasil = []
        if self.root is None:
            return hasil

        kunci = kata_kunci.lower()
        tumpukan = [self.root]
        while tumpukan:
            node = tumpukan.pop()
            cocok_nama = kunci in node.nama.lower()
            cocok_jabatan = kunci in node.jabatan.lower()

            if ((berdasarkan == "nama" and cocok_nama) or
                    (berdasarkan == "jabatan" and cocok_jabatan) or
                    (berdasarkan == "semua" and (cocok_nama or cocok_jabatan))):
                hasil.append(node)

            tumpukan.extend(reversed(node.anak))   # anak pertama diproses dulu
        return hasil

    def cari_by_id(self, id_pegawai):
        """Pencarian berdasarkan ID lewat kamus: O(1)."""
        return self._index.get(id_pegawai)

    def jalur_ke_root(self, id_pegawai):
        """Menampilkan rantai atasan dari root sampai pegawai tersebut."""
        node = self._index.get(id_pegawai)
        jalur = []
        while node is not None:
            jalur.append(node)
            node = node.atasan
        return list(reversed(jalur))

    # ---------------- TRAVERSAL ----------------
    def preorder(self):
        """Preorder: Node -> semua anak (kiri ke kanan)."""
        hasil = []

        def kunjungi(node):
            hasil.append(node)
            for a in node.anak:
                kunjungi(a)

        if self.root:
            kunjungi(self.root)
        return hasil

    def inorder(self):
        """Inorder pada General Tree (definisi yang dipakai):
        anak pertama -> Node -> anak-anak sisanya.
        (Pada binary tree: kiri -> node -> kanan.)"""
        hasil = []

        def kunjungi(node):
            if not node.anak:
                hasil.append(node)
                return
            kunjungi(node.anak[0])
            hasil.append(node)
            for a in node.anak[1:]:
                kunjungi(a)

        if self.root:
            kunjungi(self.root)
        return hasil

    def postorder(self):
        """Postorder: semua anak (kiri ke kanan) -> Node."""
        hasil = []

        def kunjungi(node):
            for a in node.anak:
                kunjungi(a)
            hasil.append(node)

        if self.root:
            kunjungi(self.root)
        return hasil

    # ---------------- INFORMASI TREE ----------------
    def jumlah_node(self):
        return len(self._index)

    def jumlah_level(self):
        """Jumlah level (root = level 1)."""
        if self.root is None:
            return 0
        level, saat_ini = 0, [self.root]
        while saat_ini:
            level += 1
            saat_ini = [a for n in saat_ini for a in n.anak]
        return level

    def tampil_pohon(self):
        """Menggambar tree dalam bentuk teks bercabang."""
        if self.root is None:
            print("(tree kosong)")
            return

        def cetak(node, awalan, terakhir, is_root=False):
            label = f"{node.jabatan} ({node.nama})"
            if is_root:
                print(label)
                anak_awalan = ""
            else:
                print(awalan + ("└── " if terakhir else "├── ") + label)
                anak_awalan = awalan + ("    " if terakhir else "│   ")
            for i, a in enumerate(node.anak):
                cetak(a, anak_awalan, i == len(node.anak) - 1)

        cetak(self.root, "", True, is_root=True)


# ======================================================================
# 3. FUNGSI BANTU
# ======================================================================
def tampil_urutan(judul, daftar_node):
    print(f"\n{judul}")
    for i, n in enumerate(daftar_node, 1):
        print(f"  {i:>2}. {n.jabatan}")
    print("  Ringkas: " + " -> ".join(n.jabatan for n in daftar_node))


def bangun_organisasi():
    """Membangun struktur organisasi UIN Suska Riau (prototipe)."""
    t = SilsilahOrganisasi()
    t.insert_node(None,      "U001", "Prof. Dr. Ahmad Rafiq, M.Ag.",   "Rektor")
    t.insert_node("U001",    "U002", "Prof. Dr. Hasan Basri, M.A.",    "Senat Universitas")
    t.insert_node("U001",    "U003", "Dr. Siti Marlina, M.Pd.",        "Wakil Rektor I (Bidang Akademik)")
    t.insert_node("U001",    "U004", "Dr. Budi Santoso, M.Si.",        "Wakil Rektor II (Bidang Administrasi Umum & Keuangan)")
    t.insert_node("U001",    "U005", "Dr. Nur Aini, M.Ag.",            "Wakil Rektor III (Bidang Kemahasiswaan & Kerja Sama)")
    t.insert_node("U001",    "U006", "Dr. Fajar Ramadhan, M.T.",       "Dekan Fakultas Sains dan Teknologi")
    t.insert_node("U006",    "U007", "Dr. Rina Wulandari, M.Kom.",     "Wakil Dekan I (Bidang Akademik & Kelembagaan)")
    t.insert_node("U006",    "U008", "Dr. Yusuf Hidayat, M.T.",        "Wakil Dekan II (Bidang AUPK)")
    t.insert_node("U006",    "U009", "Dr. Dewi Anggraini, M.Si.",      "Wakil Dekan III (Bidang Kemahasiswaan)")
    t.insert_node("U006",    "U010", "Dr. Rizki Pratama, M.Kom.",      "Ketua Program Studi Teknik Informatika")
    t.insert_node("U010",    "U011", "Lestari Putri, M.Kom.",          "Sekretaris Program Studi")
    t.insert_node("U010",    "U012", "Andi Kurniawan, M.T.",           "Kepala Laboratorium Komputer")
    t.insert_node("U012",    "U013", "Rahmat Hakim, S.Kom.",           "Asisten Laboratorium")
    t.insert_node("U012",    "U014", "Dimas Saputra, S.T.",            "Teknisi Laboratorium")
    t.insert_node("U010",    "U015", "Dr. Maya Sari, M.Kom.",          "Koordinator Dosen")
    t.insert_node("U015",    "U016", "Eko Prasetyo, M.Kom.",           "Dosen Pembimbing Akademik")
    t.insert_node("U016",    "U017", "Celsi Nabiva",                   "Mahasiswa Bimbingan")
    t.insert_node("U015",    "U018", "Fitri Handayani, M.Cs.",         "Dosen Pengampu Mata Kuliah")
    return t


def ukur_ms(fungsi, ulang=50):
    """Rata-rata waktu eksekusi dalam mikrodetik."""
    mulai = time.perf_counter()
    for _ in range(ulang):
        fungsi()
    return (time.perf_counter() - mulai) / ulang * 1_000_000


def bangun_seimbang(n, cabang=3):
    """Tree lengkap: setiap node punya `cabang` anak (tinggi ~ log n)."""
    t = SilsilahOrganisasi()
    t.insert_node(None, 0, "Pegawai 0", "Jabatan 0")
    for i in range(1, n):
        t.insert_node((i - 1) // cabang, i, f"Pegawai {i}", f"Jabatan {i}")
    return t


def bangun_condong(n):
    """Tree condong (skewed): setiap node hanya punya 1 anak (seperti linked list)."""
    t = SilsilahOrganisasi()
    t.insert_node(None, 0, "Pegawai 0", "Jabatan 0")
    for i in range(1, n):
        t.insert_node(i - 1, i, f"Pegawai {i}", f"Jabatan {i}")
    return t


# ======================================================================
# 4. PROGRAM UTAMA
# ======================================================================
if __name__ == "__main__":
    org = bangun_organisasi()

    print("=" * 70)
    print("STRUKTUR ORGANISASI UIN SUSKA RIAU (GENERAL TREE)")
    print("=" * 70)
    org.tampil_pohon()
    print(f"\nJumlah node  : {org.jumlah_node()}")
    print(f"Jumlah level : {org.jumlah_level()}")

    # ---- Operasi INSERT ----
    print("\n" + "=" * 70)
    print("OPERASI INSERT")
    print("=" * 70)
    baru = org.insert_node("U018", "U019", "Hendra Wijaya, S.Kom.", "Staf Administrasi Prodi")
    print("Berhasil menyisipkan:", baru)
    print("Atasannya           :", baru.atasan)
    try:
        org.insert_node("X999", "U020", "Tidak Ada", "Uji Gagal")
    except ValueError as e:
        print("Uji atasan tidak ada:", e)

    # ---- Operasi SEARCH ----
    print("\n" + "=" * 70)
    print("OPERASI SEARCH")
    print("=" * 70)
    for kunci, mode in [("Rizki", "nama"), ("Dekan", "jabatan"), ("Dosen", "jabatan"), ("Rektor", "semua")]:
        hasil = org.search_node(kunci, mode)
        print(f'\nCari "{kunci}" (berdasarkan {mode}) -> {len(hasil)} hasil')
        for h in hasil:
            print("   ", h)
    print("\nJalur atasan Mahasiswa Bimbingan (U017):")
    print("   " + " > ".join(n.jabatan for n in org.jalur_ke_root("U017")))

    # ---- TRAVERSAL pada struktur (tanpa node tambahan) ----
    org2 = bangun_organisasi()
    print("\n" + "=" * 70)
    print("TRAVERSAL STRUKTUR ORGANISASI (18 node)")
    print("=" * 70)
    tampil_urutan("PREORDER", org2.preorder())
    tampil_urutan("INORDER", org2.inorder())
    tampil_urutan("POSTORDER", org2.postorder())

    # ---- ANALISIS WAKTU ----
    print("\n" + "=" * 70)
    print("ANALISIS WAKTU: TREE SEIMBANG vs CONDONG (n = 1093 node)")
    print("=" * 70)
    n = 1093
    seimbang, condong = bangun_seimbang(n), bangun_condong(n)
    target = f"Pegawai {n - 1}"

    print(f"Level seimbang : {seimbang.jumlah_level()}")
    print(f"Level condong  : {condong.jumlah_level()}")

    t_cari_s = ukur_ms(lambda: seimbang.search_node(target, "nama"))
    t_cari_c = ukur_ms(lambda: condong.search_node(target, "nama"))
    t_jalur_s = ukur_ms(lambda: seimbang.jalur_ke_root(n - 1), ulang=500)
    t_jalur_c = ukur_ms(lambda: condong.jalur_ke_root(n - 1), ulang=500)
    t_id_s = ukur_ms(lambda: seimbang.cari_by_id(n - 1), ulang=5000)
    t_id_c = ukur_ms(lambda: condong.cari_by_id(n - 1), ulang=5000)

    print(f"\n{'Operasi':<34}{'Seimbang':>12}{'Condong':>12}  (mikrodetik)")
    print(f"{'search_node by nama (DFS)':<34}{t_cari_s:>12.2f}{t_cari_c:>12.2f}")
    print(f"{'jalur_ke_root (naik lewat atasan)':<34}{t_jalur_s:>12.2f}{t_jalur_c:>12.2f}")
    print(f"{'cari_by_id (dictionary)':<34}{t_id_s:>12.2f}{t_id_c:>12.2f}")
