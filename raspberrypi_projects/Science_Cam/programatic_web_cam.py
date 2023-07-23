from picamera import PiCamera
import time
from fractions import Fraction
import datetime
import os
import capture_images
import capture_light
import capture_dark
import capture_bias

shutter_speed = 500
iso = 800
contrast = 0
resolution = [1280, 720]
frame_rate_denominator = 24
savefolder = 'path of folder in pi where the Images should be saved'

# Bias frames are captured at same settings as light, dark, and image frames
# but shortest possible shutter speed
bias_descision = input("Do you want to take bias frame yes/no: ")
if bias_descision == 'yes':
    n_bias_frames = input("Enter the number of bias frames: ")
    n_bias_frames = int(n_bias_frames)
    capture_bias.bias_capture(resolution, contrast, iso, frame_rate_denominator, n_bias_frames, savefolder)
else:
    print("Bias not taken")

camera = PiCamera(framerate=Fraction(1,frame_rate_denominator)) # 24 frames/second
# shutter speed should be double the frame rate
# Lignt, Dark and Image frames should be captured at same camera settings
camera.shutter_speed = shutter_speed # in microseconds
camera.iso = iso
camera.contrast = contrast
camera.resolution = (resolution[0], resolution[1])
time.sleep(3)

while True:
    
    capture_image_type = input("Do you want to capture Image, Light, or Dark: ")
    
    if capture_image_type == 'image':
        capture_images.capture_image(camera, savefolder)
    elif capture_image_type == 'light':
        n_frames = input("Enter number of input frames to be captured: ")
        n_frames = int(n_frames)
        capture_light.capture_light_frame(camera, savefolder, n_frames)
    elif capture_image_type == 'dark':
        n_frames = input("Enter number of input frames to be captured: ")
        n_frames = int(n_frames)
        capture_dark.capture_dark_frame(camera, savefolder, n_frames)
    else:
        exit_option = input("Do you want to exit yes/no: ")
        if exit_option == 'yes':
            break
        
camera.close()
