import random
import math
import tkinter as tk


suradnice = [[60,200],[180,200],[100,180],[140,180],[20,160],[80,160],[200,160],[140,140],[40,120],
             [120,120],[180,100],[60,80],[100,80],[180,60],[20,40],[100,40],[200,40],[20,20],[60,20],[160,20]]

poradie_pov = 'ABCDEFGHIJKLMNOPQRST'#povodne poradie pre permutaciu

parent_gen = []

offspring_gen = []

def fitness_calc(nove):#funkcia pre najdenie fitness, je pocitana pytagorovov vetou
    suma = 0
    for i in range(len(nove)):
        id_x = ord(nove[i]) - ord('A')
        if i < len(nove)-1:
            id_y = ord(nove[i + 1]) - ord('A')
        else :
            id_y = ord(nove[0]) - ord('A')
        suma += math.sqrt((suradnice[id_x][0] - suradnice[id_y][0])**2 + (suradnice[id_x][1] - suradnice[id_y][1])**2)

    return 1 / suma


def min_finder():#pomocna funkcia pre najdenie najnizsej fitness v parent_gen, aby som ju vedel nahradit
    min_fitness = float('inf')
    min_index = -1
    for i in range(len(parent_gen)):
        if parent_gen[i][1] < min_fitness:
            min_fitness = parent_gen[i][1]
            min_index = i
    return min_index


def initial_shuffle():#funkcia pre vytvorenie 20 zaciatocnych permutacii, vyberie si 20 najlepsich z 1000
    for _ in range(100):
        nove = ''.join(random.sample(poradie_pov, len(poradie_pov)))
        fitness = fitness_calc(nove)

        if all(nove != row[0] for row in parent_gen):#najprv zisti, ci dana permutacia uz nie je v parent_gen
            if len(parent_gen) < len(suradnice):#ak je menej ako 20 prvkov rovno to vlozi
                parent_gen.append([nove, fitness])
            else:
                min_index = min_finder()#najde index permutacie s najhorsou fitness
                if fitness > parent_gen[min_index][1]:#ak fitness je lepsia, tak ho nahradi
                    parent_gen[min_index] = [nove, fitness]


def tournament():#funkcia na vyber prveho rodica
    naj_index = 0;
    kandidati = random.sample(parent_gen, 5)#vyberie nahodnych 5
    for i in range(1,len(kandidati)):#najdi z nich jedinca s najvyssou fitness
        if kandidati[i][1] > kandidati[naj_index][1]:
            naj_index = i
    return kandidati[naj_index][0]

def ruleta():#funkcia na vyber druheho rodica
    suma = sum(row[1] for row in parent_gen) #scita celkovu fitness
    hodnota = random.uniform(0,suma)#vyberie nahodnu hodnotu medzi 0 a celkovou fitness
    suma_2 = 0
    for row in parent_gen:#postupne pricituje fitness a ked sa nachadza nad nahodnou hodnotou, tak je na jedincovi, ktoreho si vybral
        suma_2 += row[1]
        if suma_2 > hodnota:
            return row[0]


def krizenie():
    prvy_parent = tournament()
    druhy_parent = ruleta()
    while (druhy_parent == prvy_parent):#aby sa offspring nerovnal parent
        druhy_parent = ruleta()
    a = random.randint(0,len(poradie_pov)-1)
    b = random.randint(0,len(poradie_pov)-1)
    while (a == b):#aby sa offspring nerovnal parent
        b = random.randint(0,len(poradie_pov)-1)
    if a > b:
        a, b = b, a
    if b - a > 17:#zaistuje, ze sa offspring nebude rovnat parent
        b -= 2
    offspring_b = prvy_parent[a:b]
    offspring_a = ""
    for znak in druhy_parent:
        if znak not in offspring_b:
            offspring_a += znak
    offspring_final = offspring_a[:a] + offspring_b + offspring_a[a:]
    if random.random() < 0.1:#mutacia
        offspring_final = list(offspring_final)
        a = random.randint(0, len(poradie_pov) - 1)
        b = random.randint(0, len(poradie_pov) - 1)
        while (a == b):  # aby sa offspring nerovnal parent
            b = random.randint(0, len(poradie_pov) - 1)
        offspring_final[a],offspring_final[b] = offspring_final[b], offspring_final[a]#vymenia sa dve nahodne pismena
        offspring_final = ''.join(offspring_final)
    return offspring_final

def nove_generacie():#vytvara uplne novu generaciu pre neelitarky pristup
    nove = krizenie()
    fitness = fitness_calc(nove)
    if all(nove != row[0] for row in offspring_gen):
        offspring_gen.append([nove, fitness])
    else:
        nove_generacie()

def normalizuj(data, max_y):
    m = max(data)
    return [400 - (y / m) * max_y for y in data]

# Funkcia na kreslenie grafu
def nakresli_graf(canvas, data, farba):
    if not data:
        return
    step = 800 // (len(data) - 1)
    data_y = normalizuj(data, 400 - 20)
    for i in range(len(data) - 1):
        x1, y1 = i * step, data_y[i]
        x2, y2 = (i + 1) * step, data_y[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill=farba, width=2)

def main():
    global parent_gen, offspring_gen
    initial_shuffle()
    sum_neelite = []
    sum_elite = []
    suma = sum(row[1] for row in parent_gen)
    #print(suma)
    sum_neelite.append(suma)
    for i in range(100):#neelitarsky pristup - vymeni vzdycky celu generaciu
        for j in range(20):
            nove_generacie()
        parent_gen = offspring_gen[:]
        offspring_gen = []
        if i % 10 == 0:
            suma = sum(row[1] for row in parent_gen)
            #print(suma)
            sum_neelite.append(suma)
    print("koniec:",parent_gen)
    parent_gen = []
    offspring_gen = []
    print("-------------------------------------")
    initial_shuffle()
    suma = sum(row[1] for row in parent_gen)
    #print(suma)
    sum_elite.append(suma)
    for i in range(2000):#elitarsky pristup vymeni iba najhorsie permutacie v jednotlivych generaciach
        nove = krizenie()
        fitness = fitness_calc(nove)
        if all(nove != row[0] for row in parent_gen):#najprv zisti, ci dana permutacia uz nie je v parent_gen
            min_index = min_finder()#najde index permutacie s najhorsou fitness
            if fitness > parent_gen[min_index][1]:#ak fitness je lepsia, tak ho nahradi
                parent_gen[min_index] = [nove, fitness]
        if i % 100 == 0:
            suma = sum(row[1] for row in parent_gen)
            #print(suma)
            sum_elite.append(suma)

    print("koniec:", parent_gen)

    root = tk.Tk()#jednoduchy graf
    root.title("GA súčty fitness - elitný vs. neelitný")
    canvas = tk.Canvas(root, width=800, height=400, bg="white")
    canvas.pack()
    nakresli_graf(canvas, sum_neelite, "blue")
    nakresli_graf(canvas, sum_elite, "red")

    canvas.create_text(80, 20, text="Neelitársky", fill="blue", anchor="w")
    canvas.create_text(200, 20, text="Elitársky", fill="red", anchor="w")
    root.mainloop()



main()