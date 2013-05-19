
"""
Code source issu de :
http://www.zem.fr/raspberry-pi-et-afficheur-lcd-hitachi-hd44780-1602-part-2/
"""

import threading
import RPi.GPIO as GPIO
from time import sleep

__all__ = ['HD44780']

class HD44780(threading.Thread):
	######################
	# Variable Shared    #
	######################
	_PULSE = 0.00005
	_DELAY = 0.00005
 
	######################
	# Constructeur       #
	######################
	def __init__(self, pin_rs=7, pin_e=8, pins_db=[25, 24, 23, 18], lcd_width=16):
		self.message = ""
		self.currentmessage = "azertyuiop"
		self.stop = False
		self.lcd_width = lcd_width
		self.pin_rs = pin_rs
		self.pin_e = pin_e
		self.pins_db = pins_db
		GPIO.setmode(GPIO.BCM) 				# Use BCM GPIO numbers
		GPIO.setup(self.pin_e, GPIO.OUT)
		GPIO.setup(self.pin_rs, GPIO.OUT)
		for pin in self.pins_db:
			GPIO.setup(pin, GPIO.OUT)
 
		self.Clear()
		threading.Thread.__init__(self)
 
	######################
	# Demarrage du Thread# 
	######################
	def run(self):
		while self.stop == False:
			if self.message != self.currentmessage:
				self.currentmessage = self.message
				self.LcdMessage()
			sleep(0.1)
		self.__del__()
 
	######################
	# Arret du Thread    # 
	######################	
	def Stop(self):
		self.stop = True
 
	######################
	# Initialisation LCD # 
	######################
	def Clear(self):
		""" Blank / Reset LCD """
		self.LcdByte(0x33, False) # $33 8-bit mode
		self.LcdByte(0x32, False) # $32 8-bit mode
		self.LcdByte(0x28, False) # $28 8-bit mode
		self.LcdByte(0x0C, False) # $0C 8-bit mode
		self.LcdByte(0x06, False) # $06 8-bit mode
		self.LcdByte(0x01, False) # $01 8-bit mode
 
	######################
	#Execution sur le LCD# 
	######################
	def LcdByte(self, bits, mode):
		""" Send byte to data pins """
		# bits = data
		# mode = True  for character
		#        False for command
 
		GPIO.output(self.pin_rs, mode) # RS
 
		# High bits
		for pin in self.pins_db:
			GPIO.output(pin, False)
		if bits&0x10==0x10:
			GPIO.output(self.pins_db[0], True)
		if bits&0x20==0x20:
			GPIO.output(self.pins_db[1], True)
		if bits&0x40==0x40:
			GPIO.output(self.pins_db[2], True)
		if bits&0x80==0x80:
			GPIO.output(self.pins_db[3], True)
 
		# Toggle 'Enable' pin
		sleep(HD44780._DELAY)    
		GPIO.output(self.pin_e, True)  
		sleep(HD44780._PULSE)
		GPIO.output(self.pin_e, False)  
		sleep(HD44780._DELAY)      
 
		# Low bits
		for pin in self.pins_db:
			GPIO.output(pin, False)
		if bits&0x01==0x01:
			GPIO.output(self.pins_db[0], True)
		if bits&0x02==0x02:
			GPIO.output(self.pins_db[1], True)
		if bits&0x04==0x04:
			GPIO.output(self.pins_db[2], True)
		if bits&0x08==0x08:
			GPIO.output(self.pins_db[3], True)
 
		# Toggle 'Enable' pin
		sleep(HD44780._DELAY)    
		GPIO.output(self.pin_e, True)  
		sleep(HD44780._PULSE)
		GPIO.output(self.pin_e, False)  
		sleep(HD44780._DELAY) 	
 
	######################
	#Affichage sur le LCD# 
	######################	
	def LcdMessage(self):
		""" Send string to LCD. Newline wraps to second line"""
		self.Clear()
		text = self.currentmessage
		self.LcdByte(0x80, False)
		for c in text:
			if c == '\n':
				self.LcdByte(0xC0, False) # next line
			else:
				self.LcdByte(ord(c),True)
 
	######################
	#Definir le message  # 
	######################
	def LcdSetMessage(self, text):
		self.message = text.ljust(self.lcd_width," ")

	def __del__(self):
		#GPIO.output(self.pin_rs, False)
		#GPIO.output(self.pin_e,  False)
		#for pin in self.pins_db:
		#	GPIO.output(pin, False)
		GPIO.cleanup()
