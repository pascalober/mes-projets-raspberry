import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
# Set up #17 as an output
print "Setup #17"
GPIO.setup(17, GPIO.OUT)
 
var=1
print "Start loop"
while var==1:
 print "Set Output False"
 GPIO.output(17, False)
 time.sleep(1)
 print "Set Output True"
 GPIO.output(17, True)
 time.sleep(1)
