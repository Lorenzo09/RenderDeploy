import pandas as pd
from fastapi import FastAPI
from utils import developer
from utils import userdata
from typing import Dict
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from typing import List
from fastapi import FastAPI, Query

df_steam_games = pd.read_parquet('./Datasets/pdf_SteamGames.parquet')

app = FastAPI()

@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["Home"])

@app.get("/developer/{desarrollador}",response_model=List, description=""" <font color="blue"> INSTRUCCIONES<br> 1. Haga clic en "Try it out".<br> 2. Ingrese el X en el cuadro de abajo.<br> 3. Desplácese hacia "Resposes" para ver Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.<br> 4\_ Ejemplos de desarrolladores para consultar: Valve, Capcom </font> """, tags=["Consultas Generales"])
def get_developer_info(desarrollador: str):
    result = developer(desarrollador)
    return result.to_dict(orient='records')

PARQUET_FILE_PATH = ("./Datasets/df_segunda_consulta.parquet")

@app.get("/userdata/{User_id}")
def get_userdata(User_id: str) -> Dict[str, str]:
    # Llamada a la función userdata definida en utils.py
    user_data = userdata(User_id)
    return user_data