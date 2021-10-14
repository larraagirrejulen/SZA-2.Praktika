class Irudia:

    def __init__(self, data_ordua, norabidea, irudi):
        self.data_ordua = data_ordua
        self.norabidea = norabidea
        self.irudi = irudi

    def __repr__(self):
        return "Irudia('{}', '{}')".format(self.data_ordua, self.norabidea)
