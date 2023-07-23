For long exposure astrophotography: (Video comes out blank in this mode. Images comes out fine.)

shutter_speed = floor((1/(2*frame_rate))*1000000)-100 in micro seconds which is slightly more than twice of the frame rate.
frame_rate = 1/6 for 1/6 frames per second, or 1 frame per 6 seconds.
Lowest iso value for least noise.
Better to take in burst mode to enable noise reduction using stacking.
Set exposure_mode = "off" Avoids resetting shutter speed and frame rate. Used for long exposure astro photography.


General rule of imaging:

Shutter speed should be double the frame rate
Lignt, Dark and Image frames should be captured at same camera settings
Default resolution = [1280, 960]
Default framerate = 30
Default shutter speed = floor((1/(2*frame_rate))*1000000)-100
Set exposure_mode = "on" (if left "off" images comes out black in this mode. Video comes out fine.)