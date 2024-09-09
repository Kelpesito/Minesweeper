################################################################################
########################## Testear IA del Buscaminas  ##########################
########################## Extracción de estadísticos ##########################
################################################################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

score_list = []  # Lista de puntuación (1: victoria; 0: derrota)
when_list = []  # Lista tipo de final de partida ("win", "EarlyGame", 
# "MidGame", "LateGame")
tiempo_list = []  # Lista de tiempos  

def test_minesweeper_IA(score, when, tiempo):
    """
    Parámetros:
    -----------
    score: int (0, 1). 
        Puntuación de una partida
    
    when: str ("win", "EarlyGame", "MidGame", "LateGame").
        Tipo de fin de partida
    
    tiempo: float.
        Tiempo de partida
    ------------
    Cuando se acaba una partida con IA, se guardan score, when y tiempo en sus 
    respectivas listas (globe_list, when_list, tiempo_list).
    
    Después se guarda en un excel.
    
    Finalmente, si se han hecho x partidas, se sale del programa.
    """
    
    global score_list, when_list, tiempo_list
    
    score_list += [score]
    when_list += [when]
    tiempo_list += [tiempo]
    
    print(len(score_list))
    
    nombres_filas = ["score", "when", "time"]
    df = pd.DataFrame([score_list, when_list, tiempo_list], 
                      index=nombres_filas)
    
    # Guardar excel (nombre variable)
    df.to_excel("Excels/Principiante.xlsx", header=False)
    
    # Si se han hecho x (número variable) partidas, se sale
    if len(score_list) == 100:
        quit()
    

def get_df():
    """
    Devuelve:
    ---------
    lista_dataframes: list[pd.dataframe]
        Lista de los dataframes extraídos de cada excel
    ---------
    A partir de los excels, se extraen los dataframes y se guardan en una lista
    """
    
    nombres_excels = ["Excels/Principiante.xlsx", "Excels/Intermedio.xlsx", 
                      "Excels/Experto.xlsx",
                      "Excels/Personalizada_samerate_1.xlsx", 
                      "Excels/Personalizada_samerate_2.xlsx",
                      "Excels/Personalizada_maxminas.xlsx"]
    
    lista_dataframes = []
    for excel in nombres_excels:
        df = pd.read_excel(excel, header=None)
        # Configurar la primera columna como encabezados
        df.columns = df.iloc[0, :]
        # Eliminar la primera columna que ahora son los encabezados
        df = df.iloc[:, 1:]
        # Nombrar los encabezados y numerar columnas
        df.index = ["score", "when", "time"]
        df.columns = range(1,101)
        df = df.T  # Transpuesta
        lista_dataframes += [df]
    
    return lista_dataframes


def get_df_arrays(lista_dataframes):
    """
    Parámetro:
    ----------
    lista_dataframes: list[pd.dataframe]
        Lista de los dataframes extraídos de cada excel
    ----------
    Devuelve:
    ---------
    dict_dataframes: dict[str, dict[str, np.array]]
        Diccionario donde cada clave son las dificultades y los valores son 
        diccionarios donde las claves son strings (los títulos de las columnas) 
        y los valores son arrays de numpy (representan un dataframe)
    ----------
    Para cada dataframe de lista_dataframe, se convierte en un diccionario y se 
    añade a un diccionario bajo la clave de su dificultad.
    """
    
    nombres_dificultades = ["Principiante", "Intermedio", "Experto",
                            "Personalizada_1", "Personalizada_2",
                            "Personalizada_3"]
    
    dict_dataframes = {}
    for i, dificultad in enumerate(nombres_dificultades):
        dict_of_lists = lista_dataframes[i].to_dict(orient="list")
        dict_of_arrays = {columna: np.array(valores) for columna, valores in 
                          dict_of_lists.items()}
        dict_dataframes[dificultad] = dict_of_arrays
    
    return dict_dataframes


