import os
import csv
import pandas as pd
from datetime import datetime


def file_user():
    if not os.path.exists('user.csv'):
        user = {
            'Username' : ['admin'],
            'Password' : ['Admin123'],
            'Nama' : ['Administrator'],
            'Role' : ['admin']
            }
        user = pd.DataFrame(user)
        user.to_csv('user.csv', index = False)


def file_kategori():
    if not os.path.exists('data_kategori.csv'):
        kategori = {
            'ID Kategori' : ['KTG001', 'KTG002', 'KTG003'],
            'Nama Kategori' : ['ATK', 'Elektronik', 'Perabotan']
            }
        kategori = pd.DataFrame(kategori)
        kategori.to_csv('data_kategori.csv', index = False)


def file_barang():
    if not os.path.exists('data_barang.csv'):
        barang = {
            'Kode' : [],
            'Nama Barang' : [],
            'Kategori' : [],
            'Harga (Rp)' : [],
            'Stok' : []
            }
        barang = pd.DataFrame(barang)
        barang.to_csv('data_barang.csv', index = False)


def file_transaksi():
    if not os.path.exists('data_transaksi.csv'):
        transaksi = {
            'ID Transaksi' : [],
            'Tanggal' : [],
            'Staff' : [],
            'Kode' : [],
            'Nama Barang' : [],
            'Jenis' : [],
            'Jumlah' : [],
            'Stok Akhir' : [],
            'Nilai' : []
            }
        transaksi = pd.DataFrame(transaksi)
        transaksi.to_csv('data_transaksi.csv', index = False)


def header():
    tampilan = """
==================================================
|                  SELAMAT DATANG                |
|                    DI STOKIFY                  |
|        Sistem Manajemen Inventaris Gudang      |
==================================================
|   Silakan pilih menu:                          |
|                                                |
|   [1] Login Sistem                             |
|   [2] Registrasi Staff                         |
|   [3] Keluar Program                           |
|                                                |
=================================================="""
    print(tampilan)


def garis():
    print(50 * '=')


def baris(teks = ''):
    print('|' + (' ' + teks).ljust(48) + '|')


def rupiah(angka):
    return 'Rp' + f'{int(angka):,}'.replace(',', '.')


def judul(teks):
    os.system('cls')
    print(50 * '=')
    print('|' + teks.center(48) + '|')
    print(50 * '=')


def gagal(pesan):
    os.system('cls')
    print(' GAGAL '.center(50, '='))
    print(pesan)
    input('Enter Untuk Lanjut')


def berhasil(pesan):
    os.system('cls')
    print(' BERHASIL '.center(50, '='))
    print(pesan)
    input('Enter Untuk Lanjut')


