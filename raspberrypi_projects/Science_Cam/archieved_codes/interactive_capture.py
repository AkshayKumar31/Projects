# https://blog.devgenius.io/running-multiple-functions-at-once-in-python-using-the-multiprocessing-module-4c1fe3ed9878
# https://stackoverflow.com/questions/65974055/how-to-run-two-functions-with-different-arguments-run-parallely-in-python-with-i
from picamera import PiCamera
import time
from fractions import Fraction
from picamera.array import PiRGBArray
import capture_images
import capture_light
import capture_dark
from flask import request, Flask, render_template, url_for, redirect, Response 
import io
import logging
import socketserver
from threading import Condition
from http import server
import cv2
import cam_streamer
from multiprocessing import Process,Queue

#https://tree.rocks/a-simple-way-for-motion-jpeg-in-flask-806b8bfefa96
#https://picamera.readthedocs.io/en/latest/recipes2.html#rapid-capture-and-streaming

shutter_speed = 50000
iso = 800
contrast = 0
resolution = [1440, 1440]
frame_rate_denominator = 24
savefolder = 'path of folder in pi where the Images should be saved'
camera = None

app = Flask(__name__)
app.secret_key = "camera"

@app.route("/",  methods=["POST", "GET"])
def home():
    # No redirects happen to homepage so camera doesnt need to reinitialize, so doesn't throw errors. 
    global camera
    camera = PiCamera(framerate=Fraction(1,frame_rate_denominator)) # 24 frames/second
    # shutter speed should be double the frame rate
    # Lignt, Dark and Image frames should be captured at same camera settings
    camera.shutter_speed = shutter_speed # in microseconds
    camera.iso = iso
    camera.contrast = contrast
    camera.resolution = (resolution[0], resolution[1])
    time.sleep(3)
    
    
    p2 = Process(target=cam_streamer.stream, args=(camera,))
    p2.start()
    print("rendering html page")
    
    return render_template("index.html")

'''
def gen(cam):
    output = io.BytesIO()
    while True:
        for foo in cam.capture_continuous(output, format= "jpeg", use_video_port=True):
            output.seek(0)
            frame = output.read()
            output.truncate()
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
'''

@app.route("/stream",  methods=["POST", "GET"])
def stream():
    #global camera
    #p2 = Process(target=cam_streamer.stream, args=(camera,))
    #p2.start()
    return redirect("http://{Your pi ip address on local network}:{port on which web app is deployed in pi}/stream")

@app.route("/capture_image",  methods=["POST", "GET"])
def capture_image():
    capture_images.capture_image(camera, savefolder)
    return redirect(url_for("stream"))
    

if __name__ == "__main__":
    
    p1 = Process(target=app.run, args=('0.0.0.0',4000))
    p1.start()

    


