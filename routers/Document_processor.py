from datetime import datetime
from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException,status
from app.Vectorizador import Vectorizador_func
from app.ChunkPdf import ProcesingPDF
from models.Documents import CreateDocument, GetDocument
from db import SessionDep
from sqlmodel import select
import os

routerPDFProcessing = APIRouter()

@routerPDFProcessing.post('/upload_pdf',tags=['Procesamiento de PDF'])
async def upload_pdf(session: SessionDep,
                     autors: str,
                     title: str,
                     year: str,
                     description: Optional[str] = None ,
                     file: UploadFile = File(...)
                     ):
    # Verificar si la carpeta "temp" existe
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # Guardar el archivo temporalmente
    try:
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        document_split, primer_trozo = ProcesingPDF(file_path)

        doc = CreateDocument(
            autors= autors,
            year = year,
            title = title,
            uploadDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            description = description
            )
        session.add(doc)
        session.commit()

        vectorStore = Vectorizador_func(document_split)

        return{
            'Message':'Archivo procesado y vectorizado con éxito',
            'Title': title,
            'Autors': autors,
            'firstChunk': primer_trozo
        }
    except Exception as e:
        raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
