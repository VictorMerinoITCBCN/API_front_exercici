from fastapi import FastAPI, UploadFile
from Alumnat import Alumnat
from typing import List, Union
from models import Msg, Student, New_student, Student_with_classrom_data

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Define the allowed origins
origins = [
    "http://127.0.0.1:3000",  # The frontend URL you're trying to access from
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],   # Allow all headers (Authorization, Content-Type, etc.)
)

#Retorna una llista amb tots els alumnes
@app.get("/alumne/list", response_model=Union[List[Student],Msg])
def get_students(orderby: str = "ASC",  contain: str | None = None, skip: int = 0, limit: int | None = None ):
    return Alumnat.get_all_students(orderby=orderby, contain=contain, skip=skip, limit=limit)

#Retorna l'alumne corresponent a la id pasada per parametre en el endpoint
@app.get("/alumne/show/{id}", response_model=Union[Student, Msg])
def get_student(id: int):
    return Alumnat.get_student(id)

#Retorna una llista amb tots els alumnes amb la informació de la seva clase
@app.get("/alumne/listAll", response_model=List[Student_with_classrom_data])
def get_student_and_classrom():
    return Alumnat.get_all_students_with_classrom_data()

#Afegeix una llista de alumnes desde un csv i retorna una llista de missatges indicant com a anat la consulta
@app.post("/alumne/loadAlumnes", response_model=Union[List[Msg], Msg])
async def add_students_from_csv(file: Union[UploadFile, None, str] = None):
    return await Alumnat.add_students_from_csv(file)

#Afegeix un alumne a la base de dades i retorna un missatge amb el resultat de la petició
@app.post("/alumnat/add", response_model=Msg)
async def add_student(student: New_student):
    return Alumnat.add_student(student)

#Modifica un alumne de la base de dades i retorna un missatge amb el resultat de la petició
@app.put("/alumne/update/{id}", response_model=Msg)
async def update_student(id: int,student: New_student):
    return Alumnat.update_student(id, student)

#Elimina un usuari de la base de dades i retorna un missatge amb el resultat de la petició
@app.delete("/alumne/delete/{id}", response_model=Msg)
async def delete_student(id: int):
    return Alumnat.delete_student(id)