# coding: utf-8
from random import uniform, random
from math import sin
from numpy import array, float64
from collections import Counter

global w, c1, c2, m, dim

w = 0.1 #fator de diversificação
c1 = 0.8 #intensificação fator cognitivo
c2 = 0.3 #intensificação fator social
m = 100 #número de partículas
dim = 3 #número de dimensões
xmin = -10 #limite de posição inferior
xmax = 10 #limite de posição superior

#função objetivo
def func_obj(x):

    soma = 0
    for i in range(dim):
        soma += abs(x[i]*sin(x[i]) + 0.1*x[i]) #Alpine 1 Function

    return soma

def atualizaVelocidade(x, v, pbest, gbest):

    r1 = random()
    r2 = random()
    v_novo = [
        (w*v[j] + c1*r1*(pbest[j] - x[j]) + c2*r2*(gbest[j] - x[j])) for j in range(dim)
    ]

    return array(v_novo)

def atualizaPosicao(x, v):

    x_novo = x + v
    for j in range(dim):
        if x_novo[j] < xmin: x_novo[j] = xmin
        elif x_novo[j] > xmax: x_novo[j] = xmax

    return x_novo

def main(**kwargs):
    global w, c1, c2, m, dim
    globals().update(**kwargs)

    x = [array([uniform(xmin, xmax) for i in range(dim)]) for j in range(m)] #vetor de coordenadas
    v = [array([0 for i in range(dim)]) for j in range(m)] #vetor de velocidade
    pbest = x[:]
    gbest_fit = float("inf")
    gbest = None

    contador = Counter()

    while contador[gbest_fit] <= 10:
        contador[gbest_fit] += 1
        
        for i in range(m):
            if func_obj(x[i]) <= func_obj(pbest[i]):
                pbest[i] = x[i].copy()
                if func_obj(x[i]) < gbest_fit:
                    gbest_fit = func_obj(x[i])
                    gbest = x[i].copy()
            
            v[i] = atualizaVelocidade(x[i], v[i], pbest[i], gbest)
            x[i] = atualizaPosicao(x[i], v[i])

        print(f"Melhor solução: {gbest_fit:30} {gbest}")

    return gbest, gbest_fit

if __name__ == "__main__":
    gbest = array([0 for i in range(dim)], dtype=float64)
    gbest_fit = 0
    for i in range (5):
        print(f"Teste {i+1}") 
        g, gf = main()
        gbest += g
        gbest_fit += gf
    print(f"\nSolução média: {gbest_fit/5:30} {gbest}")
