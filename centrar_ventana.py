################################################################################
################ Función para centrar una ventana en la pantalla ###############
################################################################################


def centrar_ventana(ventana, width, height):
    """
    Parámetros:
    -----------
    ventana: tk.Root
        ventana que se desea centrar
    
    width: int
        Ancho de la ventana
    
    height: int
        Alto de la ventana
    -----------
    Primero, consigue las dimensiones de la pantalla y después sitúa la ventana 
    en al centro.
    """
    
    # Dimensiones de la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    
    # Calcular las coordenadas x e y para centrar la ventana
    position_x = int((screen_width - width) / 2)
    position_y = int((screen_height - height) / 2)
    
    # Establecer la posición de la ventana
    ventana.geometry(f"{width}x{height}+{position_x}+{position_y}")
