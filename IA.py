################################################################################
############################ Funcionalidad de la IA ############################
################################################################################


import random
import tkinter as tk
import tkinter.messagebox as mb
import pulp
import time
import threading

from game import generate_mines, generate_clues, vaciado, Victoria, Solucion
from mm_np import main_menu, new_play


def IA(minesweeper):
    """
    Parámetro:
    ----------
    minesweeper: Instancia buscaminas (Minesweeper)
    ----------
    Ejecuta la función principal de la IA:
    - Cambio de estado del indicador de IA
    - Simular movimientos
    """
    
    # Si IA no está activa
    if not minesweeper.IA:
        minesweeper.canvas.itemconfig(minesweeper.circle, fill="green")
        minesweeper.IA = True
        
        # Si el tablero está vacío, generarlo aleatoriamente
        if minesweeper.movs == 0:
            x = random.choice(range(minesweeper.B))
            y = random.choice(range(minesweeper.H))
            
            simulate_descubrir(minesweeper, y, x)
            
        # Ejecutar la IA en un hilo separado para no bloquear la interfaz
        threading.Thread(target=run_ia, args=(minesweeper,)).start()
            
    # Si IA está activa
    else:
        minesweeper.canvas.itemconfig(minesweeper.circle, fill="red")
        minesweeper.IA = False
        

def simulate_descubrir(minesweeper, y, x):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    y,x: Posición de la casilla a descubrir
    -----------
    Simula la función descubrir para la funcionalidad de IA
    """
    
    # Primer movimiento: Generación de minas
    if minesweeper.movs == 0:
        # Generar matriz de minas
        generate_mines(minesweeper, y, x)
        
        # Completar campo de minas
        generate_clues(minesweeper)
        
        # Actualizar primer movimiento
        minesweeper.movs = 1
    
    # Si no es una mina ni zona vacía
    if minesweeper.Estado[y,x] == 0 and minesweeper.Field[y,x] != 0 and \
    minesweeper.Field[y,x] != 9:
        
        minesweeper.Matrix[y,x].destroy()
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
        # Apagar IA si se gana
        minesweeper.IA = False
        won = mb.askyesno(title="Felicidades!!",
                          message="Has ganado :D\n¿Deseas reintentarlo (Sí) o" 
                          " ir al menú principal (No)?")
        if won:
            minesweeper.juego.after(0, lambda: new_play(minesweeper, False, 
                                                        minesweeper.modo))
        else:
            minesweeper.juego.after(0, lambda: main_menu(minesweeper, False))
    
    # Si se pulsa una mina
    elif minesweeper.Field[y,x] == 9:
        # Apagar IA si se pierde
        minesweeper.IA = False
        # Mostrar solución
        Solucion(minesweeper, y, x)
        lost = mb.askyesno(title="Has perdido",
                           message="Has perdido :(\n¿Deseas reintentarlo (Sí) "
                           "o ir al menú principal (No)?")
        if lost:
            minesweeper.juego.after(0, lambda: new_play(minesweeper, False, 
                                                        minesweeper.modo))
        else:
            minesweeper.juego.after(0, lambda: main_menu(minesweeper, False))
    

    # Permitir que la interfaz gráfica se actualice
    time.sleep(0.5)
    minesweeper.juego.update()


def run_ia(minesweeper):
    """
    Parámetro:
    ----------
    minesweeper: Instancia buscaminas (Minesweeper)
    ----------
    Ejecuta el algoritmo de la IA basado en un problema de programación lineal 
    y entera. Cuando encuentra casillas que no son mina al 100%, las decubre. 
    Si no hay, descubre aleatoriamente.
    """
    
    while minesweeper.IA:
        # Recoger posiciones donde hay una casilla descubierta alrededor de 
        # alguna casilla desconocida
        abiertas = get_open(minesweeper)
              
        # Problema de programación lineal y entera
        prob = pulp.LpProblem("Minesweeper_AI", pulp.LpMaximize)
        
        # Resolver el problema
        status, var_map = solve_problem(minesweeper, abiertas, prob)
        
        # Si el resultado del problema es óptimo
        if status == 1:
            # Lista con las posibles zonas vacías
            posibles_vacias = [var for var in var_map if var_map[var].varValue 
                               == 0]
            
            # Comprobación zonas 100% vacías
            vacias_100x100 = get_vacias_100x100(prob, var_map, posibles_vacias)
    
            # Si hay vacias 100%
            if vacias_100x100:            
                # Descubrir casillas que no son mina 100%
                for y, x in vacias_100x100:
                    simulate_descubrir(minesweeper, y, x)
            
            # Si no hay vacías 100%
            # Si se desea que se pregunte
            want_random = True
            if minesweeper.IA_random:
                # Descubrir al azar de las posibles no minas (Primero pregunta 
                # al usuario)
                want_random = mb.askyesno(title="Opción aleatoria",
                                          message="El siguiente movimiento será"
                                          " generado de manera aleatoria."
                                          "\n¿Deseas continuar?")
            if want_random:
                y, x = random.choice(posibles_vacias)
                simulate_descubrir(minesweeper, y, x)
            else:
                minesweeper.juego.after(0, lambda: IA(minesweeper))
                break
                    
            # Pausa entre cada iteración para permitir verificar la condición 
            # de parada
            time.sleep(0.5)


def get_open(minesweeper):
    """
    Parámetro:
    ----------
    minesweeper: Instancia buscaminas (Minesweeper)
    ----------
    Devuelve:
    ---------
    abiertas: Lista con las casillas abiertas que contiene casillas cerradas en 
    su vecindario.
    ---------
    Revorre por cada casilla del tablero, si una casilla está intacta, recorre 
    su vecindario por si encuentra alguna casilla abierta. Esta casilla abierta 
    se guarda.
    """
    
    abiertas = []  # Lista con las casillas abiertas con cerradas adyacentes
    for y in range(minesweeper.H):
        for x in range(minesweeper.B):
            if minesweeper.Estado[y,x] == 0:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        ny, nx = y + i, x + j
                        if 0 <= ny <= minesweeper.H-1 and 0 <= nx <= \
                        minesweeper.B-1:
                            if minesweeper.Estado[ny,nx] == 1 and (ny,nx) not \
                            in abiertas:
                                abiertas += [(ny,nx)]
    
    return abiertas


def solve_problem(minesweeper, abiertas, problem):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    abiertas: Lista con las casillas abiertas que contiene casillas cerradas en 
    su vecindario
    
    problem: Problema de programación lineal y entera
    -----------
    Devuelve:
    ---------
    status: Estado de la solución del problema:
        -1 = Infeasible; 1 = Optimal
        
    var_map: Diccionario con la posición de cada casilla incógnita y su valor
    ---------
    Por cada casilla abierta, encuentra las casillas no abiertas adyacentes. 
    Por cada una de estas se crea una variable de pulp.
    Por cada casilla abierta se crea una ecuación del problema de la forma:
        sum(variables) = número de minas
    Finalmente, resuelve el problema
    """
    
    # Inicializar mapa de variables
    var_map = {}  # Diccionario donde las llaves son posiciones y los 
    # valores son las variables de esas posiciones
                
    # Añadir ecuaciones al problema
    for (y,x) in abiertas:
        numero = minesweeper.Field[y,x]
        vars = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                ny, nx = y + i, x + j
                if 0 <= ny <= minesweeper.H-1 and 0 <= nx <= minesweeper.B-1:
                    # Crear variables de las posiciones no abiertas
                    if minesweeper.Estado[ny, nx] == 0:
                        if (ny,nx) not in var_map:
                            var_map[(ny, nx)] = pulp.LpVariable(str((ny, nx)), 
                                                                0, 1, 
                                                                pulp.LpInteger)
                        vars += [var_map[(ny, nx)]]        
        if vars:
            problem += pulp.lpSum(vars) == numero
                
        # Solución del sistema
        status = problem.solve(pulp.PULP_CBC_CMD(msg=0))
            
        assert status in [-1, 1]  # Infeasible = -1; Optimal = 1
    
    return status, var_map


