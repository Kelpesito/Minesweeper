################################################################################
################# Funciones para interpolar las probabilidades #################
################################################################################


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


def transformada(x, a=0, b=100/3):
    return np.log((x-a)/(b-x))


def plot_transformada(a=0, b=100/3):
    """
    Parámetros:
    -----------
    a: float
        Límite inferior del intervalo
    
    b: float
        Límite superior del intervalo
    -----------
    Grafica la función transformada(x,a,b)
    """
    
    eps = 1e-6
    x = np.linspace(a+eps, b-eps, 500)
    y = transformada(x)
    
    # Plot
    plt.figure(figsize=(7,6))
    plt.plot(x,y, label=r"$t = \ln\left(\dfrac{\rho}{33.3-\rho}\right)$", 
             color="red")
    
    plt.axvline(x=a, linestyle="--", color="blue")
    plt.axvline(x=b, linestyle="--", color="blue")
    
    plt.title("Gráfico de la transformación", fontsize=18, fontweight="bold")
    plt.xlabel(r"Densidad de minas, $\rho$ (%)", fontsize=12)
    plt.ylabel("t", fontsize=12)
    
    plt.grid()
    plt.legend()
    plt.tight_layout()
    
    plt.savefig("Graficos/Transformacion.png", dpi=1080)
    
    plt.show()


def transformada_inversa(x, a=0, b=100/3):
    return (b*np.exp(x) + a)/(np.exp(x) + 1)


def interpolacion(y1, y2, a, b, x1=15.6, x2=20.6):
    """
    Parámetros:
    -----------
    x1, y1: float, float = 15.6, y1
        Punto 1
    
    x2, y2: float, float = 20.6, y2
        Punto 2
    
    a: float
        Asíntota horizontal inferior
    
    b: float
        Asíntota horizontal superior
    ----------
    Devuelve:
    ---------
    func = lambda t: a + (b - a)/(1 + np.exp(-k*(t - to)))
        Función logística
    ----------
    Realiza una interpolación tipo logística:
        y = a + (b-a)/(1+e^(-k*(x-xo)))
    Antes de eso, transforma el espacio [0, 33.3] a (-inf, inf)
    """
    
    t1 = transformada(x1)
    t2 = transformada(x2)
    
    # Interpolacion
    alpha = np.log((y1-a)/(b-y1))
    beta = np.log((y2-a)/(b-y2))
    
    to = float((beta*t1 - alpha*t2)/(beta - alpha))
    k = float(alpha/(t1-to))
    rho_0 = float(transformada_inversa(to))
    print(f"{to=}, {k=}, {rho_0=}")
    
    return lambda t: a + (b - a)/(1 + np.exp(-k*(t - to)))


def interpolacion_2(y1, y2, x1=15.6, x2=20.6):
    """
    Parámetros:
    -----------
    x1, y1: float, float = 15.6, y1
        Punto 1
    
    x2, y2: float, float = 20.6, y2
        Punto 2
    -----------
    Devuelve:
    ---------
    func = lambda x: f(x, k_opt, x0_opt, G_opt)
    ---------
    Realiza una interpolación tipo derivada de la función logística con 
    ganancia:
        G*k*e^(k*(x-x0)) / (e^(k*(x-x0)) + 1)^2
    Antes de eso, transforma el espacio [0, 33.3] a (-inf, inf)
    
    Como el problema puede ser difícil de resolver analíticamente, se utiliza 
    la función minimize de scipy para minimizar el error.
    """
    
    def f(x, k, x0, G):
        return G*k*np.exp(k*(x-x0))/(np.exp(k*(x-x0)) + 1)**2
    
    def objective(params, x1, y1, x2, y2):
        """
        Parámetros:
        -----------
        params: tuple[float, float, float]
            Tupla con los parámetros de la función: k, x0, G
            
        x1, y1: float, float = 15.6, y1
        Punto 1
    
        x2, y2: float, float = 20.6, y2
            Punto 2
        -----------
        Devuelve:
        ---------
        float = np.sqrt(error1**2 + error2**2)
            Error cuadrático del sistema de ecuaciones para la interpolación
        ---------
        Calcula los errores de las funciones como la diferencia del valor 
        estimado y el real, y después calcula el error cuadrático.
        """
        
        k, x0, G = params
        error1 = f(x1, k, x0, G) - y1
        error2 = f(x2, k, x0, G) - y2
        return np.sqrt(error1**2 + error2**2)
    
    t1 = transformada(x1)
    t2 = transformada(x2)
    
    initial_params = [1, 0, 10]
    result = minimize(objective, initial_params, args=(t1, y1, t2, y2))
    
    k_opt, x0_opt, G_opt = [float(_) for _ in result.x]
    rho_0 = float(transformada_inversa(x0_opt))
    print(f"{k_opt=}, {x0_opt=}, {G_opt=}, {rho_0=}")
    
    return lambda x: f(x, k_opt, x0_opt, G_opt)


