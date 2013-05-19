#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Button.py
#  
#  Copyright 2013  <stephane.larson>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# Cablage trouvé sur http://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/bread-board-setup-for-input-buttons


import threading
import RPi.GPIO as GPIO
from time import sleep

# Constantes
# Dernier état :
#  1 si Pressed
# -1 si Relaché
#  0 si Indéfini
LAST_STATE_PRESSED = 1
LAST_STATE_UNDEF = 0
LAST_STATE_RELEASED = -1


class Button(threading.Thread):
	def __init__(self, pin, callbackPressed, callbackReleased=None):
		self.pin = pin
		self.stop = False
		self.callbackPressed   = callbackPressed
		self.callbackReleased  = callbackReleased
		self.lastState = LAST_STATE_UNDEF
		GPIO.setmode( GPIO.BCM )
		GPIO.setup( self.pin, GPIO.IN)
		threading.Thread.__init__(self)

	def run(self):
		#Boucle infinie
		while self.stop == False:
			# Je ne souhaite pas appeller les fonctions de callback lors du premier passage, d'où l'usage du test sur LAST_STATE_UNDEF
			# Test du cas où on appuye sur le bouton, il ne faut appeller la callback QUE dans le cas où le dernier état enregistré était et avec une callback définie
			if ( (self.lastState != LAST_STATE_PRESSED) and ( GPIO.input( self.pin ) == False ) ) :
				if ( ( self.lastState == LAST_STATE_RELEASED) and ( self.callbackPressed is not None ) ):
					self.callbackPressed()
				self.lastState = LAST_STATE_PRESSED
			# Cas du relachement du bouton
			elif ( (self.lastState != LAST_STATE_RELEASED) and ( GPIO.input( self.pin ) == True ) ) :
				if ( ( self.lastState == LAST_STATE_PRESSED) and ( self.callbackReleased is not None ) ):
					self.callbackReleased()

				self.lastState = LAST_STATE_RELEASED
			sleep( 0.1)
		self.__del__()

	def Stop( self):
		self.stop = True
		
	def __del__( self ):
		GPIO.cleanup()


def maCallback():
	print("Button Pressed");

def main():
	button = Button( 4, maCallback )
	button.start()
	q = str(raw_input('Press ENTER to quit program'))
	button.Stop()
	return 0

if __name__ == '__main__':
	main()

