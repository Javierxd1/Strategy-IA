from fastapi import FastAPI
from db import create_all_tables

app = FastAPI(lifespan=create_all_tables)


@app.get('/')
async def root():
    return{'message':'Servidor levantado con éxito'}
    