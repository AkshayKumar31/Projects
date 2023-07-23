import time
import os

def video_capture(camera_object, save_folder):
    
    print("started video function")
    path = save_folder + "/Video"
    
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")
        
    file_name = path + "/" + str(time.time()) + ".h264"
    print('video capturing')
    print(time.ctime(time.time()))
    camera_object.start_recording(file_name)
    print(time.ctime(time.time()))

def stop_video(camera_object):
    camera_object.stop_recording()
