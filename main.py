import pandas as pd
import utils as u
from fastapi import FastAPI, Query
from typing import Dict
from typing import List
from fastapi.responses import HTMLResponse

df_steam_games = pd.read_parquet('./Datasets/pdf_SteamGames.parquet')

app = FastAPI()

@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["Home"])

def intro():
    '''
    Página de inicio.

    Returns:
    HTMLResponse: Respuesta HTML que muestra la presentación.
    '''
    return u.intro()

@app.get("/developer/{desarrollador}",response_model=List,
          description="""
            <font color="blue">
             INSTRUCCIONES<br>
             1. Haga clic en "Try it out".<br>
             2. Ingrese el X en el cuadro de abajo.<br>
             3. Desplácese hacia "Resposes" para ver Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.<br>
             4. Ejemplos de desarrolladores para consultar: Valve, Capcom </font> 
             """,
             tags=["Consultas Generales"])
def get_developer_info(desarrollador: str):
    result = u.developer(desarrollador)
    return result.to_dict(orient='records')

PARQUET_FILE_PATH = ("./Datasets/df_segunda_consulta.parquet")

@app.get("/userdata/{User_id}", response_model=List,  
            description="""
    <font color="blue">
        Consulta de base de datos en la API STEAM_MLOPS<br>
        Para obtener la información deseada, siga las siguientes instrucciones:<br>
        1. Haga clic en "Try it out".<br>
        2. Ingrese el ID del usuario que desee.<br>
        3. Dirígase hacia el apartado "Responses". Allí, podrá ver la cantidad de dinero gastado por el usuario seleccionado, el porcentaje de recomendación basado en las reviews y la cantidad de juegos.<br>
        4. Ejemplos de ID de usuario para consultar: evcentric, Riot-Punch
    </font>
""", 
tags=["Consultas Generales"])
def get_userdata(User_id: str) -> Dict[str, str]:
    # Llamada a la función userdata definida en utils.py
    user_data = u.userdata(User_id)
    return user_data

@app.get('/recomendacion_juego/{user_id}', 
         description="""
    <font color="blue">
        ¡Bienvenido a la sección de recomendaciones de juegos!<br>
        Siga estos pasos para obtener las recomendaciones personalizadas:<br>
        1. Haga clic en "Try it out".<br>
        2. Ingrese el ID de usuario en el cuadro de abajo.<br>
        3. Desplácese hacia "Responses" para ver las 5 recomendaciones de juegos más adecuadas para el usuario.<br>
        4. ¡Disfruta explorando nuevos juegos!<br>
        Ejemplos de ID de usuario para probar: us213ndjss09sdf, evcentric, 76561198099295859
    </font>
""")
def recomendacion_juego(user_id: str):
    """
    Devuelve una lista con 5 recomendaciones de juegos para el usuario ingresado.
    Ejemplo de retorno: {'Recomendaciones para el usuario 76561197970982479': ['1. RWBY: Grimm Eclipse', '2. Rogue Legacy', '3. Dust: An Elysian Tail', "4. King Arthur's Gold", '5. RIFT']}
    """
    # Llamar a la función recomendacion_juego del módulo funciones_api
    recomendaciones = u.recomendacion_juego(user_id)
    return recomendaciones