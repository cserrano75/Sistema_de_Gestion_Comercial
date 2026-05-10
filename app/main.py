from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, proyectos, clientes, bitacora
from app import models, database
# Y recuerda descomentar la línea de la base de datos si la habías comentado:
models.Base.metadata.create_all(bind=database.engine)


app = FastAPI(title="CRM Industrial API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas (Endpoints)
app.include_router(auth_routes.router) # <--- Ahora la seguridad tiene su propio lugar
app.include_router(proyectos.router)
app.include_router(clientes.router)
app.include_router(bitacora.router)

@app.get("/", tags=["Home"])
def home():
    return {"mensaje": "CRM API Funcionando"}