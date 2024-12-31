def hitung_pangkat_manual():
    angka = int(input("Masukkan angka: "))
    pangkat = int(input("Masukkan pangkat: "))
    hasil = 1
    for _ in range(pangkat):
        hasil *= angka
    print(f"Hasilnya: {hasil}")

hitung_pangkat_manual()
