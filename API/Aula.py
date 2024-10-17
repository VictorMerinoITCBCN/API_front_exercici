from Connection import Connection

class Aula:

    #Pasa de llista a dict
    @staticmethod
    def formate_classrom(classrom):
        return {
            "desc_aula": classrom[0],
            "edifici": classrom[1],
            "pis": classrom[2]
        }

    #Selecciona la primera aula amb la id pasada per parametre i retorna si ha obtingut algun resultat  
    @staticmethod
    def exist(id):
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM Aula WHERE IdAula = %s"
            cursor.execute(query,(id,))

            classroms = cursor.fetchone()
            return True if classroms else False
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()

    #Retorna la id de un aula segons la descripció
    @staticmethod
    def get_id_by_desc(desc):
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            query = "SELECT IdAula FROM Aula WHERE DescAula = %s"
            cursor.execute(query,(desc,))

            id_aula = cursor.fetchone()
            if not id_aula: return -1

            return id_aula[0]
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()

    #Afegeix un aula a la base de dades
    @staticmethod
    def add(classrom):
        try:
            conn = Connection.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO Aula (DescAula,Edifici,Pis) VALUES (%s, %s, %s);"
            values = (classrom["desc_aula"], classrom["edifici"], classrom["pis"])

            cursor.execute(query, values)
            conn.commit()
            id_aula = cursor.lastrowid

            return {"status": 1, "message": f"Aula {classrom["desc_aula"]} afegida correctament", "id_aula": id_aula}
        except Exception as e:
            return {"status": -1, "message": f"Connection error: {e}"}
        finally:
            Connection.close()