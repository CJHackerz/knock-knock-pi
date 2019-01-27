import RPi.GPIO as GPIO
from picamera import PiCamera
import requests
import os
import time

#Raspberry pi GPIO config. according to wiring setup
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
camera = PiCamera()

def sendMail(sendfile):
	return requests.post(
		"https://api.mailgun.net/v3/YOUR_DOMAIN/messages",
		auth=("api", os.environ['MAILGUN_API_KEY']),
		files=[("attachment", open(sendfile, 'rb'))],
		data={
		"from": "HomeSecurity Bot <bot@YOUR_DOMAIN>",
		"to": ["Full Name", "alice@example.com"],
		"subject": "Security Alert",
		"text": "Someone is at front door!"
		})

while True:		#Continues code execution
	print("Distance Measurement In Progress")

	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)

	GPIO.output(TRIG, False)
	print("Waiting For Sensor To Settle")
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

	print("Distance: {} cm".format(distance))

	if distance < 20: #Make tweet if somthing found at less than 20cm range
		print("Found something in close range! Recording 10 second footage...")
		footage_out_fname = os.getcwd() + "/" + "security_footage-" + str(time.time()) + '.h264'
		camera.start_recording(footage_out_fname)
		time.sleep(5)
		camera.stop_recording()
		time.sleep(1)
		print("Converting file to .mp4")
		os.system("ffmpeg -framerate 30 -i {} -c copy security_footage.mp4".format(footage_out_fname))
		time.sleep(2)
		print("Sending email notification...")
		print(sendMail(os.getcwd() + "/security_footage.mp4"))
		os.system("rm -drf security_footage.mp4")
GPIO.cleanup()

# =>Code written by: CJHackerz
# ++ https://github.com/cjhackerz