Dependencies:
Flask 1.0.2
If using RPi 3 and up: Node 15.13.0 (ARM7 Version)
If using RPi 0W: Node 10.24.1 (ARM6 Version)
Make sure npm is installed with Node, whichever version matches the Node of your device

All important files located in my-app/
React files located in my-app/
Flask backend located in my-app/api

To start everything:
1. Start backend: go to my-app/api and run "flask run"
2. Start frontend: go to my-app and run "npm start"
3. Client-facing webpage located at localhost:3000
4. Accessible via other machines at server_ip:3000

Quick I/O pin lookup:
Stepper motor controller pins 1-4: 7, 11, 13, 15
Stepper motor power: 5V and GND
Photoresistor light pin: 5
Photoresistor power: 5V and GND
