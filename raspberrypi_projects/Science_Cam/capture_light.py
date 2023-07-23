import time
import os


def capture_light_frame(camera_object, save_folder, n_frames):
    # camera_object - Initialized camera object so that it doesnt need to be initialize every time
    # save_folder - folder where bias frame is to be saved
    # n_frames = number of light frames to be captured
    
    path = save_folder + "/LightFrames"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")
    
    i = 0
    
    while i < n_frames:
        file_name = path + "/" + str(time.time()) + ".jpg"
        print(time.ctime(time.time()))
        camera_object.capture(file_name)
        print(time.ctime(time.time()))
        time.sleep(0.5)
        i = i+1
    
    print('Light frames captured')