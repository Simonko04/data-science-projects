import random
import numpy as np
import math

import matplotlib.pyplot as plt


matrix = np.empty((20_020,2),dtype=int)#matica sluziaca na prvotne body
pole = np.full((20_020,20_020),np.inf,dtype=np.float32)#pole sluziace ako 2D vzdialenostna matica
clusters = []

def contains_point(x: int, y: int) -> bool:#na zaistenie unikatnosti bodov
    return np.any((matrix[:, 0] == x) & (matrix[:, 1] == y))



def initial_twenty():#vytvori zaciatocnych 20
    for i in range(20):
        x_poistion = random.randint(-5000, 5000)
        y_poistion = random.randint(-5000, 5000)
        while contains_point(x_poistion, y_poistion):#ak existuje uz takyto bod, tak opakuje
            x_poistion = random.randint(-5000, 5000)
            y_poistion = random.randint(-5000, 5000)
        matrix[i,0] = x_poistion
        matrix[i,1] = y_poistion




def next_twenty_thousand():#vytvori dalsich 20_000 po 20tich
    for i in range(20_000):
        number = random.randrange(20+i)
        chosen_node = matrix[number]
        x_range = 100
        y_range = 100
        if chosen_node[0] + 100 > 5000 or chosen_node[0] - 100 < -5000:#ak sa nevopcha na platno, tak zmensi rozsah
            x_range = 5000 - abs(chosen_node[0])
        if chosen_node[1] + 100 > 5000 or chosen_node[1] - 100 < -5000:
            y_range = 5000 - abs(chosen_node[1])
        x_poistion = chosen_node[0] + random.randint(-x_range, x_range)
        y_poistion = chosen_node[1] + random.randint(-y_range, y_range)
        while contains_point(x_poistion, y_poistion):#ak existuje uz takyto bod, tak opakuje
            x_poistion = chosen_node[0] + random.randint(-x_range, x_range)
            y_poistion = chosen_node[1] + random.randint(-y_range, y_range)
        matrix[i+20, 0]  = x_poistion
        matrix[i+20, 1] = y_poistion


def distance_calculator(x1, y1, x2, y2) -> np.float32:
    return np.float32(math.hypot(x1 - x2, y1 - y2))


def two_d_matrix():#vytvara 2d maticu pre vzdialenosti zo vstupu je to O(n2)
    for i in range(len(matrix)):
        for j in range(i, len(matrix)):
            pole[i][j] = (distance_calculator(matrix[i][0],matrix[i][1], matrix[j][0], matrix[j][1]))


def centroid(cluster) -> tuple:#vypocita centroid
    x_sum = 0
    y_sum = 0
    for i in range(1,len(cluster)):#dvojica s indexom 0 je stary centroid, tak ho nepocitam
        x_sum += cluster[i][0]
        y_sum += cluster[i][1]
    x = x_sum / (len(cluster)-1)#-1, aby som nepocital stary centroid
    y = y_sum / (len(cluster)-1)
    return x,y

def add_column(x,y):#prida novy stlpec do matice, pokial sa vytvori novy cluster
    global matrix, pole
    element = np.array([[x,y]])
    matrix = np.concatenate([matrix,element],axis=0)
    row = np.full(( 1,len(matrix)-1),np.inf ,dtype=np.float32)
    column = np.empty((len(matrix),1),dtype=np.float32)
    for i in range(len(matrix)):
        column[i][0] = distance_calculator(x,y,matrix[i][0],matrix[i][1])
    pole = np.concatenate([pole,row],axis=0)
    pole = np.concatenate([pole,column],axis=1)


def cluster_effectivness(cluster):#pocita, i je nejaky bod od stredu vzdialeny viac ako 20
    for i in range(1, len(cluster)):
        if distance_calculator(cluster[0][0],cluster[0][1],cluster[i][0],cluster[i][1]) > 500:
            return False
    return True


