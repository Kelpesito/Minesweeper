################################################################################
################# Intervalos de confianza de las probabilidades ################
################################################################################


import scipy.stats as stats
import numpy as np

def get_intervalo_confianza(*args, confianza=0.95, label=""):
    """
    Parámetros:
    -----------
    args: list[num]
        Lista de los valores de observaciones
    
    confianza: float = 0.95
        Nivel de confianza para el intervalo
    
    label: str = ""
        Título de la muestra
    ------------
    Imprime en pantalla el intervalo de confianza de una muestra de 
    observaciones a un determinado nivel de confianza
    """
    
    # Calcular media muestral
    x_bar = np.mean(args)
    
    # Calcular desviación estándar
    s = np.std(args, ddof=1)
    
    # Valor crítico de t
    alpha = 1 - confianza
    n = len(args)
    df = n - 1
    t = abs(stats.t.ppf(alpha/2, df))
    
    # Error estándar de la media
    u = s/np.sqrt(n)
    
    # Margen de error
    U = t*u
    
    # Intervalo de confianza
    I = x_bar - U
    S = x_bar + U
    
    print(label)
    print(f"Intervalo de confianza: (I,S)|{confianza*100}%: ({I}, {S}), valor "
          f"medio: {x_bar}, error: {U}")
    print("\n")


if __name__ == "__main__":
    get_intervalo_confianza(52,46,45, label="rho_1. Victorias")
    get_intervalo_confianza(37,45,44, label="rho_1. EarlyGame")
    get_intervalo_confianza(3,2,2, label="rho_1. MidGame")
    get_intervalo_confianza(8,7,9, label="rho_1. LateGame")
    get_intervalo_confianza(63,55,56, label="rho_1. > EarlyGame")
    get_intervalo_confianza(82.5,83.6,80.4, label="rho_1. win | > EarlyGame")
    get_intervalo_confianza(60,53,54, label="rho_1. >= LateGame")
    get_intervalo_confianza(86.7,86.8,83.3, label="rho_1. win | >= LateGame")
    
    get_intervalo_confianza(14,13, label="rho_2. Victorias")
    get_intervalo_confianza(52,61, label="rho_2. EarlyGame")
    get_intervalo_confianza(14,12, label="rho_2. MidGame")
    get_intervalo_confianza(20,14, label="rho_2. LateGame")
    get_intervalo_confianza(48,39, label="rho_2. > EarlyGame")
    get_intervalo_confianza(29.2,33.3, label="rho_2. win | > EarlyGame")
    get_intervalo_confianza(34,27, label="rho_2. >= LateGame")
    get_intervalo_confianza(41.2,48.1, label="rho_2. win | >= LateGame")
        