import socket, os, signal

PORT = 50000

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
			buf = elkarrizketa.recv( 1024 )
			if not buf:
				break
			komandoa = buf[0:2:1]
			if(komandoa=="DIR"){

			}else if(komandoa=="TME"){

			}else if(komandoa=="IMG"){

			}else if(komandoa=="QTY"){
				
			}else{
				#errore 02 komando ezezaguna
			}
		print( "Konexioa ixteko eskaera jasota." )
		elkarrizketa.close()
		exit( 0 )
s.close()