def get_evolution_win_rate(dict_dataframes):
    """
    Parámetro:
    ----------
    dict_dataframes: dict[str, dict[str, np.array]]
        Diccionario donde cada clave son las dificultades y los valores son 
        diccionarios donde las claves son strings (los títulos de las columnas) 
        y los valores son arrays de numpy (representan un dataframe)
    ----------
    Devuelve:
    ---------
    dict_dataframes: dict[str, dict[str, np.array]]
        Diccionario donde cada clave son las dificultades y los valores son 
        diccionarios donde las claves son strings (los títulos de las columnas) 
        y los valores son arrays de numpy (representan un dataframe)
        Es el mismo diccionario pero con una columna más: evolución del win rate
    ---------
    Para cada diccionario de cada dificultad, se calcula la evolución del win 
    rate: cantidad ganada hasta entonces / número de partidas entonces. 
    
    Se añade a dict_dataframes
    """
    
    for dificultad in dict_dataframes:
        score = dict_dataframes[dificultad]["score"]
        cum_win_rate = np.cumsum(score)/np.arange(1, len(score) + 1)
        cum_win_rate = np.round(cum_win_rate*100)
        dict_dataframes[dificultad]["cum_win_rate"] = cum_win_rate
    
    return dict_dataframes

# Colores que representan cada dificultad
COLORES_DIFICULTAD = {"Principiante": "#B7F377", "Intermedio": "#FAF36C",
                      "Experto": "#FA6C6C", "Personalizada_1": "#B8FFF1",
                      "Personalizada_2": "#8C84FF", 
                      "Personalizada_3": "#EE82EE"}


def plot_evolution_win_rate(dict_dataframes):
    """
    Parámetro:
    ----------
    dict_dataframes: dict[str, dict[str, np.array]]
        Diccionario donde cada clave son las dificultades y los valores son 
        diccionarios donde las claves son strings (los títulos de las columnas) 
        y los valores son arrays de numpy (representan un dataframe)
    ----------
    Hace un plot de la evolución del win rate para cada dificultad en una misma 
    figura y ejes.
    """
    
    plt.figure(figsize=(7, 6))
    win_rates = {}  # Diccionario de win rates
    for dificultad in dict_dataframes:
        plt.plot(dict_dataframes[dificultad]["cum_win_rate"],
                 color=COLORES_DIFICULTAD[dificultad], label=dificultad)
        
        win_rate = dict_dataframes[dificultad]["cum_win_rate"][-1]
        win_rates[dificultad] = win_rate
        plt.axhline(y=win_rate, color="gray", linestyle='--')
        
    plt.text(92, 53, f"{win_rates["Principiante"]}%", color="gray", fontsize=12)
    plt.text(92, 47, f"{win_rates["Intermedio"]}%", color="gray", fontsize=12)
    plt.text(92, 15, f"{win_rates["Experto"]}%", color="gray", fontsize=12)
    plt.text(92, 41, f"{win_rates["Personalizada_1"]}%", color="gray", 
             fontsize=12)
    plt.text(92, 9, f"{win_rates["Personalizada_2"]}%", color="gray", 
             fontsize=12)
    plt.text(92, 1, f"{win_rates["Personalizada_3"]}%", color="gray", 
             fontsize=12)
    
    # Añadir título y etiquetas
    plt.title("Evolución del win-rate", fontsize=18, fontweight='bold')
    plt.xlabel("Partida", fontsize=12)
    plt.ylabel("Win-rate (%)", fontsize=12)
    
    plt.legend()
    
    plt.grid()
    plt.tight_layout()
    
    plt.savefig('Graficos/win_rate_evolution.png', dpi=1080)
    
    plt.show()
    

# Colores que representan los diferentes finales de partida
COLORES_END_GAME = {"win": "green",
                    "EarlyGame": "lightcoral",
                    "MidGame": "orange",
                    "LateGame": "yellow"}

# Tupla de las diferentes dificultades
DIFICULTADES = ("Principiante", "Intermedio", "Experto","Personalizada_1", 
                "Personalizada_2", "Personalizada_3")


