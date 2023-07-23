'''
  A Simple mjpg stream http server for the Raspberry Pi Camera
  inspired by https://gist.github.com/n3wtron/4624820
'''

# https://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python

from http.server import BaseHTTPRequestHandler,HTTPServer
import io
import time
import capture_images
import capture_image_burst
import capture_light
import capture_dark
import capture_video
from picamera import PiCamera
from fractions import Fraction
import json
import threading
import socket
from math import floor

camera=None

class CamHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path.endswith('.mjpg'):
      self.send_response(200)
      self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
      self.end_headers()
      stream=io.BytesIO()
      try:
        start=time.time()
        for foo in camera.capture_continuous(stream,'jpeg', use_video_port=True):
          self.wfile.write(bytes("--jpgboundary", "utf8"))
          self.send_header('Content-type','image/jpeg')
          self.send_header('Content-length',len(stream.getvalue()))
          self.end_headers()
          self.wfile.write(stream.getvalue())
          stream.seek(0)
          stream.truncate()
          #time.sleep(.5)
      except KeyboardInterrupt:
        pass
      return
    elif self.path == '/stream':
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      file=open("{path to the script folder}/templates/base.html","r")
      html_string = file.read()
      file.close
      #self.wfile.write(bytes("<html><head></head><body><img src='/cam.mjpg'/><form action='/capture' method='post'><div class='buttoncontainer'><button type='submit'>Capture Image</button></div></center></body></html>", "utf8"))
      self.wfile.write(bytes(html_string, "utf8"))
      return
    
  def do_POST(self):
        print("inside post")
        self.send_response(200)  # OK
        self.send_header('Content-type', 'text')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        result = json.loads(body, encoding='utf-8')
        print(result["body"])
        if result["body"] == 'capture_image':
            print("capturing image")
            capture_images.capture_image(camera, savefolder)
        elif result["body"] == 'capture_burst':
            print("capturing burst image frames")
            capture_image_burst.capture_image_burst_frame(camera, savefolder, 10)
        elif result["body"] == 'capture_light':
            print("capturing light frames")
            capture_light.capture_light_frame(camera, savefolder, 10)
        elif result["body"] == 'capture_dark':
            print("capturing dark frames")
            capture_dark.capture_dark_frame(camera, savefolder, 10)
        elif result["body"] == 'capture_video':
            # Doesnt work for long exposure. Returns dark or empty video
            print("starting video recording")
            capture_video.video_capture(camera, savefolder)
        elif result["body"] == 'stop_video':
            print("stopping video recording")
            capture_video.stop_video(camera)
        return
# Create ONE socket.
addr = ('', 8080)
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(addr)
sock.listen(5)

class Thread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.i = i
        self.daemon = True
        self.start()
    def run(self):
        try:
            server = HTTPServer(addr ,CamHandler, False)
            print("server started")
            server.socket = sock
            server.server_bind = self.server_close = lambda self: None
            server.serve_forever()
        except KeyboardInterrupt:
            server.socket.close()

def stream(cam):
  global camera
  camera = cam
  #camera = picamera.PiCamera()
  #camera.resolution = (1280, 960)
  #camera.resolution = (640, 480)
  global img
  try:
    [Thread(i) for i in range(5)]
  except KeyboardInterrupt:
    camera.close()

# Calling the function
iso = 400
contrast = 0
exposure_mode = "on" # "off" - Avoids resetting shutter speed and frame rate. Used for long exposure astro photography.
resolution = [1280, 960]
frame_rate = 30 #6 for 1/6 frames per second or 1 frame per 6 seconds for long exposure.
shutter_speed = floor((1/(2*frame_rate))*1000000)-100 #2900000 for long exposure astrophotos. Better to take in burst mode.
print(shutter_speed)
savefolder = 'path of folder in pi where the Images should be saved'
#cam = PiCamera(framerate=Fraction(1,frame_rate_denominator)) # 24 frames/second
# shutter speed should be double the frame rate
# Lignt, Dark and Image frames should be captured at same camera settings
#cam = PiCamera(framerate = Fraction(1,frame_rate_denominator))
cam = PiCamera(framerate = frame_rate)
cam.shutter_speed = shutter_speed # in microseconds
cam.iso = iso
cam.contrast = contrast
cam.resolution = (resolution[0], resolution[1])
if exposure_mode == "off":
    cam.exposure_mode = exposure_mode
time.sleep(3)
stream(cam)