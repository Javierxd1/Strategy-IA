# Strategy Answers API🎯

**Strategy Answers** es una API construida con **FastAPI**, **LangChain** y **Chroma** que permite:

- Subir documentos en **PDF** sobre **estrategia** y **gestión estratégica**.
- Procesarlos en **fragmentos** ("chunks") y vectorizarlos.
- Consultar sobre los documentos usando un sistema **RAG** (Retrieval Augmented Generation) que solo responde basado en el contenido cargado.
- Utilizar **GPT-4o** para generar respuestas profesionales y controladas.
---

## Tecnologías utilizadas

- **FastAPI** - Framework web para construir APIs.
- **LangChain** - Manejo de cadenas de procesamiento de lenguaje.
- **Chroma** - Base de datos vectorial para almacenar y recuperar fragmentos.
- **HuggingFace Embeddings** - Para convertir texto en vectores.
- **OpenAI GPT-4o** - Para generar respuestas a las preguntas.
- **SQLModel** - Para manejar la base de datos relacional.
- **dotenv** - Para gestionar variables de entorno de forma segura.

## Instalación y configuración

1. Clona el repositorio:

```bash
git clone https://github.com/user/Strategy-IA.git
cd Strategy-IA
```
```bash
python -m venv venv
source venv/bin/activate   # En Linux/macOS
venv\Scripts\activate      # En Windows
```

```bash
pip install -r requirements.txt
```

```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 1.Endpoints disponibles 🚀
```bash
POST /upload_pdf
```
Descripción: Procesa y vectoriza un documento PDF.

Parámetros form-data:

- autors: Nombre(s) del(los) autor(es).
- title: Título del documento.
- year: Año de publicación.
- description: (opcional) Descripción breve.
- file: Archivo PDF a cargar.

## 2. Preguntar al sistema
```bash
GET /ask?question=¿Qué es la misión empresarial?
```

**Descripción**: Consulta sobre los documentos procesados.

**Notas**:

- Solo responde si encuentra el contexto en los documentos.
Si no hay información, responde educadamente que no sabe.

## Licencia
Este proyecto es de uso educativo y puede ser adaptado para fines de investigación o aplicaciones internas.

Desarrollado con ❤️ usando FastAPI, LangChain y OpenAI.