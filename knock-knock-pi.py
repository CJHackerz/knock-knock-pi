import RPi.GPIO as GPIO
import time
import tweepy

#Raspberry pi GPIO config. according to wiring setup
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24

# This is twitter API configuiration from https://apps.twitter.com/
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACESS_KEY = ""
ACCESS_SECRET = ""

#Verifying auth.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

tweet = tweepy.API(auth) #API consumed into user defined object

tweet.update_status('This is test!') #Test status post on twitter timeline

#HC-SR04 script
while True:		#Continues code execution
	print "Distance Measurement In Progress"

	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)

	GPIO.output(TRIG, False)
	print "Waiting For Sensor To Settle"
	time.sleep(2)

	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
  		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
  		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	distance = round(distance, 2)

	print "Distance:",distance,"cm"

	if distance < 20: #Make tweet if somthing found at less than 20cm range
		tweet.update_status('Knock, Knock! Someone is at your Home!')
		print "Tweet posted!"

	GPIO.cleanup()






# =>Code written by: CJHackerz
# ++ https://github.com/cjhackerz
