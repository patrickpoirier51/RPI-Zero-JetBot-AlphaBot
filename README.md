# RPI-Zero-JetBot-AlphaBot
A JetBot frame wih a RPI Zero running a WaveShare AlphaBot2-pi python script

**Instruction:**

Download tar file from WaveShare.com/wiki/Alphabot2-pi 

Install required libraries as per wiki

Install the  adafruit_motorkit library

Build the mjpeg streamer code

Copy pi-rover.py to /home/pi/AlphaBot2/Web-Control


**To run:**

Load MJPEG Streamer

Load the pi-rover.py script

Load your Chrome Browser and go to the RPI Zero local network IP adress with suffix :8000

Control vehicle using arrows and trim


**For automatic start:**

edit /ect/rc.local and add

cd /home/pi/AlphaBot2/Web-Control

python3 pi-rover.py &

exit 0
