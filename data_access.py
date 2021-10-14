import sqlite3
from irudia import Irudia


class DataAccess:

    @staticmethod
    def convert_to_binary_data(filename):
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    @staticmethod
    def write_to_file(data, filename):
        with open(filename, 'wb') as file:
            file.write(data)

    def insert_image(self, image):
        self.c.execute("INSERT INTO irudiak VALUES (:data_ordua, :norabidea, :irudia)",
                       {'data_ordua': image.data_ordua, 'norabidea': image.norabidea, 'irudia': image.irudi})
        self.connection.commit()

    def __init__(self):
        self.connection = sqlite3.connect('irudiak.db')
        self.c = self.connection.cursor()

    def initialize(self):
        self.c.execute("""CREATE TABLE irudiak
                                data_ordua INTEGER PRIMARY KEY,
                                norabidea text NOT NULL,
                                argazkia blob NOT NULL
                                """)

        irudi_1 = Irudia(20201010101010, "+9000123456", self.convert_to_binary_data("irudiak/irudi_1.jpg"))
        irudi_2 = Irudia(20201212121212, "-9000123456", self.convert_to_binary_data("irudiak/irudi_2.jpg"))

        self.insert_image(irudi_1)
        self.insert_image(irudi_2)

    def close(self):
        self.connection.close()
