# https://roboticsbackend.com/raspberry-pi-camera-picamera-python-library/
# https://learn.adafruit.com/raspberry-pi-hq-camera-low-light-long-exposure-photography/python-code

import time
import os


def capture_image(camera_object, save_folder):
    # camera_object - Initialized camera object so that it doesnt need to be initialize every time
    # save_folder - folder where bias frame is to be saved
    print("started image function")
    path = save_folder + "/ImageFrames"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")
    
    file_name = path + "/" + str(time.time()) + ".jpg"
    print(time.ctime(time.time()))
    camera_object.capture(file_name)
    print(time.ctime(time.time()))
    print('image captured')
    time.sleep(0.5)