def clustering():
    global matrix, pole
    while True:
        np.fill_diagonal(pole, np.inf)
        pos = np.argmin(pole)
        i, j = np.unravel_index(pos, pole.shape)#najde minimum a suradnice minima
        print(len(pole))
        if pole[i, j] > 500:#ak je uz iba vacsie ako 500, tak nema zmysel pokracovat
            print("lamem")
            break
        length = len(matrix) - len(clusters)
        if i < length and j < length:#pokial su to len 2 body(clustre, ktore pozostavaju z jedneho bodu)
            if i > j:
                i,j = j,i
            cluster = [[0,0], matrix[i], matrix[j]]
            x,y  = centroid(cluster)
            cluster[0] = [x,y]
            clusters.append(cluster)
            ii, jj = sorted([i, j])
            matrix = np.delete(matrix, [ii, jj], axis=0)#zmaze oba body z matrixu a pola a prida tam cluster, teda sa zredukuju obe o 1
            pole = np.delete(pole, [ii, jj], axis=0)  # riadky
            pole = np.delete(pole, [ii, jj], axis=1)  # stĺpce
            add_column(x, y)#spoji ich a nasledne prida rad do matice
        elif i < length or j < length:#pokial jeden z clusterov ma viac ako jeden bod a druhy ma len jeden bod
            mensie = j
            vacsie = i
            if mensie > vacsie:
                mensie = i
                vacsie = j
            cluster = clusters[vacsie-length]
            cluster_copy = cluster.copy()
            cluster_copy.append(matrix[mensie])
            x, y = centroid(cluster_copy)
            cluster_copy[0] = [x,y]
            if not cluster_effectivness(cluster_copy):#zisti, ci cluster nie je s bodom prilis velky
                pole[i][j] = np.inf
                pole[j][i] = np.inf
            else:
                cluster.append(matrix[mensie])
                cluster[0] = [x,y]
                matrix = np.delete(matrix, mensie, 0)
                vacsie -= 1
                matrix[vacsie] = cluster[0]
                pole = np.delete(pole, mensie, 1)
                pole = np.delete(pole, mensie, 0)
                cx = float(cluster[0][0])
                cy = float(cluster[0][1])
                m = len(matrix)
                dx = matrix[:m, 0] - cx#tato cast je dopocitanie novych vzdialenosti
                dy = matrix[:m, 1] - cy
                row = np.hypot(dx, dy, dtype=np.float32)
                pole[vacsie, :m] = row
                pole[:m, vacsie] = row
                pole[vacsie, vacsie] = np.inf
        else:#pokial oba clustre maju viac bodov ako jeden
            if i > j:
                i,j = j,i
            cluster_1 = clusters[i - length]
            cluster_2 = clusters[j - length]
            cluster_3 = cluster_1.copy()#kopia aby som nemenil povodny cluster v pripade, ze spojenie dvoch clusterov bude prilis velke
            cluster_4 = cluster_2.copy()
            del cluster_4[0]
            cluster_3.extend(cluster_4[1:])
            x,y = centroid(cluster_3)
            cluster_3[0] = [x,y]
            if not cluster_effectivness(cluster_3):#zisti, ci cluster nie je prilis velky
                pole[i][j] = np.inf
                pole[j][i] = np.inf
            else:
                cluster_1.extend(cluster_4[1:])#doplni cluster na koniec
                cluster_1[0] = [x,y]
                pole = np.delete(pole,j,1)
                pole = np.delete(pole,j,0)
                matrix = np.delete(matrix, j, 0)#zredukuje o 1
                del clusters[j-length]
                m = len(matrix)
                cx, cy = cluster_1[0][0], cluster_1[0][1]  # centroid ako dva skaláre
                dx = matrix[:m, 0].astype(np.float32, copy=False) - cx#tato cast je dopocitanie novych vzdialenosti
                dy = matrix[:m, 1].astype(np.float32, copy=False) - cy
                row = np.hypot(dx, dy).astype(np.float32, copy=False)
                pole[i, :m] = row
                pole[:m, i] = row
                pole[i, i] = np.inf




def change_clusters():#zmeni centroid na farbu, kedze centroid uz nie je potrebny
    COLORS = [#40 volnym okom rozoznatelnych farieb
        "#4169E1", "#DC143C", "#DAA520", "#228B22", "#FF8C00",
        "#9370DB", "#FF1493", "#40E0D0", "#A0522D", "#708090",
        "#008080", "#4B0082", "#FF6347", "#1E90FF", "#32CD32",
        "#DA70D6", "#FA8072", "#F0E68C", "#D2691E", "#483D8B",
        "#E69F00","#56B4E9","#009E73","#F0E442","#0072B2",
        "#D55E00","#CC79A7","#000000","#00FF7F","#00FFFF",
        "#FFD700","#8B0000","#00BFFF","#7CFC00","#FF4500",
        "#8A2BE2","#6A5ACD","#ADFF2F","#FFB300","#17BECF",
    ]
    for i in range(len(clusters)):
        rgb = COLORS[i]
        clusters[i][0] = rgb#prvu suradnicu, ktora povodne obsahovala informaciu o strede vymeni za farbu


def painting():#vytvori platno
    ax = plt.subplot()
    for cluster in clusters:
        color = cluster[0]
        pts = np.asarray(cluster[1:])
        ax.scatter(pts[:,0], pts[:,1], c=color)
    plt.show()


if __name__ == '__main__':
    initial_twenty()
    next_twenty_thousand()
    two_d_matrix()
    clustering()
    print(len(clusters))
    for cluster in clusters:#na zistenie, ci sa vytvoril prilis velky cluster, ak sa nevypise nic, tak takyto cluster nie je
        if not cluster_effectivness(cluster):
            print("not effective")
    change_clusters()
    painting()