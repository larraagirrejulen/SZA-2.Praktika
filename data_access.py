import sqlite3
from irudia import Irudia


class DataAccess:

    @staticmethod
    def convert_to_binary_data(filename):
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    def __init__(self):
        self.connection = sqlite3.connect('irudiak.db')
        self.c = self.connection.cursor()

    def initialize(self):
        self.c.execute("""CREATE TABLE irudiak(
                                data_ordua INTEGER PRIMARY KEY,
                                norabidea text NOT NULL,
                                argazkia blob NOT NULL
                                )""")

        irudi_1 = Irudia(20201010101010, "+9000123456", self.convert_to_binary_data("irudiak/irudi_1.jpg"))
        irudi_2 = Irudia(20201212121212, "+9000123456", self.convert_to_binary_data("irudiak/irudi_2.jpg"))
        irudi_3 = Irudia(20171212121212, "-9000123456", self.convert_to_binary_data("irudiak/irudi_3.jpg"))

        self.insert_image(irudi_1)
        self.insert_image(irudi_2)
        self.insert_image(irudi_3)

    def insert_image(self, image):
        self.c.execute("INSERT INTO irudiak VALUES (:data_ordua, :norabidea, :irudia)",
                       {'data_ordua': image.data_ordua, 'norabidea': image.norabidea, 'irudia': image.irudi})
        self.connection.commit()

    def get_data_ordua_by_norabide(self, norabide):
        self.c.execute("SELECT data_ordua FROM irudiak WHERE norabidea==:norabidea", {'norabidea': norabide})
        azkena = 0
        for do in self.c.fetchall():
            if do[0] > azkena:
                azkena = do[0]
        print(azkena)
        if azkena == 0:
            print("Ez dago argazkirik emandako norabidean!")
            return None
        return str(azkena)

    def get_norabide_by_data_ordua(self, data_ordua):
        self.c.execute("SELECT norabidea FROM irudiak WHERE data_ordua==:data_ordua", {'data_ordua': data_ordua})
        value = self.c.fetchone()
        if value is None:
            print("Ez dago argazkirik emandako data eta orduan!")
            return None
        return value[0]

    def get_irudi_by_data_ordua(self, data_ordua):
        self.c.execute("SELECT argazkia FROM irudiak WHERE data_ordua==:data_ordua", {'data_ordua': data_ordua})
        value = self.c.fetchone()
        if value is None:
            return None
        return value[0]

    def count_irudi_by_data_orduak(self, data_ordua1, data_ordua2):
        self.c.execute("SELECT argazkia FROM irudiak WHERE ((data_ordua>=:data_ordua1 AND data_ordua<=:data_ordua2) OR "
                       "(data_ordua>=:data_ordua2 AND data_ordua<=:data_ordua1))",
                       {'data_ordua1': data_ordua1, 'data_ordua2': data_ordua2})
        return len(self.c.fetchall())

    def get_irudi_by_data_orduak(self, data_ordua1, data_ordua2):
        self.c.execute("SELECT argazkia FROM irudiak WHERE (data_ordua>=:data_ordua1 AND data_ordua<=:data_ordua2) OR "
                       "(data_ordua>=:data_ordua2 AND data_ordua<=:data_ordua1)",
                       {'data_ordua1': data_ordua1, 'data_ordua2': data_ordua2})
        return self.c.fetchall()

    def close(self):
        self.connection.close()
