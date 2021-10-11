#!/usr/bin/env python3

from sys import argv
from socket import SOCK_STREAM, socket, AF_INET

PORT = 50000

if len(argv) != 2:
	print( "Erabilera: {} <zerbitzaria>".format(argv[0]))
	exit(1)

zerb_helb = (argv[1], PORT)

s = socket(AF_INET, SOCK_STREAM)
s.connect(zerb_helb)

print( "Sartu bidali nahi duzun mezua (hutsa bukatzeko):" )
while True:
	mezua = input()
	if not mezua:
		break
	s.sendall(mezua.encode())
	erantzuna = s.recv(1024).decode()
	while not erantzuna.endswith("\\r\\n"):
		erantzuna += s.recv(1024).decode()

	erantzuna = erantzuna[0:5]
	print("Jasotako erantzuna => " + erantzuna + ": ")
	print("Sartu bidali nahi duzun mezua (hutsa bukatzeko):")
s.close()