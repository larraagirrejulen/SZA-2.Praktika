import re
from data_access import DataAccess


print("START")
newLine = "aaaaaaaaaaa\r\n".encode()

print(newLine)
if newLine.decode().endswith("\r\n"):
    print("ajaaaaaaaaaaa\n\n")

pattern = re.compile("^[+-](9000|[0-8][0-9]{3})([01][0-9]|2[0-3])([0-5][0-9]){2}$")
if pattern.match("+1234235959"):
    print("funciona")
else:
    print("nope funciona")


db = DataAccess()
# db.initialize()
print(db.count_irudi_by_data_orduak(20201212121212, 20101212121212))
db.close()
