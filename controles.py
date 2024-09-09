################################################################################
################# Funciones para darle controles a los botones: ################
#################                  - Descubrir                  ################
#################                   - Bandera                   ################
#################                - Interrogante                 ################
################################################################################


from functools import partial
import tkinter as tk
import tkinter.messagebox as mb
import numpy as np

from game import Victoria, generate_mines, generate_clues, vaciado, Solucion
from mm_np import main_menu, new_play


def bind_controles(minesweeper, y=None, x=None, Descubrir=None, Bandera=None, 
                   Interrogante=None):
    """
    Parámetro:
    ----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    y,x: Posición que se desea asignar controles
    
    Descubrir: Booleano si se desea asignar control descubrir()
    
    Bandera: Booleano si se desea asignar control bandera()
    
    Interrogante: Booleano si se desea asignar control interrogante()
    ----------
    Proporciona los controles a los botones del tablero:
        Clic izquierdo: Descubrir
        Clic central: Interrogante
        Clic derecho: Bandera
    """
    
    # Proporcionar controles en general
    if (y,x) == (None, None):
        for i in range(minesweeper.H):
            for j in range(minesweeper.B):
                minesweeper.Matrix[i,j].bind("<Button-1>", 
                                             partial(descubrir, 
                                                     minesweeper=minesweeper))
                minesweeper.Matrix[i,j].bind("<Button-3>",
                                             partial(bandera, 
                                                     minesweeper=minesweeper))
                minesweeper.Matrix[i,j].bind("<Button-2>",
                                             partial(interrogante, 
                                                     minesweeper=minesweeper))
    
    else:
        # Darle clic izquierdo a casilla particular
        if Descubrir:
            minesweeper.Matrix[y,x].bind("<Button-1>", 
                                         partial(descubrir, 
                                                 minesweeper=minesweeper))
        
        # Darle clic central a casilla particular
        if Interrogante:
            minesweeper.Matrix[y,x].bind("<Button-2>",
                                         partial(interrogante, 
                                                 minesweeper=minesweeper))
        
        # Darle clic derecho a casilla aparticular
        if Bandera:
            minesweeper.Matrix[y,x].bind("<Button-3>",
                                         partial(bandera, 
                                                 minesweeper=minesweeper))
    

def descubrir(event, minesweeper):
    """
    Parámetros:
    -----------
    event: Botón izquierdo del ratón
    
    minesweeper: Instancia buscaminas (Minesweeper)
    -----------
    Si la casilla tiene número, cambia el botón por un el número.
    Si la casilla está vacía, descubre toda la zona vacía.
    Si la casilla es una mina, has perdido y descubre la solución.
    Finalmente, comprueba si se ha ganado.
    El tablero se crea en el primer movimiento, para asegurar que no se 
    encuentra una bomba de primeras.
    """
    
    # Posición botón
    y = event.widget.y
    x = event.widget.x
    
    # Primer movimiento: Creación de las minas
    if minesweeper.movs == 0:
        # Generar la matriz de minas
        generate_mines(minesweeper, y, x)
        
        # Completar campo de minas
        generate_clues(minesweeper)

        # Actualizar primer movimiento
        minesweeper.movs = 1
    
    # Si no es ni mina ni zona vacía
    if minesweeper.Estado[y,x] == 0 and minesweeper.Field[y,x] != 0 and \
    minesweeper.Field[y,x] != 9:
        event.widget.destroy()
        minesweeper.Matrix[y,x] = tk.Label(minesweeper.Game,
                                           image=minesweeper.imagenes
                                           [minesweeper.Field[y,x]],
                                           borderwidth=0)
        minesweeper.Matrix[y,x].image = minesweeper.imagenes[minesweeper.Field
                                                             [y,x]]
        minesweeper.Matrix[y,x].grid(row=y, column=x, padx=1, pady=1)
        minesweeper.Estado[y,x] = 1
        
    # Si es una zona vacía
    elif minesweeper.Estado[y,x] == 0 and minesweeper.Field[y,x] == 0:
        vaciado(minesweeper, y, x)
        
    # Si se ha ganado
    if Victoria(minesweeper):
        won = mb.askyesno(title="Felicidades!!",
                          message="Has ganado :D\n¿Deseas reintentarlo (Sí) o" 
                          " ir al menú principal (No)?")
        if won:
            new_play(minesweeper, False, minesweeper.modo)
        else:
            main_menu(minesweeper, False)
    
    # Si se pulsa una mina
    if minesweeper.Field[y,x] == 9:
        # Mostrar solución
        Solucion(minesweeper, y, x)
        lost = mb.askyesno(title="Has perdido",
                           message="Has perdido :(\n¿Deseas reintentarlo (Sí) "
                           "o ir al menú principal (No)?")
        if lost:
            new_play(minesweeper, False, minesweeper.modo)
        else:
            main_menu(minesweeper, False)
    
    
