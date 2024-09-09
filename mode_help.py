################################################################################
####################### Función para obtener información #######################
#######################      de los modos de juego      ########################
################################################################################


import tkinter.messagebox as mb


def mode_help(modo):
    """
    Parámetro:
    -----------
    modo: Tipo de modo de juego:
        "principiante", "intermedio", "experto", "personalizado"
    -----------
    Ejecuta un messagebox con la información de ese modo de juego
    """
    
    match modo:
        case "principiante":
            mb.showinfo(message="- 8x8 casillas\n- 10 minas", 
                        title="Principiante")
        case "intermedio":
            mb.showinfo(message="- 16x16 casillas\n- 40 minas",
                        title="Intermedio")
        case "experto":
            mb.showinfo(message="- 16x30 casillas\n- 99 minas",
                        title="Experto")
        case "personalizado":
            mb.showinfo(message="- Altura: 8-24\n- Ancho: 8-32\n"
                        "- Bombas: 1 a 1/3 de cuadrados", 
                        title="Personalizado")
