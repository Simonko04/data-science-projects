import math
import random
import tkinter as tk

canvas = tk.Canvas(width=800, height=400, bg="white")
canvas.pack()

suradnice_1 = [[60,200],[180,200],[100,180],[140,180],[20,160],[80,160],[200,160],[140,140],[40,120],
             [120,120],[180,100],[60,80],[100,80],[180,60],[20,40],[100,40],[200,40],[20,20],[60,20],[160,20]]

suradnice_2 = [[60,200],[180,200],[100,180],[140,180],[20,160],[80,160],[200,160],[140,140],[40,120],
             [120,120],[180,100],[60,80],[100,80],[180,60],[20,40],[100,40],[200,40],[20,20],[60,20],[160,20],[190,50],
               [110,20],[90,80],[160,90],[10,190],[50,50]]

poradie1_pov = 'ABCDEFGHIJKLMNOPQRST'

poradie2_pov = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def fitness_calc(nove):#funkcia pre najdenie dlzky cesty
    suma = 0
    if (len(nove)== 20):
        suradnice = suradnice_1
    else:
        suradnice = suradnice_2
    for i in range(len(nove)):
        id_x = ord(nove[i]) - ord('A')
        if i < len(nove)-1:
            id_y = ord(nove[i + 1]) - ord('A')
        else :
            id_y = ord(nove[0]) - ord('A')
        suma += math.sqrt((suradnice[id_x][0] - suradnice[id_y][0])**2 + (suradnice[id_x][1] - suradnice[id_y][1])**2)

    return suma


def initial_shuffle(poradie_pov):#vytvori prvotnu permutaciu
    nove = ''.join(random.sample(poradie_pov, len(poradie_pov)))
    return nove


def mutation(parent):#vymiena dva uzly v permutacii
    a = random.randint(0, len(parent) - 1)
    b = random.randint(0, len(parent) - 1)
    while (a == b):
        b = random.randint(0, len(parent) - 1)
    parent = list(parent)
    parent[a], parent[b] = parent[b], parent[a]
    parent = ''.join(parent)
    return parent


def annealing(parent):#zihacia funkcia
    T = len(parent)*2#povodna teplota
    a = 0.999
    while(T >= 0.01):
        offspring = mutation(parent)
        parent_fitness = fitness_calc(parent)
        offspring_fitness = fitness_calc(offspring)
        delta = parent_fitness - offspring_fitness#rozdiel dlzok ciest
        if (delta > 0 or random.random() < math.exp(delta/T)):
            parent = offspring
        T = T*a
    return parent

def drawing(parent, color="blue"):#pomocna funkcia na nakreslenie cesty
    if len(parent) == 20:
        points = suradnice_1
    else:
        points = suradnice_2

    canvas_width = int(canvas["width"])
    canvas_height = int(canvas["height"])
    margin = 20

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    def scale(coord, min_val, max_val, canvas_size):
        return margin + (coord - min_val) / (max_val - min_val) * (canvas_size - 2 * margin)

    for i in range(len(parent)):
        id_x = ord(parent[i]) - ord('A')
        if i < len(parent) - 1:
            id_y = ord(parent[i + 1]) - ord('A')
        else:
            id_y = ord(parent[0]) - ord('A')

        x1 = scale(points[id_x][0], min_x, max_x, canvas_width)
        y1 = scale(points[id_x][1], min_y, max_y, canvas_height)
        x2 = scale(points[id_y][0], min_x, max_x, canvas_width)
        y2 = scale(points[id_y][1], min_y, max_y, canvas_height)

        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    for letter in parent:
        idx = ord(letter) - ord('A')
        x = scale(points[idx][0], min_x, max_x, canvas_width)
        y = scale(points[idx][1], min_y, max_y, canvas_height)
        r = 5
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="red")
        canvas.create_text(x, y - 10, text=letter, fill="black")



def main():
    parent_1 = initial_shuffle(poradie1_pov)
    parent_2 = initial_shuffle(poradie2_pov)
    vysledok_1 = annealing(parent_1)
    vysledok_2 = annealing(parent_2)
    print(1/fitness_calc(vysledok_1))
    print(1/fitness_calc(vysledok_2))
    #drawing(vysledok_1, color="blue")
    drawing(vysledok_2, color="green")
    tk.mainloop()
main()