#!/usr/bin/python


############################
# Imports                  #
############################

import threading
import RPi.GPIO as GPIO
from time import sleep
import signal
import sys
sys.path.append('lib')
from LCD import *

class Cligno(threading.Thread):
	def __init__(self):
		self.stop = False
		GPIO.setmode(GPIO.BCM)
		# Set up #2 as an output
		print "Setup #2"
		GPIO.setup(2, GPIO.OUT)
		# Set up #3 as an output
		print "Setup #3"
		GPIO.setup(3, GPIO.OUT)
		
		threading.Thread.__init__(self)

	def run(self):
		(on, off) = ( 2, 3 )
		while self.stop == False:
			GPIO.output(off, False)
			GPIO.output(on, True)
			(on, off) = ( off, on )
			if ( self.stop == False ) : sleep(1) 

	def Stop(self) :
			self.stop = True
			
class GUI(threading.Thread):
	def __init__(self):
		self.lcd = HD44780()
		self.lcd.start()
		self.lcd.LcdSetMessage("Hello Cosmic\n World")
		self.stop = False
		
		self.Cligno = Cligno()
		self.Cligno.start()
		threading.Thread.__init__(self)

	def Stop(self):
		print("Appel de GUI.Stop()")
		self.stop = True
		self.lcd.Stop()
		self.Cligno.Stop()
	def run(self):
		i=1
		while self.stop == False:
			self.lcd.LcdSetMessage( "MESSAGE : %d     \n                 " % i )
			sleep( 1 )
			i += 1

	def SignalStop(self,signal, frame):
		self.Stop()
		sys.exit(0)


if __name__ == '__main__':
	gui = GUI()
	gui.start()
	signal.signal(signal.SIGINT, gui.SignalStop)
	signal.signal(signal.SIGQUIT, gui.SignalStop)
	signal.signal(signal.SIGTERM, gui.SignalStop)
	while 1 :
		sleep ( 60 )
	gui.Stop()