def validasi_tanggal(tanggal):
    try:
        datetime.strptime(tanggal, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def cek_password(password):
    ada_besar = False
    ada_angka = False
    for karakter in password:
        if karakter.isupper():
            ada_besar = True
        if karakter.isdigit():
            ada_angka = True

    kurang = []
    if len(password) < 6:
        kurang.append('minimal 6 karakter')
    if not ada_besar:
        kurang.append('huruf BESAR')
    if not ada_angka:
        kurang.append('angka')
    return kurang


def input_password():
    print('Password minimal 6 karakter, ada huruf besar')
    print('dan angka.')
    while True:
        password = input('Password       : ')
        kurang = cek_password(password)
        if len(kurang) == 0:
            return password
        print('Password belum valid, harus ada: ' + ', '.join(kurang))


def pilih_nomor(teks, jumlah):
    print('\n(Masukkan 0 untuk batal)')
    try:
        nomor = int(input(teks))
    except ValueError:
        gagal('Nomornya harus angka yaaa :D')
        return -1

    if nomor == 0:
        return -1

    if nomor < 0 or nomor > jumlah:
        gagal(f'Nomor "{nomor}" Tidak Ada!')
        return -1
    return nomor - 1


def format_id(awalan, nomor, digit):
    return f'{awalan}{int(nomor):0{digit}d}'


def id_baru(z, kolom, awalan, digit = 3):
    if len(z) == 0:
        return format_id(awalan, 1, digit)
    angka = pd.to_numeric(z[kolom].astype(str).str.extract(r'(\d+)$')[0], errors = 'coerce')
    nomor = angka.max()
    if pd.isna(nomor):
        nomor = 0
    return format_id(awalan, int(nomor) + 1, digit)


def baca_user():
    return pd.read_csv('user.csv', dtype = str)


def baca_kategori():
    return pd.read_csv('data_kategori.csv', dtype = str)


def baca_barang():
    z = pd.read_csv('data_barang.csv', dtype = {'Kode' : str, 'Nama Barang' : str, 'Kategori' : str})
    z['Harga (Rp)'] = z['Harga (Rp)'].astype(int)
    z['Stok'] = z['Stok'].astype(int)
    return z


def baca_transaksi():
    t = pd.read_csv('data_transaksi.csv', dtype = {'ID Transaksi' : str, 'Tanggal' : str, 'Staff' : str, 'Kode' : str, 'Nama Barang' : str, 'Jenis' : str})
    t['Jumlah'] = t['Jumlah'].astype(int)
    t['Stok Akhir'] = t['Stok Akhir'].astype(int)
    t['Nilai'] = t['Nilai'].astype(int)
    return t



def migrasi_data():
    k = baca_kategori()
    kategori_baru = ['ATK', 'Elektronik', 'Perabotan']
    kategori_lama = ['Alat Tulis', 'Makanan', 'Minuman', 'Kebersihan']
    ada_kategori_lama = k['Nama Kategori'].isin(kategori_lama).any()

    if ada_kategori_lama:
        k = pd.DataFrame({
            'ID Kategori': [format_id('KTG', i, 3) for i in range(1, len(kategori_baru) + 1)],
            'Nama Kategori': kategori_baru
        })
        k.to_csv('data_kategori.csv', index=False)
    elif not k['ID Kategori'].str.match(r'^KTG\d+$').all():
        k['ID Kategori'] = [format_id('KTG', i, 3) for i in range(1, len(k) + 1)]
        k.to_csv('data_kategori.csv', index=False)

    kategori_tersedia = baca_kategori()['Nama Kategori'].tolist()
    peta_kode = {}
    z = baca_barang()
    if len(z) > 0:
        if not z['Kode'].str.match(r'^BRG\d+$').all():
            kode_baru = []
            for i, kode_lama in enumerate(z['Kode'].tolist(), start=1):
                kode = format_id('BRG', i, 3)
                peta_kode[str(kode_lama)] = kode
                kode_baru.append(kode)
            z['Kode'] = kode_baru
        z['Kategori'] = z['Kategori'].replace({
            'Alat Tulis': 'ATK',
            'alat tulis': 'ATK'
        })
        z.loc[~z['Kategori'].isin(kategori_tersedia), 'Kategori'] = 'ATK'
        z.to_csv('data_barang.csv', index=False)

    t = baca_transaksi()
    if len(t) > 0:
        if len(peta_kode) > 0:
            t['Kode'] = t['Kode'].astype(str).map(peta_kode).fillna(t['Kode'].astype(str))
        if not t['ID Transaksi'].astype(str).str.match(r'^TRX\d+$').all():
            t['ID Transaksi'] = [format_id('TRX', i, 4) for i in range(1, len(t) + 1)]
        t.to_csv('data_transaksi.csv', index=False)


def tabel_barang(z):
    print()
    print(f"{'No':<4}{'Kode':<9}{'Nama Barang':<12}{'Kategori':<11}{'Harga (Rp)':>9}{'Stok':>5}")
    print(50 * '-')
    for i in z.index:
        harga = f"{int(z.loc[i, 'Harga (Rp)']):,}".replace(',', '.')
        stok = int(z.loc[i, 'Stok'])
        print(f"{i + 1:<4}{z.loc[i, 'Kode']:<9}{z.loc[i, 'Nama Barang'][:11]:<12}{z.loc[i, 'Kategori'][:10]:<11}{harga:>9}{stok:>5}")
    print(50 * '-')
    print(f'Total: {len(z)} jenis barang')


def tabel_kategori(k):
    print()
    print(f"{'No':<4}{'ID':<10}{'Nama Kategori':<36}")
    print(50 * '-')
    for i in k.index:
        print(f"{i + 1:<4}{k.loc[i, 'ID Kategori']:<10}{k.loc[i, 'Nama Kategori'][:35]:<36}")
    print(50 * '-')
    print(f'Total: {len(k)} kategori')


def tabel_user(user):
    print()
    print(f"{'No':<4}{'Username':<16}{'Nama':<22}{'Role':<8}")
    print(50 * '-')
    for i in user.index:
        print(f"{i + 1:<4}{user.loc[i, 'Username'][:15]:<16}{user.loc[i, 'Nama'][:21]:<22}{user.loc[i, 'Role']:<8}")
    print(50 * '-')
    print(f'Total: {len(user)} akun')


def tabel_transaksi(z, tampil_staff = True):
    lebar = 80
    print()
    if tampil_staff:
        print(f"{'ID':<8} {'Tanggal':<16} {'Staff':<9} {'Barang':<12} {'Jenis':<6} {'Jml':>5} {'Stok':>5} {'Nilai':>12}")
    else:
        print(f"{'ID':<8} {'Tanggal':<16} {'Barang':<22} {'Jenis':<6} {'Jml':>5} {'Stok':>5} {'Nilai':>12}")
    print(lebar * '-')

    total_masuk = 0
    total_keluar = 0
    for i in z.index:
        jenis = z.loc[i, 'Jenis']
        nilai = int(z.loc[i, 'Nilai'])
        if jenis == 'MASUK':
            tanda = '+'
            total_masuk += nilai
        else:
            tanda = '-'
            total_keluar += nilai
        jumlah = tanda + str(int(z.loc[i, 'Jumlah']))
        sisa = int(z.loc[i, 'Stok Akhir'])
        tanggal = z.loc[i, 'Tanggal'][:16]

        if tampil_staff:
            print(f"{z.loc[i, 'ID Transaksi']:<8} {tanggal:<16} {z.loc[i, 'Staff'][:9]:<9} {z.loc[i, 'Nama Barang'][:12]:<12} {jenis:<6} {jumlah:>5} {sisa:>5} {rupiah(nilai):>12}")
        else:
            print(f"{z.loc[i, 'ID Transaksi']:<8} {tanggal:<16} {z.loc[i, 'Nama Barang'][:22]:<22} {jenis:<6} {jumlah:>5} {sisa:>5} {rupiah(nilai):>12}")

    print(lebar * '-')
    print(f'Total        : {len(z)} transaksi')
    print(f'Nilai Masuk  : {rupiah(total_masuk)}')
    print(f'Nilai Keluar : {rupiah(total_keluar)}')


def lihat_barang():
    z = baca_barang()
    if len(z) == 0:
        print('\nBelum ada data barang.')
    else:
        tabel_barang(z)


def menu_awal():
    file_user()
    file_kategori()
    file_barang()
    file_transaksi()
    migrasi_data()
    while True:
        os.system('cls')
        header()
        pilihan = input('Masukkan pilihan menu (1-3): ')
        if pilihan == '1':
            login()
        elif pilihan == '2':
            tambah_user('staff')
        elif pilihan == '3':
            os.system('cls')
            print(50 * '=')
            print('|' + 'TERIMA KASIH'.center(48) + '|')
            print('|' + 'SAMPAI JUMPA DI STOKIFY'.center(48) + '|')
            print(50 * '=')
            break
        else:
            print('\nMaaf, Mohon inputkan nomor yang benar :D')
            input('Enter untuk lanjut.')


def login():
    judul('FORM LOGIN')
    username = input('Username                         : ').strip()
    password = input('Password                         : ')
    print(50 * '=')

    user = baca_user()
    cocok = user[(user['Username'] == username) & (user['Password'] == password)]
    if len(cocok) == 0:
        gagal('Username atau Password Salah!')
        return

    nama = cocok.iloc[0]['Nama']
    role = cocok.iloc[0]['Role'].lower()
    print(f'[Berhasil masuk sebagai {role.capitalize()}!]')
    input('Enter Untuk Lanjut')

    if role == 'admin':
        menu_admin(username, nama)
    elif role == 'staff':
        menu_staff(username, nama)
    else:
        gagal('Role akun tidak dikenali!')


def tambah_user(role):
    judul('REGISTRASI ' + role.upper())
    user = baca_user()

    username = input('Username       : ').strip()
    if len(username) < 4:
        gagal('Username minimal 4 karakter!')
        return

    if username.lower() in user['Username'].str.lower().tolist():
        gagal(f'Username "{username}" sudah digunakan!')
        return

    nama = input('Nama Lengkap   : ').strip().title()
    if nama == '':
        gagal('Nama tidak boleh kosong!')
        return

    password = input_password()

    cek = input('\nApakah data sudah sesuai (y/t): ').lower()
    if cek == 'y':
        user.loc[len(user)] = [username, password, nama, role]
        user.to_csv('user.csv', index = False)
        berhasil(f'Akun {role} "{username}" Berhasil Dibuat!')
    else:
        print('\nRegistrasi dibatalkan.')
        input('Enter Untuk Lanjut')


def lihat_user():
    judul('DAFTAR AKUN')
    user = baca_user()
    tabel_user(user)
    input('\nEnter Untuk Lanjut')


def hapus_user(username):
    judul('HAPUS AKUN')
    user = baca_user()
    tabel_user(user)

    indek = pilih_nomor('Masukkan Nomor Akun Yang Dihapus: ', len(user))
    if indek == -1:
        return

    target = user.loc[indek, 'Username']
    if target == username:
        gagal('Akun yang sedang dipakai tidak bisa dihapus!')
        return

    konfirmasi = input(f'Apakah Anda Yakin Menghapus Akun "{target}" (y/n): ')
    if konfirmasi == 'y':
        user = user.drop(indek)
        user = user.reset_index(drop = True)
        user.to_csv('user.csv', index = False)
        berhasil(f'Akun "{target}" Berhasil Dihapus!')
    elif konfirmasi == 'n':
        print(f'\nAkun "{target}" Tidak Dihapus!')
        input('Enter Untuk Lanjut')
    else:
        gagal('Input Yang Benar Yaaa :D')


def menu_kelola_staff(username):
    while True:
        judul('KELOLA STAFF')
        baris()
        baris('  [1] Lihat Daftar Akun')
        baris('  [2] Tambah Staff')
        baris('  [3] Hapus Akun')
        baris('  [0] Kembali')
        baris()
        garis()

        pilihan = input('Masukkan Pilihan: ')
        if pilihan == '1':
            lihat_user()
        elif pilihan == '2':
            tambah_user('staff')
        elif pilihan == '3':
            hapus_user(username)
        elif pilihan == '0':
            return
        else:
            os.system('cls')
            print('Masukkan Pilihan Yang Benar!')
            input('Enter Untuk Lanjut')


def kelola_akun(username):
    while True:
        judul('KELOLA AKUN SAYA')
        user = baca_user()
        data = user[user['Username'] == username].iloc[0]
        print()
        print(f"Username : {data['Username']}")
        print(f"Nama     : {data['Nama']}")
        print(f"Role     : {data['Role']}")
        print()
        garis()
        baris('  [1] Ubah Username')
        baris('  [2] Ubah Password')
        baris('  [0] Kembali')
        garis()

        pilihan = input('Masukkan Pilihan: ')
        if pilihan == '1':
            username = ubah_username(username)
        elif pilihan == '2':
            ubah_password(username)
        elif pilihan == '0':
            return username
        else:
            os.system('cls')
            print('Masukkan Pilihan Yang Benar!')
            input('Enter Untuk Lanjut')


def ubah_username(username):
    judul('UBAH USERNAME')
    user = baca_user()

    baru = input('Username Baru   : ').strip()
    if len(baru) < 4:
        gagal('Username minimal 4 karakter!')
        return username

    if baru.lower() in user['Username'].str.lower().tolist():
        gagal(f'Username "{baru}" sudah digunakan!')
        return username

    user.loc[user['Username'] == username, 'Username'] = baru
    user.to_csv('user.csv', index = False)

    t = baca_transaksi()
    t.loc[t['Staff'] == username, 'Staff'] = baru
    t.to_csv('data_transaksi.csv', index = False)

    berhasil('Username Berhasil Diubah!')
    return baru


def ubah_password(username):
    judul('UBAH PASSWORD')
    user = baca_user()

    password_lama = input('Masukkan Password Lama: ')
    benar = ((user['Username'] == username) & (user['Password'] == password_lama)).any()
    if not benar:
        gagal('Password Lama Salah!')
        return

    password_baru = input_password()
    konfirmasi = input('Konfirmasi Passwordnya: ')
    if password_baru != konfirmasi:
        gagal('Konfirmasi Password Tidak Sama!')
        return

    user.loc[user['Username'] == username, 'Password'] = password_baru
    user.to_csv('user.csv', index = False)
    berhasil('Password Berhasil Diubah!')


def menu_admin(username, nama):
    while True:
        judul(f'MENU ADMIN - {nama}')
        lihat_barang()
        print()
        garis()
        baris('Pilihlah Pilihan:')
        baris()
        baris('  [1] Kelola Barang')
        baris('  [2] Data Kategori')
        baris('  [3] Kelola Staff')
        baris('  [4] Laporan & Rekap')
        baris('  [5] Kelola Akun Saya')
        baris('  [0] Logout')
        baris()
        garis()

        pilihan = input('Masukkan Pilihan: ')
        if pilihan == '1':
            menu_kelola_barang()
        elif pilihan == '2':
            menu_kategori()
        elif pilihan == '3':
            menu_kelola_staff(username)
        elif pilihan == '4':
            laporan_rekap()
        elif pilihan == '5':
            username = kelola_akun(username)
        elif pilihan == '0':
            return
        else:
            os.system('cls')
            print('Masukkan Pilihan Yang Benar!')
            input('Enter Untuk Lanjut')


def menu_staff(username, nama):
    while True:
        judul(f'MENU STAFF - {nama}')
        lihat_barang()
        print()
        garis()
        baris('Pilihlah Pilihan:')
        baris()
        baris('  [1] Cari Barang')
        baris('  [2] Transaksi Barang')
        baris('  [3] Kelola Akun Saya')
        baris('  [0] Logout')
        baris()
        garis()

        pilihan = input('Masukkan Pilihan: ')
        if pilihan == '1':
            cari_barang()
        elif pilihan == '2':
            menu_transaksi(username)
        elif pilihan == '3':
            username = kelola_akun(username)
        elif pilihan == '0':
            return
        else:
            os.system('cls')
            print('Masukkan Pilihan Yang Benar!')
            input('Enter Untuk Lanjut')


def menu_kelola_barang():
    while True:
        judul('KELOLA BARANG')
        lihat_barang()
        print()
        garis()
        baris('  [1] Tambah Barang')
        baris('  [2] Ubah Data Barang')
        baris('  [3] Hapus Barang')
        baris('  [4] Cari Barang')
        baris('  [0] Kembali')
        garis()

        pilihan = input('Masukkan Pilihan: ')
        if pilihan == '1':
            tambah_barang()
        elif pilihan == '2':
            ubah_barang()
        elif pilihan == '3':
            hapus_barang()
        elif pilihan == '4':
            cari_barang()
        elif pilihan == '0':
            return
        else:
            os.system('cls')
            print('Masukkan Pilihan Yang Benar!')
            input('Enter Untuk Lanjut')


def tambah_barang():
    judul('TAMBAH BARANG BARU')
    z = baca_barang()
    k = baca_kategori()
    if len(k) == 0:
        gagal('Belum ada kategori! Tambah kategori dulu.')
        return

    lihat_barang()
    print()

    kode = id_baru(z, 'Kode', 'BRG', 3)
    nama = input('Nama Barang    : ').strip().title()

    if nama == '':
        gagal('Nama barang tidak boleh kosong!')
        return

    tabel_kategori(k)
    pilih = input('Nomor Kategori : ').strip()
    if not pilih.isdigit() or int(pilih) < 1 or int(pilih) > len(k):
        gagal('Nomor kategori tidak ada!')
        return
    kategori = k.loc[int(pilih) - 1, 'Nama Kategori']

    try:
        harga = int(input('Harga (Rp)     : Rp.'))
        stok = int(input('Stok Awal      : '))
    except ValueError:
        gagal('Harga dan stok harus angka yaaa :D')
        return

    if harga < 0 or stok < 0:
        gagal('Harga dan stok tidak boleh minus!')
        return

    z.loc[len(z)] = [kode, nama, kategori, harga, stok]
    z.to_csv('data_barang.csv', index = False)
    berhasil(f'Barang "{nama}" Berhasil Ditambahkan!\nKode Barang: {kode}')


def ubah_barang():
    judul('UBAH DATA BARANG')
    z = baca_barang()
    if len(z) == 0:
        print('\nBelum ada data barang.')
        input('Enter Untuk Lanjut')
        return

    lihat_barang()
    indek = pilih_nomor('Masukkan Nomor Barang Yang Diubah: ', len(z))
    if indek == -1:
        return

    k = baca_kategori()
    print('\nKosongkan lalu Enter kalau tidak ingin mengubah')
    nama_baru = input(f'Nama Baru [{z.loc[indek, "Nama Barang"]}]: ').strip().title()
    tabel_kategori(k)
    kategori_baru = input(f'Nomor Kategori Baru [{z.loc[indek, "Kategori"]}]: ').strip()
    harga_baru = input(f'Harga Baru [{z.loc[indek, "Harga (Rp)"]}]: Rp.').strip()

    if nama_baru == '' and kategori_baru == '' and harga_baru == '':
        gagal('Tidak ada data yang diubah!')
        return

    if kategori_baru != '':
        if not kategori_baru.isdigit() or int(kategori_baru) < 1 or int(kategori_baru) > len(k):
            gagal('Nomor kategori tidak ada!')
            return
        z.loc[indek, 'Kategori'] = k.loc[int(kategori_baru) - 1, 'Nama Kategori']

    if harga_baru != '':
        try:
            harga_baru = int(harga_baru)
        except ValueError:
            gagal('Harga harus angka ya')
            return
        if harga_baru < 0:
            gagal('Harga tidak boleh minus!')
            return
        z.loc[indek, 'Harga (Rp)'] = harga_baru

    if nama_baru != '':
        z.loc[indek, 'Nama Barang'] = nama_baru

    z.to_csv('data_barang.csv', index = False)
    berhasil(f'Data Barang "{z.loc[indek, "Nama Barang"]}" Berhasil Diubah!')


def hapus_barang():
    judul('HAPUS BARANG')
    z = baca_barang()
    if len(z) == 0:
        print('\nBelum ada data barang.')
        input('Enter Untuk Lanjut')
        return

    lihat_barang()
    indek = pilih_nomor('Masukkan Nomor Barang Yang Dihapus: ', len(z))
    if indek == -1:
        return

    nama = z.loc[indek, 'Nama Barang']
    konfirmasi = input(f'Apakah Anda Yakin Menghapus Barang "{nama}" (y/n): ')
    if konfirmasi == 'y':
        z = z.drop(indek)
        z = z.reset_index(drop = True)
        z.to_csv('data_barang.csv', index = False)
        berhasil(f'Barang "{nama}" Berhasil Dihapus!')
    elif konfirmasi == 'n':
        print(f'\nBarang "{nama}" Tidak Dihapus!')
        input('Enter Untuk Lanjut')
    else:
        gagal('Input Yang Benar Yaaa :D')


def cari_barang():
    judul('PENCARIAN BARANG')
    z = baca_barang()
    kata = input('Masukkan Kata Kunci (no / kode / nama): ').strip()

    if kata == '':
        gagal('Kata kunci tidak boleh kosong!')
        return

    cocok_kode = z['Kode'].str.contains(kata, case = False, regex = False)
    cocok_nama = z['Nama Barang'].str.contains(kata, case = False, regex = False)
    hasil = z[cocok_kode | cocok_nama]

    print(f'\nHasil pencarian "{kata}":')
    if len(hasil) == 0:
        print('\nBarang tidak ditemukan.')
    else:
        tabel_barang(hasil)
    input('\nEnter Untuk Lanjut')


def menu_kategori():
    while True:
        judul('DATA KATEGORI')
        k = baca_kategori()
        if len(k) == 0:
            print('\nBelum ada data kategori.')
        else:
            tabel_kategori(k)
        print()
        garis()
        baris('  [1] Tambah Kategori')
        baris('  [2] Ubah Kategori')
        baris('  [3] Hapus Kategori')
        baris('  [0] Kembali')
        garis()

        pilihan = input('Masukkan Pilihan: ')
        if pilihan == '1':
            tambah_kategori()
        elif pilihan == '2':
            ubah_kategori()
        elif pilihan == '3':
            hapus_kategori()
        elif pilihan == '0':
            return
        else:
            os.system('cls')
            print('Masukkan Pilihan Yang Benar!')
            input('Enter Untuk Lanjut')


def tambah_kategori():
    judul('TAMBAH KATEGORI')
    k = baca_kategori()

    nama = input('Nama Kategori  : ').strip().title()
    if nama == '':
        gagal('Nama kategori tidak boleh kosong!')
        return

    if nama.lower() in k['Nama Kategori'].str.lower().tolist():
        gagal(f'Kategori "{nama}" sudah ada!')
        return

    k.loc[len(k)] = [id_baru(k, 'ID Kategori', 'KTG', 3), nama]
    k.to_csv('data_kategori.csv', index = False)
    berhasil(f'Kategori "{nama}" Berhasil Ditambahkan!')


def ubah_kategori():
    judul('UBAH KATEGORI')
    k = baca_kategori()
    if len(k) == 0:
        print('\nBelum ada data kategori.')
        input('Enter Untuk Lanjut')
        return

    tabel_kategori(k)
    indek = pilih_nomor('Masukkan Nomor Kategori Yang Diubah: ', len(k))
    if indek == -1:
        return

    lama = k.loc[indek, 'Nama Kategori']
    baru = input(f'Nama Baru [{lama}]: ').strip().title()
    if baru == '':
        gagal('Nama kategori tidak boleh kosong!')
        return

    if baru.lower() in k['Nama Kategori'].str.lower().tolist() and baru.lower() != lama.lower():
        gagal(f'Kategori "{baru}" sudah ada!')
        return

    k.loc[indek, 'Nama Kategori'] = baru
    k.to_csv('data_kategori.csv', index = False)

    z = baca_barang()
    z.loc[z['Kategori'] == lama, 'Kategori'] = baru
    z.to_csv('data_barang.csv', index = False)

    berhasil(f'Kategori "{lama}" Berhasil Diubah Menjadi "{baru}"!')


def hapus_kategori():
    judul('HAPUS KATEGORI')
    k = baca_kategori()
    if len(k) == 0:
        print('\nBelum ada data kategori.')
        input('Enter Untuk Lanjut')
        return

    tabel_kategori(k)
    indek = pilih_nomor('Masukkan Nomor Kategori Yang Dihapus: ', len(k))
    if indek == -1:
        return

    nama = k.loc[indek, 'Nama Kategori']
    z = baca_barang()
    if nama in z['Kategori'].tolist():
        gagal(f'Kategori "{nama}" masih dipakai oleh barang!')
        return

    konfirmasi = input(f'Apakah Anda Yakin Menghapus Kategori "{nama}" (y/n): ')
    if konfirmasi == 'y':
        k = k.drop(indek)
        k = k.reset_index(drop = True)
        k.to_csv('data_kategori.csv', index = False)
        berhasil(f'Kategori "{nama}" Berhasil Dihapus!')
    elif konfirmasi == 'n':
        print(f'\nKategori "{nama}" Tidak Dihapus!')
        input('Enter Untuk Lanjut')
    else:
        gagal('Input Yang Benar Yaaa :D')


def catat_barang(username, jenis):
    if jenis == 'MASUK':
        judul('CATAT BARANG MASUK')
    else:
        judul('CATAT BARANG KELUAR')

    z = baca_barang()
    if len(z) == 0:
        print('\nBelum ada data barang di gudang.')
        input('Enter Untuk Lanjut')
        return

    lihat_barang()
    indek = pilih_nomor('Masukkan Nomor Barang: ', len(z))
    if indek == -1:
        return

    kode = z.loc[indek, 'Kode']
    nama = z.loc[indek, 'Nama Barang']
    harga = int(z.loc[indek, 'Harga (Rp)'])
    stok_awal = int(z.loc[indek, 'Stok'])

    try:
        jumlah = int(input(f'Jumlah "{nama}" (stok saat ini {stok_awal}): '))
    except ValueError:
        gagal('Jumlah harus angka yaaa :D')
        return

    if jumlah <= 0:
        gagal('Jumlah harus lebih dari 0!')
        return

    if jenis == 'KELUAR' and jumlah > stok_awal:
        gagal(f'Stok "{nama}" tidak cukup!\nStok yang ada hanya {stok_awal} unit.')
        return

    if jenis == 'MASUK':
        stok_akhir = stok_awal + jumlah
    else:
        stok_akhir = stok_awal - jumlah

    nilai = jumlah * harga
    z.loc[indek, 'Stok'] = stok_akhir
    z.to_csv('data_barang.csv', index = False)

    t = baca_transaksi()
    id_transaksi = id_baru(t, 'ID Transaksi', 'TRX', 4)
    waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('data_transaksi.csv', 'a', newline = '', encoding = 'utf-8') as file:
        tulis = csv.writer(file)
        tulis.writerow([id_transaksi, waktu, username, kode, nama, jenis, jumlah, stok_akhir, nilai])

    os.system('cls')
    print(50 * '=')
    print('|' + 'BUKTI MUTASI STOK'.center(48) + '|')
    print(50 * '=')
    print(f'ID Transaksi  : {id_transaksi}')
    print(f'Tanggal       : {waktu}')
    print(f'Petugas       : {username}')
    print(50 * '-')
    print(f'Kode Barang   : {kode}')
    print(f'Nama Barang   : {nama}')
    print(f'Jenis         : Barang {jenis.capitalize()}')
    print(f'Jumlah        : {jumlah} unit')
    print(f'Stok Sebelum  : {stok_awal} unit')
    print(f'Stok Sesudah  : {stok_akhir} unit')
    print(f'Nilai         : {rupiah(nilai)}')
    print(50 * '=')
    print('|' + 'TRANSAKSI SUDAH TERCATAT DI RIWAYAT'.center(48) + '|')
    print(50 * '=')
    input('\nEnter Untuk Lanjut')


def menu_transaksi(username):
    while True:
        judul('TRANSAKSI BARANG')
        baris()
        baris('  [1] Catat Barang Masuk')
        baris('  [2] Catat Barang Keluar')
        baris('  [3] Riwayat Transaksi Saya')
        baris('  [0] Kembali')
        baris()
        garis()

        pilihan = input('Masukkan Pilihan: ')
        if pilihan == '1':
            catat_barang(username, 'MASUK')
        elif pilihan == '2':
            catat_barang(username, 'KELUAR')
        elif pilihan == '3':
            riwayat_staff(username)
        elif pilihan == '0':
            return
        else:
            os.system('cls')
            print('Masukkan Pilihan Yang Benar!')
            input('Enter Untuk Lanjut')


def riwayat_staff(username):
    judul('RIWAYAT TRANSAKSI SAYA')
    t = baca_transaksi()
    t = t[t['Staff'] == username]
    if len(t) == 0:
        print('\nBelum ada transaksi untuk akun ini.')
    else:
        tabel_transaksi(t, tampil_staff = False)
    input('\nEnter Untuk Lanjut')


def laporan_rekap():
    while True:
        judul('LAPORAN & REKAP')
        baris()
        baris('  [1] Riwayat Transaksi (Terbaru)')
        baris('  [2] Cari Transaksi Berdasarkan Tanggal')
        baris('  [3] Laporan Aset Gudang')
        baris('  [0] Kembali')
        baris()
        garis()

        pilihan = input('Masukkan Pilihan: ')
        if pilihan == '1':
            laporan_urut()
        elif pilihan == '2':
            cari_transaksi()
        elif pilihan == '3':
            laporan_aset()
        elif pilihan == '0':
            return
        else:
            os.system('cls')
            print('Masukkan Pilihan Yang Benar!')
            input('Enter Untuk Lanjut')


def laporan_urut():
    judul('RIWAYAT TRANSAKSI')
    t = baca_transaksi()
    if len(t) == 0:
        print('\nBelum ada transaksi.')
    else:
        urut = t.sort_values(by = 'Tanggal', ascending = False)
        tabel_transaksi(urut)
    input('\nEnter Untuk Lanjut')


def cari_transaksi():
    judul('CARI TRANSAKSI')
    t = baca_transaksi()
    if len(t) == 0:
        print('\nBelum ada transaksi.')
        input('Enter Untuk Lanjut')
        return

    tanggal = input('Masukkan Tanggal (YYYY-MM-DD): ').strip()
    if not validasi_tanggal(tanggal):
        gagal('Format tanggal tidak valid! Gunakan YYYY-MM-DD.')
        return

    hasil = t[t['Tanggal'].str[:10] == tanggal]
    print(f'\nTransaksi pada tanggal {tanggal}:')
    if len(hasil) == 0:
        print('\nTidak ada transaksi pada tanggal tersebut.')
    else:
        tabel_transaksi(hasil)
    input('\nEnter Untuk Lanjut')


def laporan_aset():
    judul('LAPORAN ASET TOKO')
    z = baca_barang()

    total_jenis = len(z)
    total_unit = int(z['Stok'].sum())
    total_nilai = int((z['Stok'] * z['Harga (Rp)']).sum())

    print()
    print(f'Total Jenis Barang       : {total_jenis} jenis')
    print(f'Total Keseluruhan Unit   : {total_unit} unit')
    print(f'Total Nilai Aset Gudang  : {rupiah(total_nilai)}')
    print(50 * '=')
    input('\nEnter Untuk Lanjut')


menu_awal()