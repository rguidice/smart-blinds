import RPi.GPIO as GPIO
import time
import zmq

GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]
light_pin = 5
day_flag = 0
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

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

def open_b():
  for i in range(500):
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
      time.sleep(0.001)
    
def close_b():
  for i in range(500):
    for halfstep in range(8):
      for pin in range(4):
        GPIO.output(control_pins[pin], halfstep_seq_close[halfstep][pin])
      time.sleep(0.001)

first_flag = 0
count = 0
auto_control = 0

try:
    while True:
        
        # Waiting here on every loop
        # Setting autocontrol on gets stuck here
        message = socket.recv_string()
        print("Received request: %s" % message)
        socket.send(b"hello")
        
        if message == "autocontrol_off":
          auto_control = 0
        elif message == "autocontrol_on":
          auto_control = 1
          print("HERE")
          
        if auto_control == 0 and message == "open":
          open_b()
        elif auto_control == 0 and message == "close":
          close_b()
  
        if auto_control == 1:
          if first_flag == 0:
            first_flag = 1
            time.sleep(5)
            continue
          light = rc_time(light_pin)
          print(light)
          if light > 1700 and day_flag == 1:
              print("Night")
              count += 1
              if count == 5:
                print("Closing")
                close_b()
                day_flag = 0
                count = 0
          elif light < 1500 and day_flag == 0:
              print("Day")
              count += 1
              if count == 5:
                print("Opening")
                open_b()
                day_flag = 1
                count = 0
          elif light > 1700 and day_flag == 0:
            if count != 0:
              count = 0
          elif light < 1500 and day_flag == 1:
            if count != 0:
              count = 0
        
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()



    