def plot_balance_end_game(dict_dataframes):
    """
    Parámetro:
    ----------
    dict_dataframes: dict[str, dict[str, np.array]]
        Diccionario donde cada clave son las dificultades y los valores son 
        diccionarios donde las claves son strings (los títulos de las columnas) 
        y los valores son arrays de numpy (representan un dataframe)
    ----------
    Devuelve:
    ---------
    end_games: dict[str, list[int]]
        Diccionario donde cada clave es un tipo de fin de partida y los valores 
        son listas que contienen cuántas veces se repite en cada dificultad 
        siguiendo el orden: "Principiante", "Intermedio", "Experto",
        "Personalizada_1", "Personalizada_2", "Personalizada_3"
    ---------
    Para cada dificultad clasifica y cuenta los finales de partida. Finalmente 
    se hace un gráfico de barras con estos datos
    """
    
    end_games = {"win": [], "EarlyGame": [], "MidGame": [], "LateGame": []}
    for dificultad in dict_dataframes:
        # Contar cuántos hay de cada tipo
        wins = np.count_nonzero(dict_dataframes[dificultad]["when"] == 
                                "win")
        EarlyGames = np.count_nonzero(dict_dataframes[dificultad]["when"] 
                                      == "EarlyGame")
        MidGames = np.count_nonzero(dict_dataframes[dificultad]["when"] == 
                                    "MidGame")
        LateGames = np.count_nonzero(dict_dataframes[dificultad]["when"] == 
                                     "LateGame")
        
        # Añadir a cada lista
        end_games["win"] += [wins]
        end_games["EarlyGame"] += [EarlyGames]
        end_games["MidGame"] += [MidGames]
        end_games["LateGame"] += [LateGames]
    
    # Plot
    plt.figure(figsize=(7,6))
    width = 0.6
    bottom = np.zeros(6)
    # Gráfico de barras
    for end_game, counts in end_games.items():
        p = plt.bar(DIFICULTADES, counts, width=width, label=end_game, 
                    bottom=bottom, color=COLORES_END_GAME[end_game])
        
        labels = [f"{count}%" if count != 0 else "" for count in counts]
        plt.bar_label(p, labels=labels, label_type='center')
        
        bottom += counts
    
    # Añadir título y etiquetas
    plt.title("Balance de los finales de partida", fontsize=18, 
              fontweight='bold')
    plt.xlabel("Dificultad", fontsize=12)
    plt.ylabel("%", fontsize=12)
    
    plt.xticks(rotation=10)
    
    plt.legend()
    
    plt.tight_layout()
    
    plt.savefig('Graficos/balance_end_game.png', dpi=1080)
    
    plt.show()
    
    return end_games
        
    
def plot_salen_de_Early(end_games):
    """
    Parámetro:
    ----------
    end_games: dict[str, list[int]]
        Diccionario donde cada clave es un tipo de fin de partida y los valores 
        son listas que contienen cuántas veces se repite en cada dificultad 
        siguiendo el orden: "Principiante", "Intermedio", "Experto",
        "Personalizada_1", "Personalizada_2", "Personalizada_3"
    ----------
    Devuelve:
    ---------
    salen_de_Early: dict[str, int]
        Diccionario donde cada clave es una dificultad y los valores son el 
        número de partidas que salen del early game
    ---------
    Primero se crea el diccionario donde se cuenta cuantas partidas salen del 
    early game y finalmente se hace un gráfico de barras con el resultado.
    """
    
    salen_de_Early = {dificultad: 100-end_games["EarlyGame"][i] for i, 
                      dificultad in enumerate(DIFICULTADES)}
    
    # Plot
    plt.figure(figsize=(8,6))
    
    b = plt.bar(DIFICULTADES, counts:=list(salen_de_Early.values()), 
                color=list(COLORES_DIFICULTAD.values()))
    labels = [f"{cuenta}%" for cuenta in counts]
    plt.bar_label(b, labels=labels, label_type='center')
    
    # Añadir título y etiquetas
    plt.title("Cantidad de partidas que pasan de early-game", fontsize=18, 
              fontweight='bold')
    plt.xlabel("Dificultad", fontsize=12)
    plt.ylabel("%", fontsize=12)
    
    plt.xticks(rotation=10)
    
    plt.tight_layout()
    
    plt.savefig('Graficos/num_pasan_early.png', dpi=1080)
    
    plt.show()
    
    return salen_de_Early
        

