def cek_bilangan_prima_for(angka):
    if angka < 2:
        return False
    for i in range(2, int(angka**0.5) + 1):
        if angka % i == 0:
            return False
    return True

def program_prima_for():
    angka_list = input("Masukkan angka (pisahkan dengan koma): ").split(",")
    angka_list = [int(x.strip()) for x in angka_list]
    prima_list = [angka for angka in angka_list if cek_bilangan_prima_for(angka)]
    print(f"Bilangan primanya adalah: {prima_list}")

program_prima_for()