from fastapi import FastAPI
from models import usuario, proveedor, equipo, asignacion, ticket

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "SGIT API Activa"}