def plot_ganan_sin_contar_Early(end_games, salen_de_Early):
    """
    Parámetros:
    -----------
    end_games: dict[str, list[int]]
        Diccionario donde cada clave es un tipo de fin de partida y los valores 
        son listas que contienen cuántas veces se repite en cada dificultad 
        siguiendo el orden: "Principiante", "Intermedio", "Experto",
        "Personalizada_1", "Personalizada_2", "Personalizada_3"
        
    salen_de_Early: dict[str, int]
        Diccionario donde cada clave es una dificultad y los valores son el 
        número de partidas que salen del early game
    -----------
    Calcula para cada dificultad la probabilidad de ganar si se sale de early 
    game: victorias / partidas que salen de early game, y finalmente hace un 
    gráfico de barras del resultado
    """
    
    ganan_sin_contar_Early = {dificultad:
        round(end_games["win"][i] / salen_de_Early[dificultad] * 100, 1) for i, 
        dificultad in enumerate(DIFICULTADES)}
    
    # Plot
    plt.figure(figsize=(8,6))
    
    b = plt.bar(DIFICULTADES, counts:=list(ganan_sin_contar_Early.values()), 
                color=list(COLORES_DIFICULTAD.values()))
    labels = [f"{cuenta}%" if cuenta > 0 else "" for cuenta in counts]
    plt.bar_label(b, labels=labels, label_type='center')
    
    # Añadir título y etiquetas
    plt.title("Win-rate de las partidas que salen de early-game", fontsize=18, 
              fontweight='bold')
    plt.xlabel("Dificultad", fontsize=12)
    plt.ylabel("%", fontsize=12)
    
    plt.xticks(rotation=10)
    
    plt.tight_layout()
    
    plt.savefig('Graficos/win_rate_pasan_early.png', dpi=1080)
    
    plt.show()


def plot_llegan_a_Late(end_games):
    """
    Parámetro:
    ----------
    end_games: dict[str, list[int]]
        Diccionario donde cada clave es un tipo de fin de partida y los valores 
        son listas que contienen cuántas veces se repite en cada dificultad 
        siguiendo el orden: "Principiante", "Intermedio", "Experto",
        "Personalizada_1", "Personalizada_2", "Personalizada_3"
    ----------
    Devuelve:
    ---------
    llegan_a_Late: dict[str, int]
        Diccionario donde cada clave es una dificultad y los valores son el 
        número de partidas que llegan a late game
    ---------
    Primero se crea el diccionario donde se cuenta cuantas partidas llegan a 
    late game y finalmente se hace un gráfico de barras con el resultado.
    """
    
    llegan_a_Late = {dificultad: end_games["LateGame"][i] + end_games["win"][i] 
                     for i, dificultad in enumerate(DIFICULTADES)}
    
    # Plot
    plt.figure(figsize=(7,6))
    
    b = plt.bar(DIFICULTADES, counts:=list(llegan_a_Late.values()), 
                color=list(COLORES_DIFICULTAD.values()))
    labels = [f"{cuenta}%" if cuenta > 0 else "" for cuenta in counts]
    plt.bar_label(b, labels=labels, label_type='center')
    
    # Añadir título y etiquetas
    plt.title("Cantidad de partidas que llegan a late-game", fontsize=18, 
              fontweight='bold')
    plt.xlabel("Dificultad", fontsize=12)
    plt.ylabel("%", fontsize=12)
    
    plt.xticks(rotation=10)
    
    plt.tight_layout()
    
    plt.savefig('Graficos/num_llegan_late.png', dpi=1080)
    
    plt.show()
    
    return llegan_a_Late


def plot_ganan_llegan_a_Late(end_games, llegan_a_Late):
    """
    Parámetros:
    -----------
    end_games: dict[str, list[int]]
        Diccionario donde cada clave es un tipo de fin de partida y los valores 
        son listas que contienen cuántas veces se repite en cada dificultad 
        siguiendo el orden: "Principiante", "Intermedio", "Experto",
        "Personalizada_1", "Personalizada_2", "Personalizada_3"
    
    llegan_a_Late: dict[str, int]
        Diccionario donde cada clave es una dificultad y los valores son el 
        número de partidas que llegan a late game
    -----------
    Calcula para cada dificultad la probabilidad de ganar si se llega a late 
    game: victorias / partidas que llegan a late game, y finalmente hace un 
    gráfico de barras del resultado.
    """
    
    ganan_sin_contar_Early = {dificultad:
        round(end_games["win"][i] / llegan_a_Late[dificultad] * 100 if 
              llegan_a_Late[dificultad] != 0 else 0, 1) for i,
        dificultad in enumerate(DIFICULTADES)}
    
    plt.figure(figsize=(8,6))
    
    b = plt.bar(DIFICULTADES, counts:=list(ganan_sin_contar_Early.values()), 
                color=list(COLORES_DIFICULTAD.values()))
    labels = [f"{cuenta}%" if cuenta > 0 else "" for cuenta in counts]
    plt.bar_label(b, labels=labels, label_type='center')
    
    # Añadir título y etiquetas
    plt.title("Win-rate de las partidas que llegan a late-game", fontsize=18, 
              fontweight='bold')
    plt.xlabel("Dificultad", fontsize=12)
    plt.ylabel("%", fontsize=12)
    
    plt.xticks(rotation=10)
    
    plt.tight_layout()
    
    plt.savefig('Graficos/win_rate_llegan_late.png', dpi=1080)
    
    plt.show()


