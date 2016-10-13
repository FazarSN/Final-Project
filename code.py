from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from matplotlib.path import Path
from matplotlib.patches import Wedge, PathPatch
import pandas as pd
import random
import os


def li(a):
	return a.tolist()

def ar(a):
	return np.array(a)
		
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
os.chdir('/home/fazar/Documents/Dropbox/tea/Data/')
def data(file):
    gempa = pd.read_csv(file)
    return gempa
    
def setwaktu(datas, pilihan, tahun = 2012, bulan = 12, tanggal = 12):
    global x,y
    tanggal1 = datas['DATE'].tolist()
    pilihwaktu = pilihan #(tahun/bulan/hari)
    pilihtahun = str(tahun)
    pilihbulan = str(bulan)
    pilihhari = str(tanggal)
    if pilihwaktu == "tahun":
        tahun1 = pd.Series([i.split('-')[0] for i in tanggal1])
        gempatertentu = datas[tahun1 == pilihtahun]
    elif pilihwaktu == "bulan":
        bulan1 = pd.Series([i.split('-')[0] + '-' + i.split('-')[1] for i in tanggal1])
        gempatertentu = datas[bulan1 == pilihtahun + '-' + pilihbulan]
    elif pilihwaktu == "hari":
        hari1 = pd.Series([i for i in tanggal1])
        gempatertentu = datas[hari1 == pilihtahun + '-' + pilihbulan + '-' + pilihhari]
    elif pilihwaktu == 'semua':
        gempatertentu == datas
    x = np.array(gempatertentu['LON'])
    y = np.array(gempatertentu['LAT'])
    titik = np.column_stack([x, y])
    titik = np.vstack({tuple(row) for row in titik})
    return titik
    
def input(sudut = 30, jarijari = 1, tengah = (128, 3), batas = 5):
    global satuan, batasquadrat, h, r
    batasquadrat = batas
    r = float(jarijari)
    h = jarijari
    sudut2 = sudut
    tengah1 = tengah
    satuan = 'm'
    var = [r, sudut2, tengah1]
    return var
    
def quadrat(data, var):
    global path, banyak_titik
    titik = data
    path = []
    titik_daerah = []
    banyak_titik = []
    sudut1 = 0
    r = var[0]
    sudut2 = var[1]
    tengah = var[2]
    selisih_sudut = sudut2 - sudut1
    j=0
    l = 1
    batas_daerah = [batasquadrat for i in range(30)]
    bagisudut = int(360/selisih_sudut)
    for i in range(bagisudut):
        titik_sama = 0
        while r <= batas_daerah[i]:
            path.append(Wedge(tengah, r, sudut1, sudut2).get_path())
            titik_daerah.append(titik[path[j].contains_points(titik)])
            banyak_titik.append(len(titik_daerah[j]))
            banyak_titik[j] = banyak_titik[j] - titik_sama
            titik_sama = titik_sama + banyak_titik[j]
            j += 1
            l += 1
            r = np.sqrt(l) * h
        sudut1 += selisih_sudut
        sudut2 += selisih_sudut
        r = var[0]
        l = 1
    path = np.array(path)
    titik_daerah = np.array(titik_daerah)
    data_titik = [[n,0] for n in range(max(banyak_titik) + 1)]
    
    for i in range(len(banyak_titik)):
        a = banyak_titik[i]
        data_titik[a][1] = data_titik[a][1] + 1
        
    return data_titik
    
def intensitas(mq):
    global jumlah_daerah
    data_titik = mq
    total_titik = 0
    jumlah_daerah = 0
    for i in data_titik:
        total_titik += i[0] * i[1]
        jumlah_daerah += i[1]
    intensity = total_titik / jumlah_daerah
    return intensity
    
def tabel(mq, intensitas):
    global hist1, hist2, expro, expected, proporsi
    intensity = intensitas
    data_titik = mq
    hist1 = []
    hist2 = []
    proporsi = []
    batasj = 30
    k = 0
    titikklebih = 0
    expected = []
    expro = []
    print(" n |frek|frek.relatif|Taksiran (poisson)")
    for i in data_titik:
        hist1.append(i[0])
        hist2.append(i[1])
        p = 1
        for j in range(1,i[0]+1):
            p = p * j
        expected.append(((intensity**i[0])*np.exp(-intensity))/p)
        proporsi.append(i[1] / jumlah_daerah)
        if i[0] >= batasj:
            titiklebih += i[1]
            if i[0] == len(data_titik) - 1:
                fazar = 1
            #print("%02d | %03d |   %.3f    | %.4f" %(i[0], i[1], proporsi[k], expected[k]))
        else:
            print("%02d | %03d |   %.3f    | %.4f" %(i[0], i[1], proporsi[k], expected[k]))
        expro.append(expected[k] * jumlah_daerah)
        k += 1
    print("\nlambda : %f" %intensity)
    
def ujichi(mq):
	global cs, chi, p
	data_titik = mq
	frekuensi = []
	a = 0
	cs = []
	for i in data_titik:
		frekuensi.append(i[1])
		cs += ((frekuensi[a]-expro[a]) ** 2) / expro[a]
		a += 1    
	chi, p = scipy.stats.chisquare(frekuensi, f_exp = expro)
	msg = "Statistik Uji: {}\np-value: {}"
	print( msg.format( chi, p ) )

def daerahstudi(a,b,c,d):
	return [a,b,c,d]
	
def peta(d, a = 0):
    ax1 = plt.subplot()
    m = Basemap(projection='cyl',llcrnrlat=d[0],urcrnrlat=d[1], llcrnrlon=d[2],urcrnrlon=d[3],ax = ax1,resolution='l')
    if a == 0:
	    m.drawcoastlines()
	    m.drawmapboundary()
	    m.fillcontinents(color = 'gray')
    for i in range(len(path)):
        patch = PathPatch(path[i], facecolor = 'none', alpha=0.5)
        ax1.add_patch(patch)
    plt.scatter(x,y)
    plt.show()

def hist():    
    plt.bar(hist1, hist2, 0.8, alpha = 0.5, color = 'b')
    index = np.arange(len(hist1))
    plt.xlabel('Banyak titik')
    plt.ylabel('Banyak daerah')
    plt.xticks(index + 0.4, tuple(hist1))
    plt.show()
       
    fig, ax = plt.subplots()
    index = np.arange(len(expected))
    plt.bar(index, proporsi, 0.2,
                     alpha=0.5,
                     color='b',
                     label='proporsi pengamatan')
    plt.bar(index + 0.2, expected, 0.2,
                     alpha=0.5,
                     color='r',
                     label='proporsi harapan')
    plt.xlabel('Banyak titik')
    plt.xticks(index + 0.2, tuple(index))
    plt.legend()
    plt.show()

def jarak(p,q):
    return ((p[0]-q[0])**2 + (p[1]-q[1])**2) ** 0.5
def terdekat(b, a):
    c = jarak(a[0], b)
    p = a[0]
    for i in a:
        if jarak(i,b)<c:
            p = i
    return p
def terjauh(b, a):
    c = jarak(a[0], b)
    p = a[0]
    for i in a:
        if jarak(i,b)>c:
            p = i
    return p
