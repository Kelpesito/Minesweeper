################################################################################
####################### Función para cargar las imágenes #######################
#######################    Usadas durante el programa    #######################
################################################################################


from PIL import Image, ImageTk


def load_images(minesweeper):
    """
    Parámetros:
    -----------
    minesweeper: Instancia buscaminas (Minesweeper)
    -----------
    Carga las imágenes de las casillas:
    Números, bombas, bandera, interrogante
    """
    
    # Interrogante
    imagen_int = Image.open("Imagenes/bombquestion.png")
    imagen_int = imagen_int.resize((24, 24), Image.LANCZOS)
    imagen_int = ImageTk.PhotoImage(imagen_int)
    
    # Bandera
    imagen_flag = Image.open("Imagenes/bombflagged.png")
    imagen_flag = imagen_flag.resize((24, 24), Image.LANCZOS)
    imagen_flag = ImageTk.PhotoImage(imagen_flag)
    
    # 1
    imagen_1 = Image.open("Imagenes/open1.png")
    imagen_1 = imagen_1.resize((24, 24), Image.LANCZOS)
    imagen_1 = ImageTk.PhotoImage(imagen_1)
    
    # 2
    imagen_2 = Image.open("Imagenes/open2.png")
    imagen_2 = imagen_2.resize((24, 24), Image.LANCZOS)
    imagen_2 = ImageTk.PhotoImage(imagen_2)
    
    # 3
    imagen_3 = Image.open("Imagenes/open3.png")
    imagen_3 = imagen_3.resize((24, 24), Image.LANCZOS)
    imagen_3 = ImageTk.PhotoImage(imagen_3)
    
    # 4
    imagen_4 = Image.open("Imagenes/open4.png")
    imagen_4 = imagen_4.resize((24, 24), Image.LANCZOS)
    imagen_4 = ImageTk.PhotoImage(imagen_4)
    
    # 5
    imagen_5 = Image.open("Imagenes/open5.png")
    imagen_5 = imagen_5.resize((24, 24), Image.LANCZOS)
    imagen_5 = ImageTk.PhotoImage(imagen_5)
    
    # 6
    imagen_6 = Image.open("Imagenes/open6.png")
    imagen_6 = imagen_6.resize((24, 24), Image.LANCZOS)
    imagen_6 = ImageTk.PhotoImage(imagen_6)
    
    # 7
    imagen_7 = Image.open("Imagenes/open7.png")
    imagen_7 = imagen_7.resize((24, 24), Image.LANCZOS)
    imagen_7 = ImageTk.PhotoImage(imagen_7)
    
    # 8
    imagen_8 = Image.open("Imagenes/open8.png")
    imagen_8 = imagen_8.resize((24, 24), Image.LANCZOS)
    imagen_8 = ImageTk.PhotoImage(imagen_8)
    
    # 0
    imagen_0 = Image.open("Imagenes/open0.png")
    imagen_0 = imagen_0.resize((24, 24), Image.LANCZOS)
    imagen_0 = ImageTk.PhotoImage(imagen_0)
    
    # Pérdida (muerte)
    imagen_death = Image.open("Imagenes/bombdeath.png")
    imagen_death = imagen_death.resize((24, 24), Image.LANCZOS)
    imagen_death = ImageTk.PhotoImage(imagen_death)
    
    # Bomba revelada
    imagen_bomb = Image.open("Imagenes/bombrevealed.png")
    imagen_bomb = imagen_bomb.resize((24, 24), Image.LANCZOS)
    imagen_bomb = ImageTk.PhotoImage(imagen_bomb)
    
    # Bomba fallada
    imagen_misflag = Image.open("Imagenes/bombmisflagged.png")
    imagen_misflag = imagen_misflag.resize((24, 24), Image.LANCZOS)
    imagen_misflag = ImageTk.PhotoImage(imagen_misflag)
    
    minesweeper.imagenes = {"interrogante": imagen_int,
                            "bandera": imagen_flag,
                            1: imagen_1, 2: imagen_2, 3: imagen_3, 4: imagen_4,
                            5: imagen_5, 6: imagen_6, 7: imagen_7, 8: imagen_8,
                            0: imagen_0, "bombdeath": imagen_death, 
                            "bombrevealed": imagen_bomb,
                            "bombmisflagged": imagen_misflag}
    