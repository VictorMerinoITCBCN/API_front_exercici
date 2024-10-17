import mysql.connector

class Connection:

    #Variable per guardar la conexió
    _connection = None

    #Metode estatic per assignar una conexió amb la base de dades amb la variable '_connection'
    @staticmethod
    def conect():
        try:
            database = "alumnat"
            user = "alumnat_api"
            password = "admin"
            host = "localhost"
            port = "3306"
            collation="utf8mb4_unicode_ci"
            charset="utf8mb4"

            Connection._connection = mysql.connector.connect(
                database = database,
                user = user,
                password = password,
                host = host,
                port = port,
                collation = collation,
                charset = charset
            )
        except Exception as e:
            print(f"Error connecting to the data base: {e}")

    #Metode estatic per retornar la conexió
    #En el cas de que no hi hagi una conexió, creida al metode 'conect'
    @staticmethod
    def get_connection():
        if Connection._connection is None: Connection.conect()

        return Connection._connection
    
    #Tanca la conexió i asgina None a la variable '_connection' si hi existeix
    @staticmethod
    def close():
        if Connection._connection is not None:
            Connection._connection.close()
            Connection._connection = None
        else: print("There is not a connection")