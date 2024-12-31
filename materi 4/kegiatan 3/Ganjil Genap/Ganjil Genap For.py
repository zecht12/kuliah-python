def periksa_ganjil_genap():
    angka = input("Masukkan angka: ")
    for digit in angka:
        if int(digit) % 2 == 0:
            print(f"Angka {digit} adalah genap.")
        else:
            print(f"Angka {digit} adalah ganjil.")

periksa_ganjil_genap()