def get_vacias_100x100(problem, var_map, posibles_vacias):
    """
    Parámetros:
    -----------
    problem: Problema de programación lineal y entera
    
    var_map: Diccionario con la posición de cada casilla incógnita y su valor
    
    posibles_vacias: Lista con las posiciones de las casillas que no contienen 
    mina, a priori.
    -----------
    Devuelve:
    ---------
    vacias_100x100: Sublista de posibles_vacias. Lista con las posiciones de 
    las casillas que no contienen mina al 100%.
    ----------
    Para cada casilla que posiblemente no contiene mina, se copia el programa 
    de programación lineal y entera y se añade una nueva ecuación, forzando que 
    en esa posición haya mina. Si, al resolver de nuevo el problema, el sistema 
    es inviable (Infeasible), ahí no hay mina de verdad
    """
    
    vacias_100x100 = []
    # Iterar el proceso para cada posible mina suponiendo que no es mina
    for pos in posibles_vacias:
        new_status = check_solution(problem.copy(), var_map, pos)
        # Si es infeasible significa que no es mina 100%:
        if new_status == -1:
            vacias_100x100 += [pos]
    
    return vacias_100x100

  
def check_solution(problem, var_map, position):
    """
    Parámetros:
    -----------
    problem: Problema de programación lineal y entera
    
    var_map: Diccionario con la posición de cada casilla incógnita y su valor
    
    position: Posición de la casilla que se quiere forzar mina
    -----------
    Devuelve:
    ---------
    status: Estado de la solución del nuevo problema:
        -1: Infeasible; 1: Optimal
    ---------
    Crea una condición más al problema problem, para forzar que 
    var_map[position] sea una mina. Finalmente, se resuelve el problema.
    """
    
    # Forzar valor = 1 (hay mina)
    problem += var_map[position] == 1
    
    # Resolver el problema
    status = problem.solve(pulp.PULP_CBC_CMD(msg=0))
    assert status in [-1, 1]  # -1: Infeasible, 1: Optimal
    
    return status
