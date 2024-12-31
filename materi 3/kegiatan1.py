nama = input("Masukkan nama anda: ")
tahun_kelahiran = int(input("Masukkan tahun kelahiran anda: "))

if 1944 <=tahun_kelahiran <= 1964:
    generasi = "Baby Boomer"
elif 1965 <=tahun_kelahiran <= 1979:
    generasi = "Generasi X"
elif 1980 <=tahun_kelahiran <= 1994:
    generasi = "Generasi Y"
elif 1995 <=tahun_kelahiran <= 2015:
    generasi = "Generasi Z"
else:
    generasi = "Tidak Diketahui"

print(f"{nama} berdasarkan tahun lahir anda tergolong {generasi}")