#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys

tableau = { "AVIDSEN" : 
				{ "echantillonnage" : 44100,
				  "bits" : 
					{ 0 : [ [ 52, 0 ], [ 22, 1 ] ] ,
					  1 : [ [ 22, 0 ], [ 52, 1 ] ] },
				  "buttons" : 
					{ "1 ON"  : "011111111111100101101",
					  "1 OFF" : "011111111111100111100",
					  "2 ON"  : "011111111111110101111",
					  "2 OFF" : "011111111111110111110",
					  "3 ON"  : "011111111111111101110",
					  "3 OFF" : "011111111111111111111",
					  "4 ON"  : "011111111111100001111",
					  "4 OFF" : "011111111111100011110",
					  
					}
				}
			}

def sendDataPulse( dataPin, duration, value ):
	if value == 1 :
		GPIO.output(dataPin, GPIO.HIGH)
	else:
		GPIO.output(dataPin, GPIO.LOW)
	time.sleep( duration )
			
if __name__ == "__main__" :
	marque = "AVIDSEN"
	button = "1 ON"
	
	if len(sys.argv) > 2:
		marque = sys.argv[1]
		button = sys.argv[2] + " " + sys.argv[3]
	else :
		print "arguments incorrects :"
		print sys.argv[0] + " <marque> <id> <position>"
		sys.exit(1)
	
	#cycles_perdus = 2
	tempsPerdu = 0
	dataPin    = 17
	nb_retry   = 4
	# Nombre de secondes d'attente entre deux retry
	attenteEntrePaquets = 0.075
	
	GPIO.setwarnings(False) 
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(dataPin, GPIO.OUT)
	
	if not marque in tableau :
		print "marque %s inconnue" % ( marque )
		exit( 1 )
	
	if not 0 in tableau[marque]["bits"] :
		print "erreur paramétrage bit 0  pour la marque %s"% ( marque )
		exit( 1 )
		
	if not 1 in tableau[marque]["bits"] :
		print "erreur paramétrage bit 1  pour la marque %s"% ( marque )
		exit( 1 )
		
	if not button in tableau[marque]["buttons"] :
		print "boutton %s inconnu  pour la marque %s" % ( button, marque )
		exit( 1 )	
	
	if not "echantillonnage" in tableau[marque] :
		print "echantillonnage mal paramétré pour la marque %s" % ( marque )
		exit( 1 )	

	# Compensation systeme non temps réel
	# Etallonage de la perte de temps moyenne : A la recherche du temps perdu pour faire n envois de paquets, ce temps ne doit pas être utilisé pour calculer l'attente
#	nbVal       = 10
#	sendingTime = 0.0001
#	t1 = time.time()
#	for valeur in range(0, nbVal + 1):
#		sendDataPulse( dataPin, sendingTime, 1 )
#	t2 = time.time()
#	tempsPerdu = ( 1.0 * ( t2 - t1 ) / nbVal ) - sendingTime
#	#print tempsPerdu
	tempsPerdu = 0
	
	# Précalcul les attentes pour chaque type de bits
	paramBits = {}
	for valeur in range(0, 2):
		paramBits[ valeur ] = [] 
		for paramBit in tableau[marque]["bits"][valeur]:
			tempsAttente  = 1.0 * ( paramBit[0] - tempsPerdu) / tableau[marque]["echantillonnage"]
			paramBits[valeur].append( [ tempsAttente , paramBit[1] ] )
			
	sendDataPulse( dataPin, 0.01 , 0 )
	for i in range( 0, nb_retry ) :
		for bit in tableau[marque]["buttons"][ button ]:
			for paramBit in paramBits[ int( bit ) ]:
				sendDataPulse ( dataPin, paramBit[0], paramBit[1])
		sendDataPulse( dataPin, 0.01 , 0 )
		time.sleep( attenteEntrePaquets )
	sendDataPulse( dataPin, 0.01 , 0 )
	
	GPIO.cleanup()

