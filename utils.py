import pandas as pd
import gc
import pickle
from typing import Dict

def intro():
    '''
    Iniciamos una primera página en estilo HTML para la API.    
    Returns:
    str: Código HTML.
    '''
    return '''
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                }
                h1 {
                    color: #333;
                    text-align: center;
                    margin-bottom: 20px;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 10px;
                }
                span.highlight {
                    background-color: #3498db;
                    color: #fff;
                    padding: 5px;
                    border-radius: 3px;
                }
            </style>
        </head>
        <body>
            <h1>API en Render para el proyecto STEAM_MLOPS</h1>
            <p>Aquí, podrás realizar consultas sobre la plataforma STEAM. Como por ejemplo, obtener información de las desarrolladoras y recomendaciones de juegos según preferencias.</p>
            <p><span class="highlight">INSTRUCCIONES PARA ACCEDER:</span> Escribe <span class="highlight">/docs</span> al finalizar la URL para interactuar con la API (De la siguiente manera: https://steam-mlops-renderdeploy.onrender.com/docs).</p>
        </body>
    </html>
    '''

df_steam_games = pd.read_parquet('./Datasets/pdf_SteamGames.parquet')
# Definir la ruta al archivo parquet
PARQUET_FILE_PATH = ("./Datasets/df_segunda_consulta.parquet")
df_user_reviews = pd.read_parquet('./Datasets/new_user_reviews.parquet')

def developer(desarrollador: str):
    # Filtrar por desarrollador
    df_dev = df_steam_games[df_steam_games['developer'] == desarrollador]
    
    # Obtener la cantidad de ítems por año
    items_por_anio = df_dev.groupby('release_date').size()
    
    # Obtener el porcentaje de contenido Free por año
    contenido_free_por_anio = df_dev[df_dev['price'] == 0].groupby('release_date').size()
    porcentaje_free_por_anio = (contenido_free_por_anio / items_por_anio * 100).round(2)
    
    # Reemplazar valores NaN en "Contenido Free" con "0%"
    porcentaje_free_por_anio.fillna(0, inplace=True)
    
    # Crear un DataFrame con los resultados
    result_df = pd.DataFrame({'Año': items_por_anio.index,
                              'Cantidad de Items': items_por_anio.values,
                              'Contenido Free': porcentaje_free_por_anio.values})
    
    # Ordenar el DataFrame por año
    result_df = result_df.sort_values(by='Año').reset_index(drop=True)
    
    # Formatear los valores en la columna "Contenido Free"
    result_df['Contenido Free'] = result_df['Contenido Free'].astype(str) + '%'
    # Liberamos la memoria utilizada por el DataFrame intermedio
    gc.collect()
    return result_df

def userdata(User_id: str) -> Dict[str, str]:
    # Cargar el DataFrame desde el archivo parquet
    df_segunda_consulta = pd.read_parquet(PARQUET_FILE_PATH)
    
    # Filtrar el DataFrame para obtener las filas correspondientes al User_id dado
    user_data = df_segunda_consulta[df_segunda_consulta['user_id'] == User_id]
    
    # Calcular la cantidad total de dinero gastado por el usuario
    money_spent = user_data['price'].sum()
    
    # Calcular el porcentaje de recomendación en base a las revisiones
    recommend_percentage = (user_data['recommend'].mean()) * 100
    
    # Obtener la cantidad de items del usuario y convertir a cadena de texto
    items_count = str(user_data['items_count'].sum())
    
    # Liberamos la memoria utilizada por el DataFrame intermedio
    gc.collect()

    # Retornar un diccionario con los resultados
    return {
        "Usuario": User_id,
        "Dinero gastado": f"{money_spent} USD",
        "% de recomendación": f"{recommend_percentage}%",
        "Cantidad de items": items_count
    }

def recomendacion_juego(user_id: str):
    """
    Devuelve una lista con 5 sugerencias de juegos para el usuario seleccionado.
    Ejemplo de retorno: {'Sugerencias para el usuario 76561197970982479': ['1. RWBY: Grimm Eclipse', '2. Rogue Legacy', '3. Dust: An Elysian Tail', "4. King Arthur's Gold", '5. RIFT']}

    Args:
        user_id (str): El ID del usuario para el cual se desean obtener las recomendaciones de juegos.

    Returns:
        dict: Un diccionario con una clave que indica el usuario y un valor que es una lista con las 5 recomendaciones de juegos.
    """
    # Si el ID de usuario no se encuentra en los dataframes:
    if user_id not in df_user_reviews["user_id"].values:
        return f"ERROR: El ID de usuario {user_id} no existe en la base de datos."  # se imprime un mensaje de error
    else:
        # Se asigna el ID ingresado a la variable user
        user = user_id

        # En primer lugar, se extraen los juegos que el usuario ya ha jugado:
        df_rev_games = pd.merge(
            df_user_reviews,
            df_steam_games,
            left_on="reviews_item_id",
            right_on="id",
            how="inner",
        )
        juegos_jugados = df_rev_games[df_rev_games["user_id"] == user]

        # Se eliminan del dataframe de juegos los jugados por el usuario
        df_user = df_steam_games[["id", "app_name"]].drop(
            juegos_jugados.id, errors="ignore"
        )

        # Ruta completa al archivo RS_model.pkl
        ruta_modelo = "./0 Dataset/RS_model.pkl"

        # Se carga el modelo de Sistema de Recomendación entrenado desde el archivo especificado
        with open(ruta_modelo, "rb") as file:
            RS_model = pickle.load(file)

        # Se realizan las predicciones y se agregan en una nueva columna:
        df_user["estimate_Score"] = df_user["id"].apply(
            lambda x: RS_model.predict(user, x).est
        )

        # Se ordena el dataframe de manera descendente en función al score y se seleccionan los 5 principales:
        sugerencias = (
            df_user.sort_values("estimate_Score", ascending=False)["app_name"]
            .head(5)
            .to_list()
        )

        # Se crea la llave del diccionario de retorno
        llave_dic = f"Sugerencias para el usuario {user}"

        # Se da formato a las 5 sugerencias:
        sugerencias_formateadas = [
            f"{i+1}. {sugerencia}" for i, sugerencia in enumerate(sugerencias)
        ]
        # Se libera la memoria utilizada por los dataframes intermedios
        del df_rev_games, juegos_jugados, df_user
        gc.collect()

        # Se devuelven los resultados en un diccionario
        return {llave_dic: sugerencias_formateadas}
