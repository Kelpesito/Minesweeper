################################################################################
####################   Funciones varias para la partida:    ####################
####################      - Generar matriz de botones       ####################
####################            - Generar minas             ####################
####################         - Generar los números          ####################
####################         - Vaciar zonas vacías          ####################
####################      - Comprobar si se ha ganado       ####################
#################### - Mostrar la solución cuando se pierde ####################
################################################################################


import numpy as np
import tkinter as tk
import random


def generate_matrix(minesweeper):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    -----------
    Genera la matriz de botones de la partida
    """
    
    # Generar la matriz
    minesweeper.Matrix = np.empty((minesweeper.H, minesweeper.B), dtype=object)
    for i in range(minesweeper.H):
        for j in range(minesweeper.B):
            minesweeper.Matrix[i,j] = tk.Label(minesweeper.Game, width=2, 
                                               height=1,
                                               font=minesweeper.
                                               FUENTE_MINAS_RESTANTES, 
                                               bg=minesweeper.FONDO_BOTONES,
                                               activebackground=minesweeper.
                                               FONDO_BOTONES)
            minesweeper.Matrix[i,j].y = i
            minesweeper.Matrix[i,j].x = j
            minesweeper.Matrix[i,j].grid(row=i, column=j, padx=1, pady=1)


def generate_mines(minesweeper, yo, xo):
    """
    Parámetros:
    ----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    yo, xo: Posición del primer clic
    ----------
    Genera aleatoriamente el campo de minas.
        Si = 0: No hay mina
        Si = 9: Hay mina
    """

    # Generar la matriz de minas
    minas = minesweeper.MINAS
    while minas > 0:
        x = random.choice(range(minesweeper.B))
        y = random.choice(range(minesweeper.H))
        if minesweeper.Field[y,x] == 0 and (y,x) != (yo,xo):
            minesweeper.Field[y,x] = 9
            minas -= 1


def generate_clues(minesweeper):
    """
    Parámetros:
    ----------
    minesweeper: Instancia buscaminas (Minesweeper)
    ----------
    Genera las pistas del campo de minas. Las pistas dicen el número de minas
    que hay alrededor de cada casilla.
    """
    
    # Acabar campo de minas (generar pistas)
    for i in range(minesweeper.H):
        for j in range(minesweeper.B):
            if minesweeper.Field[i,j] != 9:
                cont = 0
                for a in range(i-1, i+2):
                    for b in range(j-1, j+2):
                        if 0 <= a < minesweeper.H and 0 <= b < minesweeper.B:
                            if minesweeper.Field[a,b] == 9:
                                cont += 1
                minesweeper.Field[i,j] = cont


def vaciado(minesweeper, y, x):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    y: posición y del widget
    
    x: posición x del widget
    -----------
    La función se encarga de descubrir una zona vacía cuando se pulsa una
    casilla vacía. También descubre los números en la frontera.
    """
    
    ceros = [(y, x)]
    visitados = set()  # Un conjunto para rastrear casillas ya visitadas
    
    while len(ceros) > 0:
        cy, cx = ceros.pop()
        
        # No procesar una casilla más de una vez
        if (cy, cx) not in visitados:
            visitados.add((cy, cx))  # Marca la casilla como visitada
            
            # Recorrer entorno de la casilla
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    ny, nx = cy + i, cx + j
                    
                    if 0 <= ny < minesweeper.H and 0 <= nx < minesweeper.B and \
                    minesweeper.Estado[ny, nx] != 1:  
                        minesweeper.Estado[ny, nx] = 1
                            
                        if minesweeper.Field[ny, nx] == 0:
                            ceros.append((ny, nx))
                            
                        # Actualizar la matriz visual del juego
                        minesweeper.Matrix[ny, nx] = \
                            tk.Label(minesweeper.Game,
                                     image=minesweeper.imagenes[minesweeper.
                                                                Field[ny, nx]],
                                     borderwidth=0)
                        minesweeper.Matrix[ny, nx].image = minesweeper.imagenes
                        [minesweeper.Field[ny, nx]]
                        minesweeper.Matrix[ny, nx].grid(row=ny, column=nx, 
                                                        padx=1, pady=1)
 

def Victoria(minesweeper):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    -----------
    Comprueba si se ha ganado la partida:
        Las casillas que no son minas han sido descubiertas 
    """
    
    for i in range(minesweeper.H):
        for j in range(minesweeper.B):
            if minesweeper.Field[i,j] != 9 and minesweeper.Estado[i,j] != 1:
                return False
    return True 


def Solucion(minesweeper, y, x):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    y,x: Posición de la casilla pulsada
    -----------
    Muestra la solución del tablero, inculuidos la bomba que se ha fallado y 
    las banderas que se han puesto mal.
    """
    
    minesweeper.Game.destroy()

    End = tk.Frame(minesweeper.juego)
    End.pack(pady=30)
    End.configure(bg="black")
    
    solucion = np.empty((minesweeper.H, minesweeper.B), dtype=object)
    for i in range(minesweeper.H):
        for j in range(minesweeper.B):
            # Rellenar números y huecos (si no se ha supuesto bomba)
            if minesweeper.Field[i,j] != 9 and minesweeper.Estado[i,j] != -1:
                solucion[i,j] = tk.Label(End,
                                         image=minesweeper.imagenes[minesweeper.
                                                                    Field[i,j]],
                                         borderwidth=0)
                solucion[i,j].grid(row=i, column=j, padx=1, pady=1)
            
            # Rellenar mina pulsada
            elif i == y and j == x:
                solucion[i,j] = tk.Label(End,
                                         image=minesweeper.imagenes
                                         ["bombdeath"], borderwidth=0)
                solucion[i,j].grid(row=i, column=j, padx=1, pady=1)
            
            # Rellenar minas acertadas
            elif minesweeper.Estado[i,j] == -1 and minesweeper.Field[i,j] == 9:
                solucion[i,j] = tk.Label(End,
                                         image=minesweeper.imagenes
                                         ["bandera"], borderwidth=0)
                solucion[i,j].grid(row=i, column=j, padx=1, pady=1)
            
            # Rellenar minas falladas
            elif minesweeper.Estado[i,j] == -1 and minesweeper.Field[i,j] != 9:
                solucion[i,j] = tk.Label(End,
                                         image=minesweeper.imagenes
                                         ["bombmisflagged"], borderwidth=0)
                solucion[i,j].grid(row=i, column=j, padx=1, pady=1)
            
            # Rellenar minas no encontradas / faltantes
            else:
                solucion[i,j] = tk.Label(End,
                                         image=minesweeper.imagenes
                                         ["bombrevealed"], borderwidth=0)
                solucion[i,j].grid(row=i, column=j, padx=1, pady=1)
                