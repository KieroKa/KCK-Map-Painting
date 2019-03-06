from __future__ import division             # Division in Python 2.7
from PIL import Image
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI

# Zmienne wykorzystane w zadaniu
cos = []
linie = []
rzad = []
pixele = []
liczba = 0
y = 0
maks = 0
mins = 0

linie2 = []
rzad2 = []
pixele2 = []

linie3 = []
rzad3 = []


# Zamiana z hsl na rgb
def hsv2rgb(hz, s, v):
    if s == 0.0:
        return nargb(v, v, v)
    iz = int(hz * 6.)
    fz = (hz * 6.) - iz
    p, q, t = v * (1. - s), v * (1. - s * fz), v * (1. - s * (1. - fz))
    iz %= 6
    if iz == 0:
        return nargb(v, t, p)
    if iz == 1:
        return nargb(q, v, p)
    if iz == 2:
        return nargb(p, v, t)
    if iz == 3:
        return nargb(p, q, v)
    if iz == 4:
        return nargb(t, p, v)
    if iz == 5:
        return nargb(v, p, q)


# Zminana z trybu <0,1> do <0,255> w zapisie rgb
def nargb(r, g, b):
    jeden = int(r*255)
    dwa = int(g*255)
    trzy = int(b*255)
    return jeden, dwa, trzy


# Ustawienie wskaźnika l
def setl(row, column):
    if row == 499 or column == 499:
        return 0.90
    if pixele2[row][column] == pixele2[row][column - 1] or pixele2[row][column] == pixele2[row][column + 1]:
        return 0.85
    if pixele2[row][column] > pixele2[row][column - 1]:
        return 1
    return 0.7


# Sprawdzenie wartości minimalnej i maksymalnej do standaryzacji wysokości
with open('mapa.txt') as f:
    first_line = f.readline()
    for l in f.readlines():
        linie3.append([float(x) for x in l.split()])
        for x in linie3[liczba]:
            rzad3.append(x)
        liczba = liczba + 1
    maks = max(rzad3)
    mins = min(rzad3)

liczba = 0

# Wczytanie wartości do tablicy, żeby móc sprawdzać jego lewego sąsiada
with open('mapa.txt') as f:
    first_line = f.readline()
    for l in f.readlines():
        linie2.append([float(x) for x in l.split()])
        for x in linie2[liczba]:
            rzad2.append(x)
        pixele2.append(rzad2)
        rzad2 = []
        liczba = liczba + 1

liczba = 0

with open('mapa.txt') as f:
    first_line = f.readline()
    rozmiar_mapy = ([int(x) for x in first_line.split()])
    for l in f.readlines():
        linie.append([float(x) for x in l.split()])
        for x in linie[liczba]:
            z = (x-mins)/(maks-mins)  # Standaryzacja wysokości
            h = (120 / 360) - z * (120 / 360)  # Wyznaczenie koloru od zielonego do czerwonego
            rzad.append(hsv2rgb(h, 1, setl(liczba, y)))  # Zmiana z hsl i wyznaczenie wartości l
            y = y + 1
        pixele.append(rzad)
        rzad = []
        y = 0
        liczba = liczba + 1

img = Image.new('RGB', (rozmiar_mapy[0], rozmiar_mapy[1]), "black")  # Tworzenie obrazka (początkowo czarnego)
pixels = img.load()

for i in range(img.size[0]):
    for j in range(img.size[1]):
        pixels[i, j] = pixele[j][i]  # Rysowanie obrazka pixel po pixelu
img.show()
img.save('out.png')