def plot_interpolacion(y1, y2, func_interpolacion, monotonia=False, AHI=0, 
                       AHS=100, x1=15.6, x2=20.6, color=None, label=None):
    """
    Parámetros:
    -----------
    x1, y1: float, float = 15.6, y1
        Punto 1
    
    x2, y2: float
        Punto 2
    
    func_interpolacion: func
        Función de interpolación
    
    monotonia: bool | None= False
        True si la función es monótona creciente, False si es monótona 
        decreciante, None si no es monótona
    
    AHI: float
        Asíntota horizontal inferior
    
    AHS: float
        Asíntota horizontal superior
    
    color: str | None
        Color del gráfico
    
    label: str | None
        Nombre del gráfico
    -----------
    Hace el plot de la función de interpolación (antes se ha deshecho la 
    transformada ((-inf, inf) -> [0, 33.3]). También se marca los puntos 
    conocidos.
    """
    
    t = np.linspace(-30, 30, 500)
    y = func_interpolacion(t)
    x = transformada_inversa(t)

    plt.plot(x, y, color=color, label=label)
    
    puntos_x = [0, x1, x2, 100/3]
    puntos_y = [AHI, y1, y2, AHS] if monotonia else [AHS, y1, y2, AHI]
    puntos_y = [0, y1, y2, 0] if monotonia is None else puntos_y
    
    plt.scatter(puntos_x, puntos_y, color=color, zorder=5)   


if __name__ == "__main__":
    plot_transformada()
    
    plt.figure(figsize=(7,6))
    func_win = interpolacion(48, 14, 0, 100)
    plot_interpolacion(48, 14, func_win, color="green", label="$P(W)$")
    
    func_Early = interpolacion(42, 57, 0, 83)
    plot_interpolacion(42, 57, func_Early, monotonia=True, AHS=83,
                       color="lightcoral", label="$P(E)$")
    
    func_Mid = interpolacion(2, 13, 0, 17)
    plot_interpolacion(2, 13, func_Mid, monotonia=True, AHS=17,
                       color="orange", label="$P(M)$")
    
    func_Late = interpolacion_2(8, 17)
    plot_interpolacion(8, 17, func_Late, monotonia=None, color="yellow", 
                       label="$P(L)$")
    
    func_greater_Early = interpolacion(58, 44, 17, 100)
    plot_interpolacion(58, 44, func_greater_Early, AHI=17, 
                       color="darkslategray", label="$P(X > E)$")
    
    func_win_greater_Early = interpolacion(82, 31, 0, 100)
    plot_interpolacion(82, 31, func_win_greater_Early, color="royalblue", 
                       label="$P(W | X > E)$")
    
    func_greater_Late = interpolacion(56, 31, 0, 100)
    plot_interpolacion(56, 31, func_greater_Late, color="mediumorchid", 
                       label=r"$P(X \geq E)$")
    
    func_win_greater_Late = interpolacion(85, 45, 0, 100)
    plot_interpolacion(85, 45, func_win_greater_Late, color="crimson", 
                       label=r"$P(W | X \geq E)$")
    
    # Acabar de hacer plot
    plt.legend()
    
    plt.title("Probabilidad de cada suceso", fontsize=18, fontweight="bold")
    plt.xlabel(r"Densidad de minas, $\rho$ (%)", fontsize=12)
    plt.ylabel("Probabilidad (%)", fontsize=12)
    
    plt.grid()
    plt.tight_layout()
    
    plt.savefig("Graficos/Probabilidad.png", dpi=1080)
    
    plt.show()
