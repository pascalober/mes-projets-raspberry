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
from Button import *
import os


class ScreenMaestro():
	def __init__(self):
		self.State = "Pause"
		self.Media = "Radio"
		self.text = self.getText()
		
	def getText(self):
		return (self.Media + " - "  + self.State)
		
class GUI(threading.Thread):
	def __init__(self):
		self.lcd = HD44780()
		self.lcd.start()
		self.lcd.LcdSetMessage("Maestro Starting")
		self.playing = False
		self.stop = False
		
		self.ScreenMaestro = ScreenMaestro()
		self.ScreenMaestro.State = "Pause"
		self.ScreenMaestro.Media = "Radio"
		self.lcd.LcdSetMessage( self.ScreenMaestro.getText() )

		self.bouton1 = Button( 4, self.Button1Pressed )
		self.bouton1.start()
		
		self.bouton2 = Button( 17, self.Button2Pressed )
		self.bouton2.start()
		
		self.bouton3 = Button( 27, self.Button3Pressed )
		self.bouton3.start()
		
    self.bouton4 = Button( 22, self.Button4Pressed )
		self.bouton4.start() 
      
		threading.Thread.__init__(self)

	def Stop(self):
		#print("Appel de GUI.Stop()")
		os.system("mpc pause")
		self.stop = True
		self.lcd.Stop()
		self.bouton1.Stop()
		self.bouton2.Stop()
		self.bouton3.Stop()

	def run(self):
		self.lcd.LcdSetMessage("Mestro Running")
		while self.stop == False:
			sleep(0.1)
			

	def SignalStop(self, signal, frame):
		self.Stop()
		sys.exit(0)
		
	def Button1Pressed(self):
		#self.button1count += 1
		#print("Button Pressed : %d" % self.button1count )
		#self.lcd.LcdSetMessage( "Button1Press:%d" % self.button1count )
		if ( self.playing == True ):
			os.system("mpc pause")
			self.ScreenMaestro.State = "Pause"
			self.playing = False
		else:
			os.system("mpc play")
			self.ScreenMaestro.State = "Play"
			self.playing = True
		self.lcd.LcdSetMessage( self.ScreenMaestro.getText() )

	def Button2Pressed(self):
		#self.button2count += 1
		#print("Button Pressed : %d" % self.button2count )
		#self.lcd.LcdSetMessage( "Button2Press:%d" % self.button2count )
		os.system("mpc next")
		os.system("mpc play")
		self.ScreenMaestro.State = "Play"
		self.playing = True
		self.lcd.LcdSetMessage( self.ScreenMaestro.getText() )


	def Button3Pressed(self):
		 os.system("mpc volume -10")

	def Button4Pressed(self):
		 os.system("mpc volume +10")


if __name__ == '__main__':
	gui = GUI()
	gui.start()
	signal.signal(signal.SIGINT, gui.SignalStop)
	signal.signal(signal.SIGQUIT, gui.SignalStop)
	signal.signal(signal.SIGTERM, gui.SignalStop)
	while 1 :
		sleep ( 60 )
	gui.Stop()



