from Connection import Connection
from CSV_controller import CSV_controller
from Aula import Aula

class Alumnat:

    #Converteix una llista amb la informació d'un alumne a un diccionari
    @staticmethod
    def formate_student(student):
        return {
            "id_alumne":student[0],
            "id_aula": student[1],
            "nom":student[2],
            "cicle":student[3],
            "curs":student[4],
            "grup":student[5],
            "data_creacio":student[6],
            "data_modificacio":student[7],
            "desc_aula": student[8]
            }

    @staticmethod
    def formate_new_student(student):
        return {
            "id_aula":student[0],
            "nom":student[1],
            "cicle":student[2],
            "curs":student[3],
            "grup":student[4]
            }

    #Converteix una llista amb la informació d'un alumne i la seva aula a un diccionari
    @staticmethod
    def formate_student_with_classrom_data(student):
        return {
            "id_alumne":student[0],
            "id_aula":student[1],
            "nom":student[2],
            "cicle":student[3],
            "curs":student[4],
            "grup":student[5],
            "data_creacio":student[6],
            "data_modificacio":student[7],
            "aula_desc": student[8],
            "edifici": student[9],
            "pis": student[10]
        }

    #Selecciona tots els alumnes de la base de dades i retorna una llista de diccionaris amb els alumnes
    @staticmethod
    def get_all_students(orderby: str = "ASC", contain: str | None = None, skip: int = 0, limit: int | None = None):
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()

            # Construïm la consulta de forma dinàmica
            query = "SELECT Alumne.*, Aula.DescAula FROM Alumne JOIN Aula ON Alumne.IdAula = Aula.IdAula"
            query_values = []

            # Filtrar per "contain" si es proporciona
            if contain:
                query += " WHERE NomAlumne LIKE %s"
                query_values.append(f"%{contain}%")

            # Validar que l'ordenació sigui ASC o DESC
            if orderby.upper() not in ["ASC", "DESC"]:
                orderby = "ASC"  # Valor per defecte si és incorrecte

            # Ordenem els resultats
            query += f" ORDER BY NomAlumne {orderby}"


            # Aplicar "LIMIT" i "OFFSET" si es proporcionen
            if limit:
                query += " LIMIT %s OFFSET %s"
                query_values.extend([limit, skip])

            cursor.execute(query, query_values)

            students = cursor.fetchall()
            return [Alumnat.formate_student(student) for student in students]

        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        
        finally:
            Connection.close()

    #Selecciona tots els alumnes i fa un join amb la taula aula per després retornar una llista de diccionaris amb l'informació
    @staticmethod
    def get_all_students_with_classrom_data():
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            query = "SELECT Alumne.*, Aula.DescAula, Aula.Edifici, Aula.Pis FROM ALUMNE JOIN Aula ON Alumne.IdAula = Aula.IdAula"
            cursor.execute(query)

            students = cursor.fetchall()
            return [Alumnat.formate_student_with_classrom_data(student) for student in students]
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()

    #Selecciona el primer alumne amb la id pasada per parametre i passa el resultat de llista a diccionari
    @staticmethod
    def get_student(id):
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            query = "SELECT Alumne.*, Aula.DescAula FROM Alumne JOIN Aula ON Alumne.IdAula = Aula.IdAula WHERE IdAlumne = %s"
            cursor.execute(query,(id,))

            student = cursor.fetchone()
            if not student: return {"status": -1,"message": f"No existeix cap alumne amb la id '{id}'"}
            return Alumnat.formate_student(student)
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()

    #Selecciona el primer alumne que trobi amb la id pasada per parametre i retorna si ha obtingut algun resultat
    @staticmethod
    def student_exist(id):
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM Alumne WHERE IdAlumne = %s"
            cursor.execute(query,(id,))

            classroms = cursor.fetchone()
            return True if classroms else False
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()

    #Comproba si l'aula existeix i afegeix l'alumne a la base de dades
    @staticmethod
    def add_student(student):
        #Comproba si 'student' es un objecte o un dict
        if isinstance(student, dict):
            values = (student["id_aula"], student["nom"], student["cicle"], student["curs"], student["grup"])
            id_aula = student["id_aula"]
            student_name = student["nom"]
        else:
            values = (student.id_aula, student.nom, student.cicle, student.curs, student.grup)
            id_aula = student.id_aula
            student_name = student.nom

        #Comproba si existeix l'aula
        if not Aula.exist(id_aula):
            return {"status": -1, "message": f"No existeix l'aula amb la id '{id_aula}'"}
        
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO Alumne (IdAula, NomAlumne, Cicle, Curs, Grup) VALUES (%s, %s, %s, %s, %s)"
            #Inserta les l'alumne
            cursor.execute(query, values)
            conn.commit()
            student_id = cursor.lastrowid
            
            return {"status": 1,"message": f"Alumne {student_name} amb id: {student_id} afegit correctament"}
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()

    #Fa un insert amb una llista de alumnes
    @staticmethod
    def add_many_students(student_list):
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            #Query per fer un insert i en cas de que l'alumne ja existeixi, el reescriu 
            query = "INSERT INTO Alumne (IdAula, NomAlumne, Cicle, Curs, Grup) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE NomAlumne = VALUES(NomAlumne), Cicle = VALUES(Cicle), Curs = VALUES(Curs), Grup = VALUES(Grup)"

            values = list([(student["id_aula"], student["nom"], student["cicle"], student["curs"], student["grup"]) for student in student_list])
            cursor.executemany(query, values)
            conn.commit()

            num_of_students = cursor.rowcount

            return {"status": 1,"message": f"{num_of_students} alumnes afegits correctament"}
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()

    #Afegeix alumnes i aules desde un fitxer csv
    @staticmethod
    async def add_students_from_csv(file):
        csv_file = CSV_controller(file)
        #Llegeix el fitxer
        try: content = await csv_file.get_content()
        except Exception as e: return {"status": -1, "message": str(e)}

        #S'inicien la llista per les respostes del servidor i la llista per els alumnes per afegir 
        response = []
        student_list = []
        #Itera per totes les files
        for row in content:
            #Comproba si es una fila valida
            if not Alumnat.is_valid_row(row): 
                #Afegiex el missatge d'alumne no valid a la resposta
                response.append({"status": -1, "message": f"Alumne no valid: {row}"})
                continue

            #Obte la id de l'aula i si no existeix, la crea
            id_aula = Aula.get_id_by_desc(row[0])
            if id_aula == -1:
                classrom = Aula.formate_classrom(row[:3])
                aula_res = Aula.add(classrom)
                #Afegeix el missatge de 'Aula afegida' a la resposta
                response.append(aula_res)
                id_aula = aula_res["id_aula"]

            #afegeix la id de l'aula a la fila en la posisió 3, on es troba la informació del alumne
            row.insert(3,id_aula)
            student = Alumnat.formate_new_student(row[3:])
            #Afegeix l'alumne a la llista d'alumnes
            student_list.append(student)
        
        res_alumnes = Alumnat.add_many_students(student_list)
        response.append(res_alumnes)
        return response

    #Comproba si una fila del csv conté valors valids
    @staticmethod
    def is_valid_row(row):
        pis = row[2]
        curs = row[5]

        header = ['DescAula', 'Edifici', 'Pis', 'NomAlumne', 'Cicle', 'Curs', 'Grup']

        for i in range(len(row)):
            if row[i] == header[i]: return False

        return pis.isdigit() and curs.isdigit()

    #Comproba si l'alumne i l'aula existeixen i modifica l'alumne
    @staticmethod
    def update_student(id, student):
        if not Alumnat.student_exist(id):
            return {"status": -1, "message": f"No existeix l'alumne amb la id '{id}'"}

        if not Aula.exist(student.id_aula):
            return {"status": -1, "message": f"No existeix l'aula amb la id '{student.id_aula}'"}
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            query = "UPDATE Alumne SET IdAula = %s, NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s WHERE IdAlumne = %s"
            values = (
                student.id_aula,
                student.nom, 
                student.cicle, 
                student.curs, 
                student.grup, 
                id
            )
            cursor.execute(query, values)
            conn.commit()

            return {"status": 1, "message": f"Usuari {student.nom} actualitzat"}
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()

    #Comproba si existeix l'alumne i l'elimina
    @staticmethod
    def delete_student(id):
        if not Alumnat.student_exist(id):
            return {"status": -1, "message": f"No existeix l'alumne amb la id '{id}'"}
        
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM Alumne WHERE IdAlumne = %s"
            cursor.execute(query, (id,))
            conn.commit()

            return {"status": 1, "message": f"Usuari amb id '{id}' elminat correctament"}
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()