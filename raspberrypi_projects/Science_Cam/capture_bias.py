# https://astrobackyard.com/bias-frames-astrophotography/

from picamera import PiCamera
import time
from fractions import Fraction
import datetime
import os

def bias_capture(resolution, contrast, iso_val, frame_rate_denom, n_bias, save_folder):
    # resolution - resolution at which final image will be taken. Its list of two values
    # contrast - The contrast setting goes from -100 to 100, 0 being the default (no change).
    # iso_val - iso value at which bias should be taken
    # n_bias - number of bias frames to be captured
    # save_folder - folder where bias frame is to be saved
    
    path = save_folder + "/BiasFrames"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")
    
    camera = PiCamera(framerate=Fraction(1,frame_rate_denom)) # 24 frames/second
    # shutter speed should be double the frame rate
    camera.shutter_speed = 200 # in microseconds
    camera.iso = iso_val
    camera.contrast = contrast
    camera.resolution = (resolution[0], resolution[1])
    time.sleep(3)
    
    i = 0
    
    print("Bias Frame capture start")
    
    while i < n_bias:
        file_name = path + "/" + str(time.time()) + ".jpg"
        camera.capture(file_name)
        time.sleep(0.5)
        i = i+1
    camera.close()
    
    print("Bias Frames capture finished")


#bias_capture([1280, 720], 0, 800, 10, 'path of folder in pi where the Images should be saved')
