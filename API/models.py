from pydantic import BaseModel
from datetime import datetime

#Model per els missatges de resposta de la APIs
class Msg(BaseModel):
    status: int
    message: str

#Model per retornar un alumne
class Student(BaseModel):
    id_alumne: int
    nom: str
    cicle: str
    curs: int
    grup: str
    desc_aula: str

#Model per la creació y modificació d'un alumne
class New_student(BaseModel):
    id_aula: int
    nom: str
    cicle: str
    curs: int
    grup: str

#Model per un alumne amb la informació de la seva respectiva aula
class Student_with_classrom_data(BaseModel):
    id_alumne: int
    id_aula: int
    nom: str
    cicle: str
    curs: int
    grup: str
    data_creacio: datetime
    data_modificacio: datetime
    aula_desc: str
    edifici: str
    pis: int