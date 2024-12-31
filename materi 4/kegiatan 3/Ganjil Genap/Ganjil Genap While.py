def periksa_ganjil_genap_while():
    angka = input("Masukkan angka: ")
    i = 0
    while i < len(angka):
        digit = int(angka[i])
        if digit % 2 == 0:
            print(f"Angka {digit} adalah genap.")
        else:
            print(f"Angka {digit} adalah ganjil.")
        i += 1

periksa_ganjil_genap_while()
