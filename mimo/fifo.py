#!/usr/bin/python 
# -*- coding: utf-8 -*- 

import Queue
import time
import threading
import sys
import socket
import select
import serial
from xml.dom.minidom import parse, parseString

class SerialDataPump(object):
	ser = None
	t = None
	fifo = None
	running = 1
	def receiving(self, those):
		global last_received
		buffer = ''

		while self.ser and self.running == 1:
			last_received = self.ser.readline()
			if last_received:
				last_received = last_received.rstrip()
				self.fifo.put( last_received )

	def __init__(self, port, fifo):
		self.fifo = fifo
		try:
			self.ser = ser = serial.Serial(
				port=port,
				baudrate=9600,
				bytesize=serial.EIGHTBITS,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE,
				timeout=0.1,
				xonxoff=0,
				rtscts=0,
				interCharTimeout=None
			)
		except serial.serialutil.SerialException:
			#no serial connection
			self.ser = None
		else:
			self.t = threading.Thread(target=self.receiving, args=(self, ))
			self.t.start()



class FifoPump:
	running = 1
	i = 0
	t = None
	fifo = None
	
	def loop( self, those ):
		print("starting loop")
		while ( self.running == 1 ) :
			fifo.put( str( self.i ) )
			self.i += 1
			time.sleep( 1 )
		
	def __init__( self, fifo ):
		self.fifo = fifo
		self.fifo.put ("starting FifoPump")
		self.t = threading.Thread( target = self.loop, args=(self,) )
		self.t.start()


class TCPPump2:
	running = 1
	port = None
	fifo = None
	def loop(self, those):
		connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connexion_principale.bind(('', self.port))
		connexion_principale.listen(5)
		print("Le serveur écoute à présent sur le port {}".format( self.port ))

		clients_connectes = []
		while self.running == 1:
			# On va vérifier que de nouveaux clients ne demandent pas à se connecter
			# Pour cela, on écoute la connexion_principale en lecture
			# On attend maximum 50ms
			connexions_demandees, wlist, xlist = select.select([connexion_principale],[], [], 0.05)

			for connexion in connexions_demandees:
				connexion_avec_client, infos_connexion = connexion.accept()
				# On ajoute le socket connecté à la liste des clients
				clients_connectes.append(connexion_avec_client)

			# Maintenant, on écoute la liste des clients connectés
			# Les clients renvoyés par select sont ceux devant être lus (recv)
			# On attend là encore 50ms maximum
			# On enferme l'appel à select.select dans un bloc try
			# En effet, si la liste de clients connectés est vide, une exception
			# Peut être levée
			clients_a_lire = []
			try:
				clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
			except select.error:
					pass
			else:
				# On parcourt la liste des clients à lire
				for client in clients_a_lire:
					# Client est de type socket
					msg_recu = client.recv(1024)
					# Peut planter si le message contient des caractères spéciaux
					msg_recu = msg_recu.decode()
					print("Reçu {}".format(msg_recu))
					self.fifo.put( msg_recu )
					client.send(b"5 / 5")
					client.close()
					#if msg_recu == "fin":
					#	self.running = 0

		#print("Fermeture des connexions")
		#for client in clients_connectes:
		#	client.close()

		connexion_principale.close()

	def __init__(self, port, fifo):
		self.fifo = fifo
		self.port = port
		self.fifo.put ("starting TCPPump2")
		self.t = threading.Thread( target = self.loop, args=(self,) )
		self.t.start()	

class TCPPump:
	running = 1
	i = 0
	t = None
	port = None
	fifo = None
	
	def loop( self, those ):
		print("starting loop network")
		connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connexion_principale.bind(('', self.port))
		connexion_principale.listen(5)
		connexion_avec_client = None
		while ( self.running == 1 ) :
			try:
				# TODO : Voir pour rendre ça non bloquant pour pouvoir terminer le thread sans kill
				#        Solution à base de select ?
				connexion_avec_client, infos_connexion = connexion_principale.accept()
				connexion_avec_client.send("FIFO waiting!\n\r")
				msg_recu = connexion_avec_client.recv(1024)
				msg_recu = msg_recu.rstrip();
				fifo.put( msg_recu)
				connexion_avec_client.close()
			except:
				if connexion_avec_client :
					connexion_avec_client.close()
		connexion_principale.close()
			
	def __init__( self, port, fifo ):
		self.fifo = fifo
		self.port = port
		self.fifo.put ("starting FifoPumpTCP")
		self.t = threading.Thread( target = self.loop, args=(self,) )
		self.t.start()	
		
class FifoReader:
	running = 1
	t = None
	def read( self, those ):
		while ( self.running == 1 ) :
			try:
				#chaine = fifo.get(False, 5)
				chaine = fifo.get()
				print ( "FifoReader :" + chaine )
			except Queue.Empty:
				pass
		
	def __init__( self, fifo ):
		self.fifo = fifo
		self.fifo.put("starting FifoReader")
		self.t = threading.Thread(target = self.read, args=(self,) )
		self.t.start()

		
class TelecommandeRF :
	# Liste des télécommandes RF disponibles
	#  Pour chaque id de télécommande définir une liste des actions suivant les valeurs des boutons
	def __init__( self ):
		# lecture du fichier de config
		pass
	
	def convertir( self ):
		a = Action()


		
class ActionSocket :
	host = None
	port = None
	execute = None
	
	def __init__(self):
		pass
	
	def start(self):
		s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		#s.connect(("www.mcmillan-inc.com", 80))


class ActionLocal:
	execute = None
	def __init__(self, xmlFile):
		pass
	
	def start(self):
		pass

		
if __name__ == "__main__":
	fifo = Queue.Queue()

	#fp  = FifoPump( fifo )
	fr  = FifoReader( fifo )
	tcp = TCPPump( 9091, fifo )
	sdp = SerialDataPump( "/dev/ttyACM0", fifo)
	#tcp2 = TCPPump2( 9091, fifo)
	
	try :
		while True:
			time.sleep(1)
	except:
		sdp.running = 0
		tcp.running = 0
		#fp.running  = 0
		fr.running  = 0
		#tcp2.running = 0
		sys.exit()
	
