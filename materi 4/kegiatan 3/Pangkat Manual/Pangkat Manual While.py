def hitung_pangkat_manual_while():
    angka = int(input("Masukkan angka: "))
    pangkat = int(input("Masukkan pangkat: "))
    hasil = 1
    i = 0
    while i < pangkat:
        hasil *= angka
        i += 1
    print(f"Hasilnya: {hasil}")

hitung_pangkat_manual_while()
