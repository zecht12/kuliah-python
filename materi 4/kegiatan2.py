def ubah_huruf_vokal(kalimat, huruf_pengganti):
    vokal = "aeiouAEIOU"

    hasil = ""
    for char in kalimat:
        if char in vokal:
            if char.isupper():
                hasil += huruf_pengganti.upper()
            else:
                hasil += huruf_pengganti.lower()
        else:
            hasil += char
    return hasil

def program_ubah_vokal():

    kalimat = input("Masukkan kalimat: ")
    huruf_pengganti = input("Masukkan huruf pengganti untuk vokal: ")
    if len(huruf_pengganti) != 1 or not huruf_pengganti.isalpha():
        print("Huruf pengganti harus berupa satu huruf!")
        return

    hasil = ubah_huruf_vokal(kalimat, huruf_pengganti)

    print(f"Kalimat asli: {kalimat}")
    print(f"Kalimat setelah diubah: {hasil}")

program_ubah_vokal()