import os
import re
import signal
import socket

PORT = 50000


def data_ordua_egiaztatu(dat_ord):
	pattern = re.compile("^(19|20)[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[01])([01][0-9]|2[0-3])([0-5][0-9]){2}$")
	if pattern.match(dat_ord):
		return dat_ord
	else:
		return None


def norabidea_egiaztatu(norab):
	return (norab[0] == '-' or norab[0] == '+') and (int(norab[1:])>0 and int(norab[1:])<9999)

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
			komandoa = buf[0:2:1]
			if komandoa=="DIR":
				erantzuna = ""
				norabidea = buf[3:]
				if norabidea_egiaztatu(norabidea):
					if True:	#DBan norabideari dagokion argazkiaren data eta ordua lortu.
						data_ordua = " "
						erantzuna = "OK+" + data_ordua
					else:	#Norabidean irudirik ez badago errorea.
						erantzuna = "ER-06"
				else:
					erantzuna = "ER-05"
				elkarrizketa.sendall(erantzuna.encode())
			elif komandoa=="TME":
				erantzuna = ""
				data_ordua = buf[3:end:1]
				if data_ordua_egiaztatu(data_ordua) is None:
					erantzuna = "ER-05"
				else:
					if True:	#DBan data eta orduari dagokion argazkiaren norabidea lortu.
						norabidea = " "
						erantzuna = "OK+" + norabidea
					else:	#Data eta orduan irudirik ez badago errorea.
						erantzuna = "ER-07"
				elkarrizketa.sendall(erantzuna.encode())
			#elif komandoa=="IMG":

			#elif komandoa=="QTY":

			else:
				elkarrizketa.sendall("ER-02".encode())

		print( "Konexioa ixteko eskaera jasota." )
		elkarrizketa.close()
		exit( 0 )

