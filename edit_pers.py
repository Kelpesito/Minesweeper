################################################################################
################### Funciones para establecer los parámetros ###################
###################       De una partida personalizada       ###################
################################################################################


import tkinter as tk
import tkinter.messagebox as mb


def param_pers(minesweeper):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    -----------
    Crea la pantalla para introducir los parámetros de la partida personalizada
    """
    
    FUENTE = ("Courier New", 15)
    FONDO = "#898989"
        
    # Ventana para selección de parámetros partida personalizada
    pers_Config = tk.Tk()
    pers_Config.title("Buscaminas")
    pers_Config.geometry("400x400")
    pers_Config.configure(bg=FONDO)
    
    # Número de columnas
    B_Label = tk.Label(pers_Config, text="Número de columnas:", font=FUENTE,
                       bg=FONDO)
    B_Label.grid(row=0, column=0, padx=2, pady=2)

    B_Entry = tk.Entry(pers_Config, font=FUENTE, width=5)
    B_Entry.grid(row=0, column=1, padx=2, pady=2)
    
    # Número de filas
    H_Label = tk.Label(pers_Config, text="Número de filas:", font=FUENTE,
                    bg=FONDO)
    H_Label.grid(row=1, column=0, padx=2, pady=2)

    H_Entry = tk.Entry(pers_Config, font=FUENTE, width=5)
    H_Entry.grid(row=1, column=1, padx=2, pady=2)
    
    # Número de minas
    MINAS_Label = tk.Label(pers_Config, text="Número de minas:", font=FUENTE,
                           bg=FONDO)
    MINAS_Label.grid(row=2, column=0, padx=2, pady=2)
    
    MINAS_Entry = tk.Entry(pers_Config, font=FUENTE, width=5)
    MINAS_Entry.grid(row=2, column=1, padx=2, pady=2)
    
    # Submit button
    submit_Button = tk.Button(pers_Config, text="Aceptar", font=FUENTE,
                              command=lambda: submit_Pers(minesweeper, B_Entry, 
                                                          H_Entry, MINAS_Entry,
                                                          pers_Config))
    submit_Button.grid(row=3, pady=4)
    
    # Cancel button
    cancel_Button = tk.Button(pers_Config, text="Cancelar", font=FUENTE,
                              command=lambda: cancel_Pers(minesweeper, 
                                                          pers_Config))
    cancel_Button.grid(row=3, column=1, pady=4)
    
    # Bucle de la ventana de personalización
    pers_Config.mainloop()
    

def submit_Pers(minesweeper, B_Entry, H_Entry, MINAS_Entry, 
                pers_Config):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    B_Entry: Entry con información del número de columnas
    
    H_Entry: Entry con información del número de filas
    
    MINAS_Entry: Entry con información del número de minas
    
    pers_Config: Ventana perteneciente a la personalización de los parámetros
    de la partida personalizada
    -----------
    Establece los parámetros de la partida personalizada.
    """
    
    try:
        # Obtener parámetros introducidos por el usuario
        B = int(str(B_Entry.get()))
        H = int(str(H_Entry.get()))
        MINAS = int(str(MINAS_Entry.get()))
        
        # Error si no cumple las especificaciones de dimensiones
        if not (8 <= H <= 24 and 8 <= B <= 32 and 1 <= MINAS <= 1 / 3 * H * B):
            mb.showerror(title="Error!",
                         message="Parámetros incorrectos. Debe ser:\n - Número "
                         "de filas: 8-24\n- Número de columnas: 8-32\n- Número "
                         "de minas: 1-1/3 de cuadrados")
        else:
            pers_Config.destroy()
            
            minesweeper.B, minesweeper.H, minesweeper.MINAS = B, H, MINAS
            
    # Error si se introducen caracteres
    except Exception:
        mb.showerror(title="Error!", message="Introduce únicamente números")

def cancel_Pers(minesweeper, pers_Config):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    
    pers_Config: Ventana perteneciente a la personalización de los parámetros
    de la partida personalizada
    -----------
    Destruye la ventana de personalizar partida y vuelve a empezar el programa.
    """
    
    # Destruir ventana partida personalizada
    pers_Config.destroy()
    
    # Comenzar de nuevo
    minesweeper.main()
    