from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from starlette.staticfiles import StaticFiles
import os
import shutil
import subprocess
from app.rag_chain import final_chain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/rag/static", StaticFiles(directory="./pdf-documents"), name="static")
@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

pdf_directory = "./pdf-documents"

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    for file in files:
        try:
            file_path = os.path.join(pdf_directory, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    
    return {"message": "Files uploaded successfully", "filenames": [file.filename for file in files]}


"""
@app.post("/load-and-process-pdfs")
async def load_and_process_pdfs():
    try:
        subprocess.run(["python", "./rag-data-loader/rag_load_and_process.py"], check=True)
        return {"message": "PDFs loaded and processed successfully"}
    except subprocess.CalledProcessError as e:
        return {"error": "Failed to execute script"}
"""


# Añadimos un eejcutable de python para que se utilice el entorno virtual para ejecutar el script
from dotenv import load_dotenv
load_dotenv()

@app.post("/load-and-process-pdfs")
async def load_and_process_pdfs():
    print("Accediendo a load_and_process")
    try:
        print("Accedido!")
        # Ruta al ejecutable de Python del entorno de Poetry
        python_executable = os.getenv("PYTHON_EXECUTABLE")
        
        # Ruta al script
        script_path = "./rag-data-loader/rag_load_and_process.py"
        print(script_path)

        # Ejecutar el script utilizando el Python del entorno de Poetry
        result = subprocess.run([python_executable, script_path], check=True)
        
        print("Ejecutando el analisis de los PDFS")
        # Si todo va bien, devolvemos el mensaje
        return {"message": "PDFs loaded and processed successfully", "output": result.stdout}
    
    except subprocess.CalledProcessError as e:
        # En caso de error, capturamos el stderr y lo devolvemos
        return {"error": "Failed to execute script", "details": e.stderr}

# Edit this to add the chain you want to add
add_routes(app, final_chain, path="/rag")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
