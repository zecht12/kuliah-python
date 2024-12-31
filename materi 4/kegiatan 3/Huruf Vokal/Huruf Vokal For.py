def hitung_huruf_vokal():
    kalimat = input("Masukkan kalimat: ")
    vokal = "aeiouAEIOU"
    jumlah_vokal = 0
    
    for char in kalimat:
        if char in vokal:
            jumlah_vokal += 1
    
    print(f"Jumlah karakter: {len(kalimat)}")
    print(f"Huruf vokalnya: {jumlah_vokal}")

hitung_huruf_vokal()
