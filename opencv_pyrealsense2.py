import pyrealsense2 as rs
import Jetson.GPIO as GPIO
import cv2 as cv
import numpy as np

# Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

# Setting Intel Realsense D435i
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

#Getting the sensor's depth scale
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth scale is: ", depth_scale)

#We will remove the background that is more than the clipping distance
clipping_distance_in_meters = 1
clipping_distance = clipping_distance_in_meters / depth_scale

#Create an align object
align_to = rs.stream.color
align = rs.align(align_to)


try:
    while True:
        #Read the frame
        frames = pipeline.wait_for_frames()

        #Get depth data
        depth_frame = frames.get_depth_frame()

        if not depth_frame: continue
        depth_image = np.asanyarray(depth_frame.get_data())

        #Applying color scale
        np_image = cv.convertScaleAbs(depth_image, alpha = 0.3)
        np_image = -np_image

        ret, thresh_image = cv.threshold(np_image, 127, 255, cv.THRESH_BINARY)

        #Getting parameters
        width = depth_frame.get_width()
        height = depth_frame.get_height()

        img_left = thresh_image[:, :int(width/2)]
        img_right = thresh_image[:, int(width/2):]

        sum_left = np.sum(img_left)
        sum_right = np.sum(img_right)

        left_detect = sum_left/(255*(height*(width/2)))
        right_detect = sum_right/(255*(height*(width/2)))

        print("Sum left", left_detect)
        print("Sum_right", right_detect)

        if((left_detect > 0.1) and (left_detect > right_detect)):
            #TURN RIGHT LOGIC
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            cv.arrowedLine(np_image, (int(width*2/3), int(height/2)), (int(width*5/6), int(height/2)), (255,255,255), 9)

        elif((right_detect > 0.1) and (right_detect > left_detect)):
            #TURN LEFT LOGIC
            GPIO.output(18, GPIO.LOW)
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(16, GPIO.LOW)
            cv.arrowedLine(np_image, (int(width/3), int(height/2)), (int(width/6), int(height/2)), (255,255,255), 9)

        else:
            #FRONT LOGIC
            GPIO.output(18, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(16, GPIO.HIGH)
            cv.arrowedLine(np_image, (int(width/2), int(height/2)), (int(width/2), int(height/6)), (255,255,255), 9)



        #print("Middle distance:", depth_frame.get_distance(int(width/2), int(height/2)))

        #np_image = cv.circle(np_image, (int(width/2), int(height/2)), radius=1, color=(255,0,0), thickness=-1)
 

        cv.namedWindow("RealSense", cv.WINDOW_AUTOSIZE)
        cv.imshow("Depth Image", np_image)
        #cv.imshow("Threshold Image", thresh_image)
        #cv.imshow("Left", img_left)
        #cv.imshow("Right", img_right)
        key = cv.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv.destroyAllWindows()
            break
finally:
    pipeline.stop()

