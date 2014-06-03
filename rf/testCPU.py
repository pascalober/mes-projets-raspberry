#!/usr/bin/python
import RPi.GPIO as GPIO
import threading
from time import sleep, time
import signal

class RFServer( threading.Thread ):
	pinIn = 17
	def __init__(self, __pinIn):
		self.pinIn = __pinIn
		self.working = True
		GPIO.setmode( GPIO.BCM )
		GPIO.setup (self.pinIn , GPIO.IN )
		threading.Thread.__init__(self)
		
	def SignalStop(self, signal, val):
		print( "Got Signal : ")
		self.working = False
		self.join()

	def run( self ):
		t=time()
		d=0
		ps=None
		st = ''
		str=''
		while self.working:
			s = GPIO.input ( self.pinIn )
			sleep(0.0005)
			if ps!=s:
				if s:
					d = round(time() - t, 3)
					print repr( d ) + " : " + repr( s )
					#~ if d < 0.02:
						#~ st += '1'
					#~ elif d >= 0.02 and d <= 0.03:
						#~ st += '0'
					#~ elif d > 0.03 and d < 0.2:
						#~ if len( st )>0:
							#~ print st
							#~ #str += chr( int( st, 2 ) )
							#~ st = ''
					t = time()
				ps = s
			d2 = round(time()-t, 3)
			if d2 > 0.2 and str!='':
				#print('\nReceived:\n'+str)
				str=''
def fMain():
	pinIn = 17
	rfServeur = RFServer( pinIn )
	
	signal.signal(signal.SIGINT,  rfServeur.SignalStop)
	signal.signal(signal.SIGQUIT, rfServeur.SignalStop)
	signal.signal(signal.SIGTERM, rfServeur.SignalStop)

	rfServeur.start()
	while rfServeur.working :
		sleep(1)
	print("post while")
	rfServeur.working = False
	rfServeur.join()
	print("exit")

if __name__ =='__main__':
	fMain()


