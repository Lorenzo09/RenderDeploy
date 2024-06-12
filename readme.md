Este es el repositorio para deployar la aplicación en Render.

# STEAM MLOPS_RENDER 

## 📄 Descripción del Proyecto:     

 Este proyecto busca crear un MVP en un lapso de 7 días que incluye una API desarrollada con FastAPI para consultar datos de la plataforma Steam.

### 🎯 Objetivos y roles:

1. **📂 Feature Engineering**
     - Desarrollo de funciones para los endpoints.
     - Preparación de datasets para las consultas de la API.
     - Análisis de sentimiento en las reseñas de los usuarios aplicado con NLP en el dataset.
   - **🌐 API**:
     - Con endpoints que proporcionan acceso a los resultados.
     - Despliegue automático desde GitHub.

### 🚀 Funcionalidades del Proyecto:

- **Página de Inicio**: Introducción en estilo HTML a la API.
- **Consulta por Desarrollador**: Proporciona información sobre la cantidad de juegos y el porcentaje de contenido gratuito por año para un desarrollador específico.
- **Consulta de Datos de Usuario**: Muestra la cantidad de dinero gastado por un usuario, el porcentaje de recomendación basado en las reviews y la cantidad de juegos.
- **Recomendación de Juegos**: Devuelve una lista de 5 juegos recomendados para un usuario específico basado en un modelo de sistema de recomendación.

### 📂 Estructura del Proyecto:
    project-root/
    │
    ├── Datasets/
    │ ├── pdf_SteamGames.parquet
    │ ├── new_user_reviews.parquet
    │ ├── df_segunda_consulta.parquet
    │ └── modelo_sentimiento.pkl
    │
    ├── utils.py
    ├── main.py
    └── README.md

### 🔧 Archivos Principales:

- **utils.py**: Contiene las funciones para el procesamiento de datos y generación de respuestas para los endpoints de la API.
- **main.py**: Configuración de los endpoints utilizando FastAPI.

### 📋 Descripción de los Endpoints:

1. **Home**: `GET /`
   - **Descripción**: Página de inicio en HTML.
   - **Respuesta**: HTML con instrucciones y presentación.

2. **Consulta por Desarrollador**: `GET /developer/{desarrollador}`
   - **Descripción**: Proporciona información sobre la cantidad de juegos y el porcentaje de contenido gratuito por año para un desarrollador específico.
   - **Parámetro**: `desarrollador` (str) - Nombre del desarrollador.
   - **Respuesta**: Lista de diccionarios con información por año.

3. **Consulta de Datos de Usuario**: `GET /userdata/{User_id}`
   - **Descripción**: Muestra la cantidad de dinero gastado por un usuario, el porcentaje de recomendación basado en las reviews y la cantidad de juegos.
   - **Parámetro**: `User_id` (str) - ID del usuario.
   - **Respuesta**: Diccionario con la información del usuario.

4. **Recomendación de Juegos**: `GET /recomendacion_juego/{user_id}`
   - **Descripción**: Devuelve una lista de 5 juegos recomendados para un usuario específico.
   - **Parámetro**: `user_id` (str) - ID del usuario.
   - **Respuesta**: Diccionario con las recomendaciones de juegos.

### 🚀 Despliegue:

Para acceder a la API, dirígete a la siguiente [URL](https://steam-mlops-renderdeploy.onrender.com) y agrega `/docs` al final del link para ver la documentación interactiva y probar los endpoints. También puedes copiar y pegar el link en tú buscador: https://steam-mlops-renderdeploy.onrender.com

### 🛠️ Instalación y Uso:

1. Clona el repositorio:
   ```bash
   git clone <URL-del-repositorio>

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

3. Ejecuta la aplicación:
    ```bash
    uvicorn main:app --reload

4. Accede a la documentación:
    http://127.0.0.1:8000/docs
    