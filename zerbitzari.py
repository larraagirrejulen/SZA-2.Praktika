import socket, os, signal, re

PORT = 50000

function dataEtaOrduaEgiaztatu(dataEtaOrdua):
	pattern = re.compile("^(19|20)[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[01])([01][0-9]|2[0-3])([0-5][0-9]){2}$")
	if pattern.match(dataEtaOrdua)
		return dataEtaOrdua
	else:
		return None

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

s.bind( ('', PORT) )
s.listen( 5 )

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

while True:
	elkarrizketa, bez_helb = s.accept()
	print( "Bezeroa konektatuta {}:{}.".format( bez_helb[0], bez_helb[1] ) )
	if os.fork():
		elkarrizketa.close()
	else:
		s.close()
		while True:
			buf = elkarrizketa.recv( 1024 ).decode()
			if not buf:
				break
			komandoa = buf[0:2:1]
			if komandoa=="DIR":
				erantzuna = ""
                norabidea = buf[3:end:1]
                if (norabidea[0] == '-' or norabidea[0] == '+') and (int(norabidea[1:end:1])>0 and int(norabidea[1:end:1])<9999):
                    #datu-basetik irudia hartzen du eta bere data eta ordua bultatzen du.
                    #errore 06 bueltatzen du emandako norabidearekin irudirik ez badago.
                    if True:
	                    dataEtaOrdua = " "
	                    erantzuna = "OK+" + dataEtaOrdua
                	else:
                		erantzuna = "ER-06"
                else:
                    erantzuna = "ER-05"
                elkarrizketa.sendall(erantzuna.encode())
			else if(komandoa=="TME"):
				erantzuna = ""
				if dataEtaOrduaEgiaztatu(buf[3:end:1]) is None:
					erantzuna = "ER-05"
				else:
					#DBan begiratu ez badago 07 errore kodea
					if True:
						norabidea = " "
						erantzuna = "OK+" + norabidea
					else:
						erantzuna = "ER-07"
				elkarrizketa.sendall(erantzuna.encode())
			else if(komandoa=="IMG"):

			else if(komandoa=="QTY"):
				
			else:
				elkarrizketa.sendall("ER-02".encode())
		
		print( "Konexioa ixteko eskaera jasota." )
		elkarrizketa.close()
		exit( 0 )
s.close()

