#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

n = 5 # número do grupo! IMPORTANTE MUDAR PARA O CORRETO
l_x = 30 #metros
l_y = 20 #metros
delta_x = 1.13
delta_y = 1
delta_t = 0.5
tempo_despejo = 3 #segundos
tempo_total = 10 * tempo_despejo #segundos
k = 1 #m^2/s
alpha = 1 #m/s
qezao = 100 #kg/ms
a = n/ 1.4 #coordenada x do ponto de derramamento do líquido
b = 60/(n+5) #coordenada y do ponto de derramamento do líquido

qzinho = qezao/(delta_x*delta_y)

nx = int(l_x/delta_x)
ny = int(l_y/delta_y)

def build_matrix(nx, ny):
    empty_matrix = np.zeros((nx,ny))
    return empty_matrix

def solve_matrix(act_matrix, nx, ny):
    nxt_matrix = build_matrix(nx, ny)
    for i in range (2, nx - 2):
        for j in range (2, ny - 2):
            vel_u = alpha
            vel_v = alpha*np.sin((np.pi/5)*i)
            
            nxt_matrix[i][j] = act_matrix[i][j] + delta_t * (qzinho - vel_u*(
                (act_matrix[i+1][j] - act_matrix[i-1][j])/2*delta_x) - vel_v*((act_matrix[i][j+1] - act_matrix[i][j-1])/2*delta_y) +
                k * ((act_matrix[i+1][j] - 2*act_matrix[i][j] + act_matrix[i-1][j])/delta_x**2) +
                k * ((act_matrix[i][j+1] - 2*act_matrix[i][j] + act_matrix[i][j-1])/delta_y**2))
            if nxt_matrix[i][j] < 0:
                nxt_matrix[i][j] = 0

    return nxt_matrix

act_matrix = build_matrix(nx, ny)
for qq in range(1000):
    act_matrix = solve_matrix(act_matrix, nx, ny)

print(act_matrix)

plt.imshow(act_matrix)
plt.colorbar()
plt.show()
