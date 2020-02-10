#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get,post,run,route,request,template,static_file
#from AlphaBot import AlphaBot
#from PCA9685 import PCA9685
from adafruit_motorkit import MotorKit
import threading
import socket #ip
import os

drv = MotorKit()
#Ab = AlphaBot()
#pwm = PCA9685(0x40)
#pwm.setPWMFreq(50)

#Set servo parameters
HPulse = 1500  #Sets the initial Pulse
HStep = 1.00      #Sets the initial step length
VPulse = 1500  #Sets the initial Pulse
VStep = 0      #Sets the initial step length
#pwm.setServoPulse(1,VPulse)
#pwm.setServoPulse(0,HPulse)
Speed = 0.5



@get("/")
def index():
	return template("index")
	
@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./')

@route('/fonts/<filename>')
def server_fonts(filename):
    return static_file(filename, root='./fonts/')
	
@post("/cmd")
def cmd():
    global HStep,VStep,Speed
    code = request.body.read().decode()
    speed = request.POST.get('speed')
    print(code)
    if(speed != None):
        #Ab.setPWMA(float(speed))
        #Ab.setPWMB(float(speed))
        Speed = (int(speed) * .01)
        print(speed)
        print(Speed)
    if code == "stop":
        #HStep = 0
        VStep = 0
        drv.motor1.throttle = 0
        drv.motor2.throttle = 0
        #Ab.stop()
        print("stop")
    elif code == "forward":
        #Ab.forward()
        drv.motor1.throttle = -(Speed * HStep) 
        drv.motor2.throttle = -(Speed)
        #print("forward")
        print(Speed)
    elif code == "backward":
        #Ab.backward()
        drv.motor1.throttle = Speed 
        drv.motor2.throttle = Speed
        print("backward")
    elif code == "turnleft":
        #Ab.left()
        drv.motor2.throttle = -(Speed) 
        print("turnleft")
    elif code == "turnright":
        #Ab.right()
        drv.motor1.throttle = -(Speed)
        print("turnright")
    elif code == "up":
        VStep = -5
        print("up")
    elif code == "down":
        VStep = 5
        print("down")
    elif code == "left":
        HStep = HStep - 0.01
        print(HStep)
        #print("left")
    elif code == "right":
        HStep = HStep + 0.01
        print(HStep)
        #print("right")
    return "OK"
	
def timerfunc():
	global HPulse,VPulse,HStep,VStep,pwm
	
	if(HStep != 0):
		HPulse += HStep
		if(HPulse >= 2500): 
			HPulse = 2500
		if(HPulse <= 500):
			HPulse = 500
		#set channel 2, the Horizontal servo
		#pwm.setServoPulse(0,HPulse)    
		
	if(VStep != 0):
		VPulse += VStep
		if(VPulse >= 2500): 
			VPulse = 2500
		if(VPulse <= 500):
			VPulse = 500
		#set channel 3, the vertical servo
		#pwm.setServoPulse(1,VPulse)   
	
	global t        #Notice: use global variable!
	t = threading.Timer(0.02, timerfunc)
	t.start()
    
def camera():
    lastpath = os.path.abspath(os.path.join(os.getcwd(), "../"))
    print("lastpath = %s" %lastpath)
    campath = lastpath + '/mjpg-streamer/mjpg-streamer-experimental/'
    print("campath = %s" %campath)
    os.system(campath  + './mjpg_streamer -i "' + campath + './input_uvc.so" -o "' + campath + './output_http.so -w ' + campath + './www"') 

tcamera = threading.Thread(target = camera)
tcamera.setDaemon(True)
tcamera.start()
tcamera = threading.Thread(target = camera)
tcamera.setDaemon(True)
tcamera.start()

t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(('8.8.8.8',80))
localhost=s.getsockname()[0]
run(host = localhost, port = 8000)
