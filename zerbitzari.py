import os
import re
import signal
import socket

PORT = 50000
EOM = "\r\n"


def data_ordua_egiaztatu(dat_ord):
	pattern = re.compile("^(19|20)[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[01])([01][0-9]|2[0-3])([0-5][0-9]){2}$")
	if len(dat_ord) == 16 and pattern.match(dat_ord[0:14]):
		print("Data eta ordu egokiak.")
		return True
	else:
		print("Data eta orduak ez datoz bat protokoloarekin!!!")
		return False


def norabidea_egiaztatu(norab):
	if len(norab) == 13 and (norab[0] == '-' or norab[0] == '+') and (int(norab[1:]) > 0 and int(norab[1:]) < 9999):
		print("Norabide egokia.")
		return True
	else:
		print("Norabidea ez dator bat protokoloarekin!!!")
		return False


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', PORT))
s.listen(5)

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

while True:
	elkarrizketa, bez_helb = s.accept()
	print("Bezeroa konektatuta {}:{}.".format(bez_helb[0], bez_helb[1]))
	if os.fork():
		elkarrizketa.close()
	else:
		s.close()
		while True:
			buf = elkarrizketa.recv(1024).decode()
			if not buf:
				break
			while not buf.endswith(EOM):
				buf += elkarrizketa.recv(1024).decode()
			print("Jasotako mezua: " + buf)
			komandoa = buf[0:3]
			gainontzekoa = buf[3:]

			if komandoa == "DIR":
				if norabidea_egiaztatu(gainontzekoa) is False:
					print("Errore kodea bidaltzen...")
					erantzuna = "ER-05"
				elif True:		#DBan norabideari dagokion argazkiaren data eta ordua lortu.
					print("Data eta ordua bidaltzen...")
					data_ordua = " "
					erantzuna = "OK+" + data_ordua
				else:
					print("Ez da aurkitu argazkirik.\nErrore kodea bidaltzen...")
					erantzuna = "ER-06"
				elkarrizketa.sendall((erantzuna + EOM).encode())

			elif komandoa == "TME":
				if data_ordua_egiaztatu(gainontzekoa) is False:
					print("Errore kodea bidaltzen...")
					erantzuna = "ER-05"
				elif True:		#DBan data eta orduari dagokion argazkiaren norabidea lortu.
					print("Norabidea bidaltzen...")
					norabidea = " "
					erantzuna = "OK+" + norabidea
				else:
					print("Ez da aurkitu argazkirik.\nErrore kodea bidaltzen...")
					erantzuna = "ER-07"
				elkarrizketa.sendall((erantzuna + EOM).encode())

			#elif komandoa=="IMG":

			#elif komandoa=="QTY":

			else:
				elkarrizketa.sendall("ER-02".encode())

		print("Konexioa ixteko eskaera jasota.\n")
		elkarrizketa.close()
		exit(0)
