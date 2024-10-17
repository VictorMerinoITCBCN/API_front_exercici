import csv
from io import StringIO

class CSV_controller:
    def __init__(self, file):
           self.file = file

    #Llegeix i elimina el contigut duplicat per despres retornarlo
    async def get_content(self):
        await self.read_file()
        return self.content
    
    #Llegeix i elimina el contingut duplicat
    async def read_file(self):
        if not self.file or self.file == "": raise Exception("No has pujat cap fitxer")

        if not self.file.content_type == "text/csv": raise Exception("Fitxer incorrecte")

        content = await self.file.read()
        content_text = content.decode('utf-8')

        csv_file = list(csv.reader(StringIO(content_text)))

        self.content = self.remove_duplicates(csv_file)
    
    #Elimina el contingut duplicat
    def remove_duplicates(self,lst):
        uniques = []
        for element in lst:
            if element in uniques: continue
            uniques.append(element)
        return uniques
    
