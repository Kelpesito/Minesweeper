################################################################################
################### Funciones para volver al menú principal ####################
###################       O empezar una nueva partida       ####################
################################################################################


import tkinter.messagebox as mb


def new_play(minesweeper, boolean, modo):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    boolean: Booleano que indica si la nueva partida viene de fin de partida
    (False) o de querer reiniciar (True).
        
    modo: Modo de juego:
        "principiante", "intermedio", "experto", "personalizado".
    -----------
    Pregunta si quieres empezar una nueva partida.
    """
    
    if boolean:
        NewPlay = mb.askokcancel(title="Empezar una nueva partida?",
                                 message="¿Desea empezar una nueva partida?")
    else:
        NewPlay = True
        
    if NewPlay:
        minesweeper.juego.destroy()
        minesweeper.game(modo, False)
   
        
def main_menu(minesweeper, boolean):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    boolean: Booleano que indica si la nueva partida viene de fin de partida
    (False) o de querer reiniciar (True).
    -----------
    Pregunta si quieres ir al menú principal.
    """
    
    if boolean:
        salir = mb.askokcancel(title="Salir al menú principal?",
                               message="¿Desea salir al menú principal?")
    else:
        salir = True
    
    if salir:
        minesweeper.juego.destroy()
        minesweeper.main()
    