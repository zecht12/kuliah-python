nilai = int(input("Masukan nilai: "))

if nilai >= 90:
    predikat = "A"
elif 80 <= nilai < 90:
    predikat = "B"
elif 60 <= nilai < 80:
    predikat = "C"
elif 40 <= nilai < 60:
    predikat = "D"
else:
    predikat = "E"

print(f"Maka predikatnya: {predikat}")