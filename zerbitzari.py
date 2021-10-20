import os
import re
import signal
import socket
from data_access import DataAccess

PORT = 50000
EOM = "\r\n"
OK = "OK+"
ER = "ER-"

# Socketak sortu eta konfiguratu
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))
s.listen(5)
signal.signal(signal.SIGCHLD, signal.SIG_IGN)


# Pasatako data eta ordua parametroa/ak egokiak diren egiaztatu
def data_ordua_egiaztatu(dat_ord, komand):
	regex = re.compile("^(19|20)[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[01])([01][0-9]|2[0-3])([0-5][0-9]){2}$")
	if (len(dat_ord) == 14 and regex.match(dat_ord)) or (
		komand == "IMG" and len(dat_ord) == 28 and regex.match(dat_ord[0:14]) and regex.match(dat_ord[14:28])):
		print("Data eta ordu parametro egokia/ak: {}".format(dat_ord))
		return dat_ord
	else:
		print("Data eta ordu parametro desegokia/ak: {}".format(dat_ord))
		return None


# Pasatako norabide parametroa egokia den egiaztatu
def norabidea_egiaztatu(norab):
	regex = re.compile("^[+-](9000|[0-8][0-9]{3})([01][0-9]|2[0-3])([0-5][0-9]){2}$")
	if len(norab) == 11 and regex.match(norab):
		print("Norabide parametro egokia: {}".format(norab))
		return True
	else:
		print("Norabide parametro desegokia: {}".format(norab))
		return False


# Erantzun mezua sortzeko funtzioa
def erantzun_mezua_sortu(erantzun):
	regex = re.compile("^(0[0-9])|(1[0-1])$")
	if regex.match(erantzun):
		return ER + erantzun + EOM
	elif erantzun == "":
		return OK + EOM
	else:
		return OK + erantzun + EOM


# Datu base objetua sortu
db = DataAccess()

while True:
	# Elkarrizketa eskaera onartu
	elkarrizketa, bez_helb = s.accept()
	print("Bezeroa konektatuta {}:{}.".format(bez_helb[0], bez_helb[1]))

	# Prozesu gurasoa
	if os.fork():
		elkarrizketa.close()

	# Prozesu umea
	else:
		s.close()
		while True:

			# Bezeroaren mezua jaso
			buf = elkarrizketa.recv(1024).decode()
			if not buf:
				break
			while not buf.endswith(EOM):
				buf += elkarrizketa.recv(1024).decode()
			komandoa = buf[0:3]
			parametroa = buf[3:len(buf)-2]

			# Parametrorik ez bada jasotzen errorea kodea bidali
			if len(parametroa) == 0:
				erantzuna = "04"

			# DIR komandoaren tratamendua
			elif komandoa == "DIR":
				if norabidea_egiaztatu(parametroa) is False:
					erantzuna = "05"		# Formatu desegokia
				else:
					data_ordua = db.get_data_ordua_by_norabide(parametroa)
					if data_ordua is not None:
						erantzuna = data_ordua
					else:
						erantzuna = "06"		# Norabide horretan argazkirik ez dago

			# TME komandoaren tratamendua
			elif komandoa == "TME":
				if data_ordua_egiaztatu(parametroa, komandoa) is None:
					erantzuna = "05"		# Formatu desegokia
				else:
					norabidea = db.get_norabide_by_data_ordua(parametroa)
					if norabidea is not None:
						erantzuna = norabidea
					else:
						erantzuna = "07"		# Data eta ordu horretan argazkirik ez dago

			# IMG komandoaren tratamendua
			elif komandoa == "IMG":
				data_ordua = data_ordua_egiaztatu(parametroa, komandoa)
				if data_ordua is None:
					erantzuna = "05"		# Formatu desegokia

				# Irudi bakarreko eskaera
				elif len(data_ordua) == 14:
					irudia = db.get_irudi_by_data_ordua(data_ordua)
					if irudia is not None:
						tamaina = str(len(irudia))
						erantzuna = OK + tamaina + "#"
						elkarrizketa.sendall(erantzuna.encode())
						elkarrizketa.sendall(irudia)
						erantzuna = None		# Berriro bidalketarik ez egiteko
					else:
						erantzuna = "08"		# Data eta ordu horretan argazkirik ez dago

				# Irudi anitzeko eskaera
				else:
					zenbat = db.count_irudi_by_data_orduak(data_ordua[0:14], data_ordua[14:28])
					elkarrizketa.sendall((OK + str(zenbat) + EOM).encode())
					if zenbat > 0:
						buf = elkarrizketa.recv(1024).decode()
						if not buf:
							break
						while not buf.endswith(EOM):
							buf += elkarrizketa.recv(1024).decode()
						komandoa = buf[0:3]
						parametroa = int(buf[3:len(buf) - 2])
						if komandoa == "QTY":
							if parametroa > zenbat:
								erantzuna = "10"		# Eskaera handiegia
							else:
								irudiak = db.get_irudi_by_data_orduak(data_ordua[0:14], data_ordua[14:28])
								for i in irudiak:
									if parametroa == 0:
										erantzuna == ""
										break
									else:
										parametroa -= 1
										erantzuna = OK + str(len(i)) + "#"
										elkarrizketa.sendall(erantzuna.encode())
										elkarrizketa.sendall(i[0])
								erantzuna = None
						else:
							erantzuna = "01"		# Espero ez den komandoa
					else:
						erantzuna = None		# Argazki kopurua 0 denez bukatu

			# Espero ez den komandoa jasotzen badu errore kodea bidali
			elif komandoa == "QTY":
				erantzuna = "01"

			# Komando ezezaguna bada errore kodea bidali
			else:
				erantzuna = "02"

			if erantzuna is not None:
				elkarrizketa.sendall(erantzun_mezua_sortu(erantzuna).encode())

		print("Konexioa ixteko eskaera jasota.\n")
		elkarrizketa.close()
		exit(0)
