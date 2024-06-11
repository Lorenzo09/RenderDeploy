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

# Se cargan los archivos con los que se trabajará:
df_steam_games = pd.read_parquet('./Datasets/pdf_SteamGames.parquet')
df_user_reviews = pd.read_parquet('./Datasets/new_user_reviews.parquet')
df_user_items = pd.read_parquet('./Datasets/new_df_users_items.parquet')
# Definir la ruta al archivo parquet
PARQUET_FILE_PATH = ("./Datasets/df_segunda_consulta.parquet")

def developer(desarrollador: str):
    # Filtrar por desarrollador
    df_dev = df_steam_games[df_steam_games['developer'] == desarrollador]
    
    # Obtener la cantidad de ítems por año
    items_por_anio = df_dev.groupby('release_date').size()
    
    # Obtener el porcentaje de contenido Free por año
    contenido_free_por_anio = df_dev[df_dev['price'] == 0].groupby('release_date').size()
    
    # Calcular el porcentaje de contenido Free y reemplazar NaN con 0
    porcentaje_free_por_anio = (contenido_free_por_anio / items_por_anio * 100).fillna(0).round(2)
    
    # Crear un DataFrame con los resultados
    result_df = pd.DataFrame({
        'Año': items_por_anio.index,
        'Cantidad de Items': items_por_anio.values,
        'Contenido Free': porcentaje_free_por_anio.values
    })
    
    # Ordenar el DataFrame por año
    result_df.sort_values(by='Año', inplace=True)
    
    # Formatear los valores en la columna "Contenido Free"
    result_df['Contenido Free'] = result_df['Contenido Free'].astype(str) + '%'
    
    # Liberar memoria
    del df_dev
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
    
    # Liberar memoria utilizada por el DataFrame intermedio
    del user_data
    gc.collect()

    # Retornar un diccionario con los resultados
    return {
        "Usuario": User_id,
        "Dinero gastado": f"{money_spent} USD",
        "% de recomendación": f"{recommend_percentage:.2f}%",
        "Cantidad de items": items_count
    }
    
def recomendacion_juego(user_id: str):
    '''
    Devuelve una lista con 5 sugerencias de juegos para el usuario seleccionado.
    Ejemplo de retorno: {'Sugerencias para el usuario 76561197970982479': ['1. RWBY: Grimm Eclipse', '2. Rogue Legacy', '3. Dust: An Elysian Tail', "4. King Arthur's Gold", '5. RIFT']}
    '''
    # Verificar si el ID de usuario está en el DataFrame de reseñas de usuarios
    if user_id not in df_user_reviews['user_id'].values:
        return f"ERROR: El ID de usuario {user_id} no existe en la base de datos."
    
    # Extraer los juegos que el usuario ya ha jugado
    df_rev_games = pd.merge(df_user_reviews, df_steam_games, left_on="item_id", right_on="id", how="inner")
    juegos_jugados = df_rev_games[df_rev_games['user_id'] == user_id]

    # Eliminar los juegos jugados por el usuario del DataFrame de juegos
    df_user = df_steam_games[["id", "app_name"]].drop(juegos_jugados['id'].values, errors='ignore')

    # Liberar memoria de los DataFrames intermedios
    del df_rev_games, juegos_jugados
    gc.collect()

    # Ruta completa al archivo modelo_sentimiento.pkl
    ruta_modelo = './Datasets/modelo_sentimiento.pkl'

    # Cargar el modelo de Sistema de Recomendación entrenado desde el archivo especificado
    with open(ruta_modelo, 'rb') as file:
        modelo_sentimiento = pickle.load(file)

    # Realizar las predicciones y agregar en una nueva columna
    df_user['estimate_Score'] = df_user['id'].apply(lambda x: modelo_sentimiento.predict(user_id, x).est)

    # Ordenar el DataFrame de manera descendente en función al score y seleccionar los 5 principales
    sugerencias = df_user.sort_values('estimate_Score', ascending=False)["app_name"].head(5).to_list()

    # Liberar memoria del DataFrame intermedio
    del df_user
    gc.collect()

    # Crear la llave del diccionario de retorno
    llave_dic = f'Sugerencias para el usuario {user_id}'

    # Dar formato a las 5 sugerencias
    sugerencias_formateadas = [f'{i+1}. {sugerencia}' for i, sugerencia in enumerate(sugerencias)]

    # Devolver los resultados en un diccionario
    return {llave_dic: sugerencias_formateadas}