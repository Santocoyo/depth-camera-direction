import pyrealsense2 as rs
import cv2 as cv
import numpy as np

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
        #aligned_frames = align.process(frames)
        #aligned_depth_frame = aligned_frames.get_depth_frame()
        #color_frame = aligned_frames.get_color_frame()

        #Get depth data
        depth_frame = frames.get_depth_frame()
        #zDepth = depth_frame.get_distance(int(x), int(y))

        if not depth_frame: continue
        #depth_data = depth.as_frame().get_data()
        #np_image = np.asanyarray(depth_data)
        #depth_image = np.asanyarray(aligned_depth_frame.get_data())
        #color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        #Applying color scale
        #np_image = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.3), cv.COLORMAP_JET)
        np_image = cv.convertScaleAbs(depth_image, alpha = 0.3)
        np_image = -np_image

        ret, thresh_image = cv.threshold(np_image, 127, 255, cv.THRESH_BINARY)


        #Getting parameters
        width = depth_frame.get_width()
        height = depth_frame.get_height()

        #for x in range(width):
            #for y in range(height):
                #print(x, y)
                #zDepth = depth_frame.get_distance(int(x), int(y))
                #if(0.1 < zDepth < 0.3):
                    #np_image = cv.circle(np_image, (x, y), radius=5, color=(255,0,0), thickness=-1)


        #grey_color = 153
        #depth_image_3d = np.dstack((depth_image, depth_image, depth_image))
        #bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, depth_image_3d)
        #images = np.hstack((np_image, bg_removed, depth_colormap))

        #Show output

        #print("np_shape:", np_image.shape)
        print("Middle distance:", depth_frame.get_distance(int(width/2), int(height/2)))

        np_image = cv.circle(np_image, (int(width/2), int(height/2)), radius=1, color=(255,0,0), thickness=-1)
        cv.namedWindow("RealSense", cv.WINDOW_AUTOSIZE)
        cv.imshow("Depth Image", np_image)
        cv.imshow("Threshold Image", thresh_image)
        key = cv.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv.destroyAllWindows()
            break
finally:
    pipeline.stop()

