from fastapi import FastAPI
from db import create_all_tables
from routers.Document_processor import routerPDFProcessing
from db import SessionDep

app = FastAPI(lifespan=create_all_tables)


@app.get('/')
async def root():
    return{'message':'Servidor levantado con éxito'}

app.include_router(routerPDFProcessing)