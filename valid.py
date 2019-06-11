#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

n = 10 
l_x = 30 #metros
l_y = 30 #metros



delta_x = 1
delta_y = 1
delta_t = 0.05

tempo_despejo = 2 #segundos
tempo_total = 5 #segundos
k = 1 #m^2/s
alpha = 1 #m/s
qezao = 80 #kg/ms
a = 15 #coordenada x do ponto de derramamento do líquido
b = 15 #coordenada y do ponto de derramamento do líquido

qzinho = qezao/(delta_x*delta_y)

act_x = int(l_x/delta_x)
act_y = int(l_y/delta_y)

def build_matrix(nx, ny):
    empty_matrix = np.zeros((ny, nx))
    for j in range (nx):
        for i in range (ny):
            if (i==0 or j==0 or i==(ny-1) or j==(nx-1)):
                empty_matrix[i][j] = 0
            else:
                empty_matrix[i][j] = -1
    return empty_matrix

def solve_matrix(act_matrix, nx, ny, instant):
    nxt_matrix = build_matrix(nx, ny)
    for i in range (ny):
        for j in range (nx):
            if (nxt_matrix[i][j] == -1):
                vel_u = 0
                vel_v = 1
                if(instant <= int(tempo_despejo/delta_t) and (i == int(a)) and (j == int(b))):

                    nxt_matrix[i][j] = act_matrix[i][j] + delta_t * (qzinho - vel_u*(
                    (act_matrix[i+1][j] - act_matrix[i-1][j])/2*delta_x) - vel_v*((act_matrix[i][j+1] - act_matrix[i][j-1])/2*delta_y) +
                    k * ((act_matrix[i+1][j] - 2*act_matrix[i][j] + act_matrix[i-1][j])/(delta_x**2)) +
                    k * ((act_matrix[i][j+1] - 2*act_matrix[i][j] + act_matrix[i][j-1])/(delta_y**2)))

                else:
                    nxt_matrix[i][j] = act_matrix[i][j] + delta_t * (-vel_u*(
                    (act_matrix[i+1][j] - act_matrix[i-1][j])/2*delta_x) - vel_v*((act_matrix[i][j+1] - act_matrix[i][j-1])/2*delta_y) +
                    k * ((act_matrix[i+1][j] - 2*act_matrix[i][j] + act_matrix[i-1][j])/(delta_x**2)) +
                    k * ((act_matrix[i][j+1] - 2*act_matrix[i][j] + act_matrix[i][j-1])/(delta_y**2)))

                if nxt_matrix[i][j] < 0:
                    nxt_matrix[i][j] = 0
                

        for i in range(ny):
            for j in range(nx):
                if((i==0 and j == 0) or (i==0 and j == (ny-1))):
                    nxt_matrix[i][j] = nxt_matrix[i+1][j]
                elif((i==(nx-1) and j == 0) or (i == (nx-1) and j == (ny-1))):
                    nxt_matrix[i][j] = nxt_matrix[i-1][j]
                elif(((j==0) and i == 0) or ( j==0 and i == (nx -1))):
                    nxt_matrix[i][j] = nxt_matrix[i][j-1]
                elif((j==(ny-1) and i == 0) or (j==(ny-1) and i == (nx -1))):
                    nxt_matrix[i][j] = nxt_matrix[i][j+1]
                

    return nxt_matrix


act_matrix = build_matrix(act_x, act_y)

list = []
for instant in range(int(tempo_total/delta_t)):
    act_matrix = solve_matrix(act_matrix, act_x, act_y,instant)
    list.append(act_matrix)

def moments(i):
    return list[i]

img = plt.figure()
i = 0
iasd = [range(len(list))]
im = plt.imshow(moments(i),animated=True)

def updatefig(*args):
    global i
    i+=1
    im.set_array(moments(i))   
    return im,

ani = animation.FuncAnimation(img,updatefig,interval=5,blit=True)


cbar = img.colorbar(im, ticks=[0, 0.5, 1])
cbar.ax.set_yticklabels(['0', '0.5', '> 1']) 

plt.axis([0, 30, 0, 30])
plt.clim(0,1)
plt.legend()

plt.show()