def plot_tiempo_de_test(dict_dataframes):
    """
    Parámetro:
    ----------
    dict_dataframes: dict[str, dict[str, np.array]]
        Diccionario donde cada clave son las dificultades y los valores son 
        diccionarios donde las claves son strings (los títulos de las columnas) 
        y los valores son arrays de numpy (representan un dataframe)
    ----------
    Muestra en un gráfico el tiempo que toma cada partida. Se muestran en la 
    misma figura, pero en diferentes ejes. También se añade información del 
    tiempo medio, la desviación estándar, el mínimo y el máximo
    """
    
    fig, axs = plt.subplots(3, 2, figsize=(8,8))
    for i, dificultad in enumerate(dict_dataframes):
        row = i // 2  # Fila correspondiente en la cuadrícula
        col = i % 2   # Columna correspondiente en la cuadrícula
        
        axs[row,col].plot(time:=dict_dataframes[dificultad]["time"],
                          color=COLORES_DIFICULTAD[dificultad])
        axs[row,col].set_title(f"{dificultad}. Tiempo total: {round(sum(time)/
                               3600, 1)} h", fontsize=14)
        
        # Tiempo medio, desviación estándar, mínimo y máximo de la dificultad
        tiempo_medio = round(np.mean(time), 1)
        desv = round(np.std(time, ddof=1), 1)
        tiempo_min = round(min(time), 1)
        tiempo_max = round(max(time), 1)
        
        axs[row,col].axhline(y=tiempo_medio, color="black", linestyle="--")
        axs[row,col].text(0, tiempo_medio*1.1, f"Tiempo_medio: {tiempo_medio} s"
                          f";\nDesviación estándar: {desv} s;\nRango de tiempo"
                          f": [{tiempo_min}, {tiempo_max}]", color="black", 
                          fontsize=12)
        
        axs[row,col].grid()
    
    # Añadir título y etiquetas
    plt.suptitle("Tiempo de cada partida", fontsize=18, fontweight='bold')
    fig.text(0.5, 0.001, 'Partida', ha='center', fontsize=12)
    fig.text(0.001, 0.5, 'Tiempo (s)', va='center', 
             rotation='vertical', fontsize=11)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    plt.savefig('Graficos/time.png', dpi=1080)
    
    plt.show()
    
    
if __name__ == "__main__":
    lista_dataframes = get_df()  # Lista de dataframes
    dict_dataframes = get_df_arrays(lista_dataframes)  # Diccionario de 
    # diccionarios (llaves: listas)
    dict_dataframes = get_evolution_win_rate(dict_dataframes)  # Diccionario de 
    # diccionarios (llaves: arrays)
    plot_evolution_win_rate(dict_dataframes)  # Plot evolución win rate
    end_games = plot_balance_end_game(dict_dataframes)  # Plot balance fin
    # partida
    salen_de_Early = plot_salen_de_Early(end_games)  # Plot partidas que salen 
    # del early game
    plot_ganan_sin_contar_Early(end_games, salen_de_Early)  # Plot partidas que 
    # ganan si salen del early game
    llegan_a_Late = plot_llegan_a_Late(end_games)  # Plot partidas que llegan a 
    # late game
    plot_ganan_llegan_a_Late(end_games, llegan_a_Late)  # Plot partidas que 
    # ganan si llegan a late game
    plot_tiempo_de_test(dict_dataframes)  # Plot tiempo de partida
    