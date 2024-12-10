from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import database
from api.routers.routers_users import routerlogin
from api.routers.routers_turnos import routerturnos
from api.routers.routers_tareas import routertareas
from api.routers.routers_tareas_asignadas import routertareas_asignadas
from api.routers.routers_datos_users import routerdatosuser

app = FastAPI()

# # Configuración de CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Permitir todos los orígenes
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(routerlogin)
app.include_router(routerturnos)
app.include_router(routertareas)
app.include_router(routertareas_asignadas)
app.include_router(routerdatosuser)
database.init_db()
