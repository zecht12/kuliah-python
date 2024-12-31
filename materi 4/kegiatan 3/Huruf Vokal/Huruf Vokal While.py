def hitung_huruf_vokal_while():
    kalimat = input("Masukkan kalimat: ")
    vokal = "aeiouAEIOU"
    jumlah_vokal = 0
    i = 0
    while i < len(kalimat):
        if kalimat[i] in vokal:
            jumlah_vokal += 1
        i += 1
    print(f"Jumlah karakter: {len(kalimat)}")
    print(f"Huruf vokalnya: {jumlah_vokal}")

hitung_huruf_vokal_while()
