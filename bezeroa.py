#!/usr/bin/env python3

import socket, sys, os
import szasar
from datetime import datetime

SERVER = 'U030065.gi'
PORT = 50000
ER_MSG = (
	"Dena ondo. Errorerik ez.",
	"Espero ez den komandoa.",
	"Komando ezezaguna.",
	"Espero ez zen parametroa.",
	"Hautazkoa ez den parametro bat ez da jaso.",
	"Parametroak ez du formatu egokia.", 
	"Ez da argazkirik atera norabide horretan.",
	"Ez dago argazkirik data eta ordu horretan.",
	"Ez dago argazkirik data eta ordu horretan.",
	"Ez da lortu argazkia atzitzea.",
	"Adierazitako kopurua handiegia da.",
	"Irudiren bat ezin izan da atzitu.")

class Menua:
	Direction, Time, Image, SeveralImages, Exit = range( 1, 6 )
	Options = ( "Norabide jakin bateko azken argazkiaren data eta ordua lortu", "Data eta ordu jakin bateko azken argazkiaren norabidea lortu", "Irudia eskatu", "Hainbat irudi eskatu", "Irten" )

	def menua():
		print( "+{}+".format( '-' * 66 ) )
		for i,option in enumerate( Menua.Options, 1 ):
			print( "| {}.- {:<61}|".format( i, option ) )
		print( "+{}+".format( '-' * 66 ) )

		while True:
			try:
				selected = int( input( "Egin zure aukera: " ) )
			except:
				print( "Aukera okerra, saiatu berriro." )
				continue
			if 0 < selected <= len( Menua.Options ):
				return selected
			else:
				print( "Aukera okerra, saiatu berriro." )

def iserror( message ):
	if( message.startswith( "ER-" ) ):
		code = int( message[3:] )
		print( ER_MSG[code] )
		return True
	else:
		return False

def int2bytes( n ):
	if n < 1 << 10:
		return str(n) + " B  "
	elif n < 1 << 20:
		return str(round( n / (1 << 10) ) ) + " KiB"
	elif n < 1 << 30:
		return str(round( n / (1 << 20) ) ) + " MiB"
	else:
		return str(round( n / (1 << 30) ) ) + " GiB"

def norabideaLortu():
	while True:
		DeklinazioaStr = input( "Sartu norabidearen deklinazioa (-90 <= x <= 90):  " )
		try:
			Deklinazioa = float(DeklinazioaStr)
		except:
			print( "Aukera okerra, saiatu berriro. " )
			continue
		if -90 <= Deklinazioa <= 90:
			break
		else:
			print( "Aukera okerra, saiatu berriro. " )
	#Erabiltzaileak pasa duen zenbakiari ez badio zeinu positiboa jarri, guk egiten dugu.
	if Deklinazioa > 0 and not DeklinazioaStr[0] == '+':
		DeklinazioaStr = "+" + DeklinazioaStr
	#Zenbakia idatzi haurretik zerokoak idatzi baditu, kendu egin behar dira.
	i=1
	while DeklinazioaStr[i]=='0':
		i+=1
	#(0, i) tartean zerokoak daude.
	DeklinazioaStr = DeklinazioaStr[0]+DeklinazioaStr[i:len(DeklinazioaStr)]
	#Zenbakia digitu batekoa bada, zeroko bat jarri behar zaio zeinuaren eta zenbakiaren artean.	
	if -9 <= Deklinazioa <=9:
		DeklinazioaStr = DeklinazioaStr[0]+"0"+DeklinazioaStr[1:len(DeklinazioaStr)]
	#Daukagun DeklinazioaStr-ren luzera 3 bada, hau da, komarik ez badu, koma jartzen zaio.
	if len(DeklinazioaStr) == 3:
		DeklinazioaStr = DeklinazioaStr + "."
	#Daukagun DeklinazioaStr-ren luzera 5 baino txikiagoa edo berdina bada, zerokoak gehitu behar zaizkio bukaeran bi digitu hamartar izateko.
	if len(DeklinazioaStr) <= 5:
		DeklinazioaStr = DeklinazioaStr + ("0" * (6 - len(DeklinazioaStr)))
	#Hau dena egin ostean, -xx.yy edo +xx.yy egiturako string bat dugu. Beraz, koma kentzen diogu. 
	#Erabiltzaileak bi hamartar baino gehiago eman baditu, lehen biak bakarrik hartuko dira.
	DeklinazioaStr = DeklinazioaStr[0:3] + DeklinazioaStr[4:6]
	while True:
		IgoeraZuzena = input( "Sartu angeluaren igoera zuzena (oo/mm/ss):  " )
		try:
			datetime.strptime(IgoeraZuzena, '%H/%M/%S')
			break
		except:
			print( "Aukera okerra, saiatu berriro. ")
	return DeklinazioaStr + IgoeraZuzena[0:2] + IgoeraZuzena[3:5] + IgoeraZuzena[6:8]

def dataEtaOrduaLortu():
	while True:
		Data = input( "Sartu data (xxxx/xx/xx) : " )
		try:
			datetime.strptime(Data, '%Y/%m/%d')
			break
		except:
			print( "Aukera okerra, saiatu berriro. " )
	while True:
		Ordua = input( "Sartu ordua (oo:mm:ss) : ")
		try:
			datetime.strptime(Ordua, '%H:%M:%S')
			break
		except:
			print( "Aukera okerra, saiatu berriro. " )
	return Data[0:4] + Data[5:7] + Data[8:10] + Ordua[0:2] + Ordua[3:5] + Ordua[6:8]

