import time

import cv2
import urllib.request
import numpy as np

from cameras.models import Camera
from detect import detect
from .yolo_parking import get_detected_objects


# Set the URL of the camera feed


def get_camera_frame(camera, intruders=False):
    camera_url = camera.url

    # Open the video stream
    stream = urllib.request.urlopen(camera_url)

    # Initialize an empty byte buffer
    buffer = bytes()

    # Flag to indicate if the first frame has been captured
    first_frame_captured = False

    # Loop to receive and process the video stream frames
    while True:
        # Read the next chunk of data
        chunk = stream.read(1024)

        # Break the loop if no data is received
        if not chunk:
            break

        # Append the chunk to the buffer
        buffer += chunk

        # Check if the buffer contains a complete JPEG image
        a = buffer.find(b'\xff\xd8')
        b = buffer.find(b'\xff\xd9')
        if a != -1 and b != -1:
            # Extract the JPEG image from the buffer
            jpeg_data = buffer[a:b + 2]

            # Decode the JPEG image using OpenCV
            frame = cv2.imdecode(np.frombuffer(jpeg_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Pass the frame to the show_camera_with_mask function

            # Break the loop after capturing the first frame
            break

    # Release the video stream and close the OpenCV windows
    stream.close()
    cv2.destroyAllWindows()

    show_camera_with_mask(camera, frame, intruders)


def show_camera_with_mask(camera, frame, intruders):
    # Resize the frame to match the camera's height while maintaining the aspect ratio
    polygons = camera.p_mask if intruders is False else camera.v_mask
    desired_height = int(camera.height)
    aspect_ratio = desired_height / frame.shape[0]
    desired_width = int(frame.shape[1] * aspect_ratio)
    resized_frame = cv2.resize(frame, (desired_width, desired_height))

    # Create a blank canvas with the same size as the camera
    canvas = np.zeros((int(camera.height), int(camera.width), 3), dtype=np.uint8)

    # Calculate the position to center the resized frame on the canvas
    x_offset = (int(camera.width) - resized_frame.shape[1]) // 2
    y_offset = 0  # Assuming the image should be aligned to the top

    # Place the resized frame on the canvas
    canvas[y_offset:y_offset + resized_frame.shape[0], x_offset:x_offset + resized_frame.shape[1]] = resized_frame

    # Create a black mask image
    mask = np.zeros_like(canvas)

    # Draw each polygon on the mask
    for polygon in polygons:
        # Convert the polygon coordinates to NumPy array
        polygon_pts = np.array([[point['x'], point['y']] for point in polygon], dtype=np.int32)
        # Draw the polygon on the mask
        cv2.fillPoly(mask, [polygon_pts], (255, 255, 255))

    # Apply the mask to the canvas
    result = cv2.bitwise_and(canvas, mask)
    # cv2.imshow(f'Image with Polygon {intruders}', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    detections = detect(image=result)
    total_vehicles = sum([1 for i in detections if i.get('class') in ['car', 'bus', 'truck']])
    print(intruders, total_vehicles)
    if intruders is False:
        camera.current_cap = total_vehicles
        if camera.current_cap > camera.max_cap:
            camera.max_cap = camera.current_cap
    else:
        camera.intruders_count = total_vehicles
    camera.save()
    print('Done!')


def get_all_cameras():
    for i in range(10):
        for camera in Camera.objects.all():
            # print(camera.name)
            # continue
            try:
                get_camera_frame(camera)
                get_camera_frame(camera, intruders=True)
            except Exception as e:
                print('error processing camera: %s %s' % (camera.name, e))
        time.sleep(2)
