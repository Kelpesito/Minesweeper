################################################################################
#################                  Buscaminas                  #################
################# Creación del objeto Buscaminas (Minesweeper) #################
#################      Y Ejecución principal del programa      #################
################################################################################


import tkinter as tk
import tkinter.messagebox as mb
from PIL import Image, ImageTk
import numpy as np

from mode_help import mode_help
from edit_pers import param_pers
from mm_np import main_menu, new_play
from game import generate_matrix
from controles import bind_controles
from load_images import load_images
from IA import IA
from centrar_ventana import centrar_ventana
from resource_path import resource_path


class Minesweeper():
    
    def __init__(self):
        """
        Inicializa constantes.
        """
    
        self.COLOR_PRINCIPIANTE = "#B7F377"  # Color principiante
        self.COLOR_INTERMEDIO = "#FAF36C"  # Color intermedio
        self.COLOR_EXPERTO = "#FA6C6C"  # Color experto
        self.COLOR_PERSONALIZADO = "#B9FFF1"  # Color personalizado
        
        self.FUENTE_TITULO = ("Courier New", 40, "bold")  # Fuente título
        self.FUENTE_MAIN = ("Courier New", 25)  # Fuente del menú principal
        self.FUENTE = ("Courier New", 10)  # Fuente de la partida
        self.FUENTE_MINAS_RESTANTES = ("Courier New", 12)  # Fuente de 
        # indicador de minas restantes
        self.FUENTE_EDIT_PERS = ("Courier New", 15)  # Fuente de la pantalla de 
        # personalización de partida personalizada
                
        self.FONDO = "#898989"  # Color fondo  
        self.FONDO_BOTONES = "#7d7c7c"  # Color fondo botones de la partida
        self.FONDO_BOTONES_MAIN = "#d1d1d1"  # Color fondo botones del menú 
        # principal 
        
        self.INFO_GAME = {"principiante": [8,8,10], "intermedio": [16,16,40], 
                          "experto": [30,16,99]}  # Diccionario con base, 
        # altura y número de minas de cada modo
        
        self.modo = None  # Modo de juego
        self.B = None  # Ancho del tablero
        self.H = None  # Alto del tablero
        self.MINAS = None  # Número de minas
        
        self.IA = None  # Estado de IA
        
        # Definir si IA genera elementos random o lo hace el usuario
        with open(resource_path("random_on_of/random_on_of.txt")) as file:
            content = file.read().strip().lower()
            self.IA_random = True if content == "on" else False if content == \
            "off" else None

    
    def main(self):
        """
        Ejecución principal del programa.
        
        Menú principal
        """
        
        # Reinicialización de las variables
        self.__init__()
        
        ## Menú principal
        # Configuración ventana menú principal
        self.ventana = tk.Tk()
        self.ventana.title("Buscaminas")
        self.ventana.geometry("500x500")
        centrar_ventana(self.ventana, width=500, height=500)
        self.ventana.configure(bg=self.FONDO)
        
        # Icono
        icono = tk.PhotoImage(file=resource_path("1f4a3.png"))
        self.ventana.iconphoto(True, icono)
        
        # Título
        titulo = tk.Label(self.ventana, text="Buscaminas", 
                          font=self.FUENTE_TITULO, justify=tk.CENTER,
                          bg=self.FONDO)
        titulo.pack(pady=10)
        
        # Subtítulo
        np_Label = tk.Label(self.ventana, text="Nueva partida",
                            font=self.FUENTE_MAIN, justify=tk.CENTER,
                            bg=self.FONDO)
        np_Label.pack(pady=20)
        
        # Frame botones
        frame = tk.Frame(self.ventana, bg=self.FONDO)
        frame.pack()
        
        # Botón dificultad principiante
        prin_Button = tk.Button(frame, text="Principiante", 
                                font=self.FUENTE_MAIN,
                                bg=self.COLOR_PRINCIPIANTE,
                                activebackground=self.COLOR_PRINCIPIANTE,
                                justify=tk.CENTER, width=15,
                                command=lambda: self.game("principiante", True))
        prin_Button.grid(row=0, column=0)
        
        # Botón información dificultad principiante
        help1 = tk.Button(frame, bitmap="question", width=50, height=57,
                          bg=self.COLOR_PRINCIPIANTE,
                          activebackground=self.COLOR_PRINCIPIANTE,
                          command=lambda: mode_help("principiante"))
        help1.grid(row=0, column=1, padx=7)
        
        # Botón dificultad intermedia
        int_Button = tk.Button(frame, text="Intermedio", font=self.FUENTE_MAIN,
                               bg=self.COLOR_INTERMEDIO,
                               activebackground=self.COLOR_INTERMEDIO,
                               justify=tk.CENTER, width=15,
                               command=lambda: self.game("intermedio", True))
        int_Button.grid(row=1, column=0, pady=7)
        
        # Botón información dificultad intermedia
        help2 = tk.Button(frame, bitmap="question", width=50, height=57,
                          bg=self.COLOR_INTERMEDIO, 
                          activebackground=self.COLOR_INTERMEDIO,
                          command=lambda: mode_help("intermedio"))
        help2.grid(row=1, column=1, padx=7)
        
        # Botón dificultad experto
        exp_Button = tk.Button(frame, text="Experto", font=self.FUENTE_MAIN,
                               bg=self.COLOR_EXPERTO, 
                               activebackground=self.COLOR_EXPERTO,
                               justify=tk.CENTER, width=15,
                               command=lambda: self.game("experto", True))
        exp_Button.grid(row=2, column=0, pady=7)
        
        # Botón información dificultad experto
        help3 = tk.Button(frame, bitmap="question", width=50, height=57,
                          bg=self.COLOR_EXPERTO,
                          activebackground=self.COLOR_EXPERTO,
                          command=lambda: mode_help("experto"))
        help3.grid(row=2, column=1, padx=7)
        
        # Botón dificultad personalizada
        pers_Button = tk.Button(frame, text="Personalizado", 
                                font=self.FUENTE_MAIN,
                                bg=self.COLOR_PERSONALIZADO,
                                activebackground=self.COLOR_PERSONALIZADO,
                                justify=tk.CENTER, width=15,
                                command=lambda: self.game("personalizado", 
                                                          True))
        pers_Button.grid(row=3, column=0, pady=7)
        
        # Botón información dificultad personalizada
        help4 = tk.Button(frame, bitmap="question", width=50, height=57,
                          bg=self.COLOR_PERSONALIZADO,
                          activebackground=self.COLOR_PERSONALIZADO,
                          command=lambda: mode_help("personalizado"))
        help4.grid(row=3, column=1, padx=7)
        
        # Bucle ventana
        self.ventana.mainloop()
        
    
    def game(self, modo, boolean):
        """
        Parámetros:
        -----------
        modo: Modo de juego:
            "principiante", "intermedio", "experto", "personalizado".
            
        boolean: Boolean si se procede del menú principal (True) o de juego 
        (False)
        -----------
        Ejecución principal del juego.
        """
        self.modo = modo
        
        # Destrucción del menú principal si viene de este
        if boolean:
            self.ventana.destroy()
            
        # Asignación de las variables a los modos generales
        if self.modo != "personalizado":
            self.B, self.H, self.MINAS = self.INFO_GAME[self.modo]
        
        # Elegir parámetros de la partida personalizada
        else:
            param_pers(self)
            
        # Generar juego
        if (self.B, self.H, self.MINAS) != (None, None, None):
            self.generate_game()
            
            # Estado actual de las casillas
            size = [self.H, self.B]
            self.Estado = np.zeros(size, dtype=int)
            
            self.Field = np.zeros(size, dtype=int)
            
            self.movs = 0  # Variable si se ha hecho el primer movimiento
            self.IA = False  # Booleano que indica si IA está activa
        
            # Asignación de controles
            bind_controles(self)
        
            # Bucle de juego
            self.juego.mainloop()
            
            
    def generate_game(self):
        """
        Crea la ventana del juego.
        Crea la matriz de botones.
        """
        
        ## Pantalla de juego
        # Configuración de la pantalla
        self.juego = tk.Tk()
        self.juego.title("Buscaminas")
        
        size = (self.B, self.H)
        button_width = 30
        button_height = 30
        window_padding = 150
        extra_padding_height = 80 
        
        ancho_ventana = size[0] * button_width + window_padding
        alto_ventana = size[1] * button_height + extra_padding_height
        self.juego.geometry(f"{ancho_ventana}x{alto_ventana}")
        centrar_ventana(self.juego, width=ancho_ventana, height=alto_ventana)
        self.juego.configure(bg=self.FONDO)
        
        # Barra de opciones
        bar_Frame = tk.Frame(self.juego)
        bar_Frame.pack()
        bar_Frame.config(bg=self.FONDO, height=50)
        
        # Botón de nueva partida
        np_Button = tk.Button(bar_Frame, text="Nueva partida", font=self.FUENTE,
                              bg=self.FONDO_BOTONES_MAIN,
                              activebackground=self.FONDO_BOTONES_MAIN,
                              command=lambda: new_play(self, True, self.modo))
        np_Button.grid(row=0, column=0, padx=5)
        
        # Botón de ir al menú principal
        mp_Button = tk.Button(bar_Frame, text="Menú principal",
                              font=self.FUENTE, bg=self.FONDO_BOTONES_MAIN, 
                              activebackground=self.FONDO_BOTONES_MAIN,
                              command=lambda: main_menu(self, True))
        mp_Button.grid(row=0, column=1, padx=5)
        
        # Label minas restantes
        self.Minas_Restantes = self.MINAS
        self.Minas_Restantes_Var = tk.StringVar()
        self.Minas_Restantes_Var.set(str(self.Minas_Restantes))
        tempo_Label = tk.Label(bar_Frame, textvariable=self.Minas_Restantes_Var,
                               font=self.FUENTE_MINAS_RESTANTES, bg="black", 
                               fg="red")
        tempo_Label.grid(row=0, column=3, padx=5)
        
        # Indicador IA
        self.canvas = tk.Canvas(bar_Frame, width=30, height=30, bg=self.FONDO,
                                highlightthickness=0, bd=0, relief="flat")
        self.circle = self.canvas.create_oval(2, 2, 28, 28, fill="red")
        self.canvas.grid(row=0, column=5, padx=5)

        # Frame tablero
        self.Game = tk.Frame(self.juego)
        self.Game.pack(pady=30)
        self.Game.configure(bg="black")
        
        # Generar la matriz
        generate_matrix(self)
    
        # Botón IA
        imagen = Image.open(resource_path("Imagenes/facewin.png"))
        imagen = imagen.resize((30, 30), Image.LANCZOS)
        imagen = ImageTk.PhotoImage(imagen)
        
        ia_Button = tk.Button(bar_Frame, image=imagen, font=self.FUENTE,
                              bg=self.FONDO_BOTONES_MAIN,
                              activebackground=self.FONDO_BOTONES_MAIN,
                              highlightthickness=0, bd=0, relief="flat",
                              command=lambda: IA(self))
        ia_Button.image = imagen
        ia_Button.grid(row=0, column=4, padx=5)
        
        # Cargar diccionario de imágenes
        load_images(self)
    
        
if __name__ == "__main__":
    minesweeper = Minesweeper()
    minesweeper.main()
