from star import Star
from gpiozero.tools import random_values
import threading
import time
import requests

step = 0.5
count = 0
star = Star(pwm=True)
leds = star.leds

ticks=time.time();
timeout=ticks+5;

power=""
oldPower=""
powerChanged = False
tweetclass=""
oldtweetclass=""
tweetclassChanged = False
exitFlag = 0

class myThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		print "Initialising " + self.name
	def run(self):
		print "Starting " + self.name
		global ticks;
		global timeout;
		global power;
		global oldPower;
		global powerChanged;
		global tweetclass;
		global oldtweetclass;
		global tweetclassChanged;
		while not exitFlag:
			ticks=time.time();
			if(ticks>timeout):
				timeout=ticks+5;
				responsePower = requests.get("http://pistar:1880/power");
				if(responsePower.status_code==200):
					localtime = time.asctime( time.localtime(time.time()) )
					power = responsePower.json()['power'];
					if(power != oldPower):
						print(localtime + ": Setting power: " + power)
						powerChanged = True;
						oldPower = power;
						if(power=="on"):
							tweetclassChanged = True;
					response = requests.get("http://pistar:1880/lastWindowMostPopular");
					if(response.status_code==200):
						if(power=="on"):
							tweetclass = response.json()['lastWindowMostPopular'][0:2]
							if(tweetclass != oldtweetclass):
								print(localtime + ": Setting tweetclass: " + tweetclass)
								tweetclassChanged = True;
								oldtweetclass = tweetclass;
					else:
						print("Error: " + str(response.status_code))
				else:
					print("Error: " + str(responsePower.status_code))
			else:
				time.sleep(1);
		print "Exiting " + self.name

# Create and start new thread
thread1 = myThread(1, "Tweet Poller")
thread1.start()

try:
	while True:
		if(powerChanged):
			powerChanged = False;
			if(power == "off"):
				star.off();
		if(tweetclassChanged):
			tweetclassChanged = False;
			if(tweetclass=="br"):
				#print("brexit - blink")
				star.off()
				star.blink()
			elif(tweetclass=="co"):
				#print("covid - pulse")
				star.off()
				star.pulse()
			elif(tweetclass=="ch"):
				#print("christmas - random leds")
				#for led in leds:
				#	led.source_delay = 0.1
				#	led.source = random_values()	
				#print("christmas - on")
				star.off()
				star.on()
			else:
				print("Unknown tweetclass: " + tweetclass)
		time.sleep(10)
except KeyboardInterrupt:
	exitFlag = 1;
	star.off()
	star.close()
