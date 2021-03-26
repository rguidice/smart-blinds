import time
from flask import Flask
from flask import jsonify
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]
light_pin = 5
day_flag = 0

app = Flask(__name__)

for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
  
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

halfstep_seq_close = [
  [1,0,0,1],
  [0,0,0,1],
  [0,0,1,1],
  [0,0,1,0],
  [0,1,1,0],
  [0,1,0,0],
  [1,1,0,0],
  [1,0,0,0],
]

first_flag = 0
count = 0
auto_control = 0
opened = False

def rc_time(light_pin):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(light_pin, GPIO.OUT)
    GPIO.output(light_pin, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(light_pin, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(light_pin) == GPIO.LOW):
        count += 1

    return count * 10

@app.route('/time')
def get_current_time():
	print("HERE IN TIME")
	return "GOT HERE IN TIME"
	
@app.route('/open')
def open_b():
  f = open("state", "w")
  f.write("1")
  f.close()
  for i in range(500):
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)
  return jsonify({})

@app.route('/close')    
def close_b():
  f = open("state", "w")
  f.write("0")
  f.close()
  for i in range(500):
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(control_pins[pin], halfstep_seq_close[halfstep][pin])
      time.sleep(0.001)
  return jsonify({})
      
@app.route('/get_state')    
def get_state():
	f = open("state", "r")
	#print(f.read(), "hi")
	ret = False
	if f.read() == "1":
		ret = True
	f.close()
	print(ret)
	return jsonify(state=ret)
