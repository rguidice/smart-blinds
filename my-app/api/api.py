##########################################
#### CS370 SP21 Final Project
#### Ryan Guidice and Andrew Helmreich
#### TEAM: Datsun

# Import modules
import time
from flask import Flask
from flask import jsonify
import RPi.GPIO as GPIO

# Setup GPIO and pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
control_pins = [7,11,13,15]
light_pin = 5
day_flag = 0
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

app = Flask(__name__)

# Define arrays for stepper motor operation
halfstep_seq_close = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

halfstep_seq_open = [
    [1,0,0,1],
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0],
    [1,0,0,0],
]

# Global variables for controlling operation
first_flag = 0
count = 0
auto_control = 0
opened = False

# Function to get integer value based on light level detected by photoresistor
# Based on code from: https://pimylifeup.com/raspberry-pi-light-sensor/
def rc_time(light_pin):
    count = 0
    # Setup GPIO for light_pin as output
    GPIO.setup(light_pin, GPIO.OUT)
    # Send low signal
    GPIO.output(light_pin, GPIO.LOW)
    time.sleep(0.1)
    # Change light_pin back to input
    GPIO.setup(light_pin, GPIO.IN)
    # Count until the pin goes high
    while (GPIO.input(light_pin) == GPIO.LOW):
        count += 1
    # Return value multiplied by 10 to make detectable range wider
    return count * 10

# Helper function to read values from the state file
def read():
    f = open("state", "r")
    value = f.read()
    print(value)
    f.close()

# Flask function used for debugging purposes
@app.route('/time')
def get_current_time():
    print("HERE IN TIME")
    return "GOT HERE IN TIME"
	
# Flask function used to open the blinds
@app.route('/open')
def open_b():
    # Update the state file to be opened
    f = open("state", "w")
    f.write("0")
    f.close()
    # Open the blinds
    # Based on code from: https://keithweaverca.medium.com/controlling-stepper-motors-using-python-with-a-raspberry-pi-b3fbd482f886
    # 1700 deteremined to be value from close to open on our blinds
    for i in range(1700):
        for halfstep in range(8):
            for pin in range(4):
                # Output GPIO values based on stepper motor open array
                GPIO.output(control_pins[pin], halfstep_seq_open[halfstep][pin])
            # 0.0007 seconds determined to give fastest spin without losing torque
            time.sleep(0.0007)
    ##### CAN POSSIBLY REMOVE? ####
    read()
    # Return jsonify with empty dict to fulfill React promise
    return jsonify({})

@app.route('/close')    
def close_b():
    # Update the state file to be closed
    f = open("state", "w")
    f.write("1")
    f.close()
    # Close the blinds
    # Based on code from: https://keithweaverca.medium.com/controlling-stepper-motors-using-python-with-a-raspberry-pi-b3fbd482f886
    for i in range(1700):
        for halfstep in range(8):
            for pin in range(4):
                # Output GPIO values based on stepper motor close array
                GPIO.output(control_pins[pin], halfstep_seq_close[halfstep][pin])
            time.sleep(0.0007)
    read()
    # Return jsonify with empty dict to fulfill React promise
    return jsonify({})
      
# Flask function to return the value in state to compare with values in React code
@app.route('/get_state')    
def get_state():
    f = open("state", "r")
    ret = False;
    value = int(f.read())
    print(value == 1)
    if value == 1:
        ret = True
    f.close()
    print(ret, "HI")
    read()
    return jsonify(ret)
	
# Flask function to manage the autocontrol process
@app.route('/autocontrol')
def autocontrol():
    # Get the current state of the blinds
    f = open("state", "r")
    value = int(f.read())
    f.close()
    day_flag = not value
    count = 0
    # Switch the value in autocontrol_state file
    f = open("autocontrol_state", "r")
    value = int(f.read())
    print("VALUE BEFORE", int(value))
    if(value == 1):
        value = "0"
    print(int(value) == 0)
    if(value == 0):
        value = "1"
    print("VALUE AFTER", value)
    f.close()
    f = open("autocontrol_state", "w")
    f.write(value)
    f.close()
	
    # Infinite loop that runs autocontrol process
    while(True):
        # Read in autocontrol value
        f = open("autocontrol_state", "r")
        value = int(f.read())
        f.close()
        # If the value is set back to 0, then break out
        # This is how we break out of the infinite loop, since the autocontrol UI button in React
        # calls this same function on each press
        print("VALUE: ", value)
        if(value == 0):
            break
        if(value == 1):
            print("HERE")
            # Get the current light integer value
            light = rc_time(light_pin)
            print("LIGHT: ",light)
            # Larger light values indicate darker settings
            # Increment count variable if the light reading exceeds determined darkness threshold
            # and it's currently "day" based on the blinds orientation
            if light > 1700 and day_flag == 1:
                print("Night")
                count += 1
                # Once 5 repeated readings occur, close
                # the blinds. This prevents 1 or 2
                # incorrect readings from opening the blinds
                if count == 5:
                    print("Closing")
                    close_b()
                    day_flag = 0
                    count = 0
            # Same as with night, but opposite values
            # Small difference in light ranges to prevent repeated opening/closing of blinds
            elif light < 1500 and day_flag == 0:
                print("Day")
                count += 1
                if count == 5:
                    print("Opening")
                    open_b()
                    day_flag = 1
                    count = 0
            # Reset count value if it wasn't valid
            elif light > 1700 and day_flag == 0:
                if count != 0:
                    count = 0
            elif light < 1500 and day_flag == 1:
                if count != 0:
                    count = 0
        # Wait 2 seconds between each reading
        time.sleep(2)
    return "0"
