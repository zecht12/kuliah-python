def hitung_bmi():
    berat = int(input("Masukkan berat badan anda (kg): "))
    tinggi_cm = int(input("Masukkan tinggi badan anda (cm): "))

    tinggi_m = tinggi_cm / 100

    bmi = berat / (tinggi_m ** 2)

    if bmi < 18.5:
        kategori = "kurus"
    elif 18.5 <= bmi < 25:
        kategori = "langsing/sehat"
    else:
        kategori = "gemuk"

    print(f"Nilai BMI anda adalah: {bmi:.2f}")
    print(f"Anda tergolong berbadan {kategori}")

hitung_bmi()