def argazkiKopuruaLortu():
	while True:
		EskatutakoKopurua = input( "Zenbat argazki eskatu nahi dituzu?  " )
		try:
			Kopurua = int(EskatutakoKopurua)
		except:
			print( "Aukera okerra, saiatu berriro. " )
		if Kopurua < 0:
			print( "Aukera okerra, saiatu berriro. " )
		else:
			break
	return Kopurua


if __name__ == "__main__":
	if len( sys.argv ) > 3:
		print( "Erabilera: {} [<zerbitzaria> [<portua>]]".format( sys.argv[0] ) )
		exit( 2 )

	if len( sys.argv ) >= 2:
		SERVER = sys.argv[1]
	if len( sys.argv ) == 3:
		PORT = int( sys.argv[2])

	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	s.connect( (SERVER, PORT) )


	while True:
		option = Menua.menua()

		if option == Menua.Direction:
			Norabidea = norabideaLortu()
			Mezua = "{}{}\r\n".format( szasar.Command.Direction, Norabidea )
			s.sendall(Mezua.encode("ascii" ))
			Mezua = szasar.recvline( s ).decode("ascii")
			if iserror( Mezua ):
				continue
			print(Mezua)
			dataEtaOrdua = Mezua[3:]
			OK+20201212121212
			print("Data: "+dataEtaOrdua[0:4]+"/"+dataEtaOrdua[4:6]+"/"+dataEtaOrdua[6:8]+" Ordua: "+dataEtaOrdua[8:10]+dataEtaOrdua[10:12]+dataEtaOrdua[12:13])
		elif option == Menua.Time:
			DataOrdua = dataEtaOrduaLortu()
			Mezua = "{}{}\r\n".format( szasar.Command.Time, DataOrdua)
			s.sendall( Mezua.encode("ascii"))
			Mezua = szasar.recvline(s).decode("ascii")
			print(Mezua)
			if iserror( Mezua ):
                                continue
			Norabidea = Mezua[3:]
			print("Deklinazioa: "+Norabidea[0:3]+"."+Norabidea[3:5]+"º Igoera zuzena: "+Norabidea[5:7]+"º"+Norabidea[7:9]+"'"+Norabidea[9:11]+"''")
		elif option == Menua.Image:
			DataOrdua = dataEtaOrduaLortu()
			Mezua = "{}{}\r\n".format(szasar.Command.Image, DataOrdua)
			s.sendall(Mezua.encode("ascii"))
			Mezua = szasar.recvImageSize(s).decode("ascii")
			if iserror( Mezua ):
				continue
			print(Mezua)
			ArgazkiarenTamaina = int(Mezua[3:len(Mezua)-1])
			Filedata = szasar.recvall( s, ArgazkiarenTamaina )
			ArgIzena = "Argazkia"+DataOrdua[0:4]+DataOrdua[4:6]+DataOrdua[6:8]
			try:
				with open( ArgIzena, "wb" ) as f:
					f.write( Filedata )
				except:
					print( "Ezin da argazkia disko lokalean gorde." )
				else:
					print( "'{}' argazkia zuzen jaso da.".format( filename ) )
		elif option == Menua.SeveralImages:
			print("HASIERAKO DATA ETA ORDUA:")
			DataOrdua1 = dataEtaOrduaLortu()
			print("AMAIERAKO DATA ETA ORDUA:")
			DataOrdua2 = dataEtaOrduaLortu()
			Mezua = "{}{}\r\n".format(szasar.Command.Image, DataOrdua1 + DataOrdua2)
			s.sendall( Mezua.encode( "ascii" ) )
			Mezua = szasar.recvline( s ).decode ("ascii" )
			if iserror( Mezua ):
				continue
			ArgazkiKop = int( mezua[3:] )
			if ArgazkiKop == 0:
				print("Ez dago argazkirik adieraziriko denbora tartean")
				continue
			print(str(ArgazkiKop)+" argazki daude adieraziriko denbora tartean")
			EskatutakoKopurua = lortuEskatutakoKopurua()
			Mezua = "{}{}\n\r".format(szasar.Command.Quantity, EskatutakoKopurua)
			s.sendall(Mezua.encode("ascii"))
			i=1 
			Mezua = szasar.recvImageSize(s).decode("ascii")
			if iserror( Mezua ):
				continue
			if EskatutakoKopurua == 0:
				continue
			ArgazkiarenTamaina = int(Mezua[3:len(Mezua)-1])
			while i <= EskatutakoKopurua:
				Filedata = szasar.recvall( s, ArgazkiarenTamaina )
				ArgIzena = "Argazkia{}".format(i)
				try:
					with open( ArgIzena, "wb" ) as f:
						f.write( Filedata )
				except:
					print( "Ezin da {}. argazkia disko lokalean gorde.".format(i) )
				else:
					print( "{}. argazkia zuzen jaso da.".format(i) )
				if i != EskatutakoKopurua:
					Mezua = szasar.recvImageSize(s).decode("ascii")
					ArgazkiarenTamaina = int(Mezua[0:len(Mezua)-1])
				i+=1
		elif option == Menua.Exit:
			print("Agur!")
			break

	s.close()


