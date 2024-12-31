# Nama = Gilang Prima Ertansyah
# NIM = 220103092
# Kelas = TI22C1

# Fungsi Sambutan
def sambutan():
    nama = input("Masukan nama anda: ")
    return print("Selamat datang, ", nama, "!")

# Fungsi Penjumlahan Sederhana
def penjumlahan():
    angka1 = int(input("Masukan angka pertama: "))
    angka2 = int(input("Masukan angka yang ingin di jumlahkan: "))
    
    hasil = angka1 + angka2
    return print("Hasil penjumlahannya adalah ", hasil)

# Memanggil Fungsi
sambutan()
penjumlahan()