def bandera(event, minesweeper):
    """
    Parámetros:
    -----------
    event: Botón derecho del ratón
    
    minesweeper: Instancia buscaminas (Minesweeper)
    -----------
    Si la casilla está vacía, cambia el botón por una bandera.
    Si la casilla tiene una bandera, lo cambia por un botón.
    """
    
    # Posición botón
    y = event.widget.y
    x = event.widget.x
    
    # Si botón intacto
    if minesweeper.Estado[y,x] == 0:
        event.widget.destroy()
        minesweeper.Matrix[y,x] = tk.Label(minesweeper.Game,
                                           image=minesweeper.imagenes
                                           ["bandera"], borderwidth=0)
        minesweeper.Matrix[y,x].image = minesweeper.imagenes["bandera"]
        minesweeper.Matrix[y,x].y = y
        minesweeper.Matrix[y,x].x = x
        minesweeper.Matrix[y,x].grid(row=y, column=x, padx=1, pady=1)
        minesweeper.Estado[y,x] = -1
        
        minesweeper.Minas_Restantes -= 1
        minesweeper.Minas_Restantes_Var.set(str(minesweeper.Minas_Restantes))
        
        # Dar efecto de nuevo
        bind_controles(minesweeper=minesweeper, y=y, x=x, Bandera=True)
    
    # Si hay bandera
    elif minesweeper.Estado[y,x] == -1: 
        event.widget.destroy()
        minesweeper.Matrix[y,x] = tk.Label(minesweeper.Game, width=2, height=1,
                                           font=("Courier New", 12),
                                           bg=minesweeper.FONDO_BOTONES,
                                           activebackground=minesweeper.
                                           FONDO_BOTONES)
        minesweeper.Matrix[y,x].y = y
        minesweeper.Matrix[y,x].x = x
        minesweeper.Matrix[y,x].grid(row=y, column=x, padx=1, pady=1)
        minesweeper.Estado[y,x] = 0
        
        minesweeper.Minas_Restantes += 1
        minesweeper.Minas_Restantes_Var.set(str(minesweeper.Minas_Restantes))
        
        # Dar efecto de nuevo
        bind_controles(minesweeper, y=y, x=x, Descubrir=True, Bandera=True, 
                       Interrogante=True)


def interrogante(event, minesweeper):
    """
    Parámetros:
    -----------
    event: Botón central del ratón
    
    minesweeper: Instancia buscaminas (Minesweeper)
    -----------
    Si la casilla está vacía, cambia el botón por un interrogante.
    Si la casilla tiene un interrogante, lo cambia por un botón.
    """
    
    # Posición botón
    y = event.widget.y
    x = event.widget.x

    # Si botón intacto
    if minesweeper.Estado[y,x] == 0:
        event.widget.destroy()
        minesweeper.Matrix[y,x] = tk.Label(minesweeper.Game,
                                           image=minesweeper.imagenes
                                           ["interrogante"], borderwidth=0)
        minesweeper.Matrix[y,x].image = minesweeper.imagenes["interrogante"]
        minesweeper.Matrix[y,x].y = y
        minesweeper.Matrix[y,x].x = x
        minesweeper.Matrix[y,x].grid(row=y, column=x, padx=1, pady=1)
        minesweeper.Estado[y,x] = 2
        
        # Dar efecto de nuevo
        bind_controles(minesweeper, y=y, x=x, Interrogante=True)
    
    # Si hay interrogante
    elif minesweeper.Estado[y,x] == 2:
        event.widget.destroy()
        minesweeper.Matrix[y,x] = tk.Label(minesweeper.Game, width=2, height=1,
                                           font=("Courier New", 12),
                                           bg=minesweeper.FONDO_BOTONES,
                                           activebackground=minesweeper.
                                           FONDO_BOTONES)
        minesweeper.Matrix[y,x].y = y
        minesweeper.Matrix[y,x].x = x
        minesweeper.Matrix[y,x].grid(row=y, column=x, padx=1, pady=1)
        minesweeper.Estado[y,x] = 0
        
        # Dar efecto de nuevo
        bind_controles(minesweeper, y=y, x=x, Descubrir=True, Bandera=True, 
                       Interrogante=True)
