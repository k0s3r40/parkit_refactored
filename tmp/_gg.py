import cv2
import urllib.request
import numpy as np

from cameras.models import Camera


# Set the URL of the camera feed
camera = Camera.objects.last()

def get_camera_frame(camera):

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
            jpeg_data = buffer[a:b+2]

            # Decode the JPEG image using OpenCV
            frame = cv2.imdecode(np.frombuffer(jpeg_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Save the first frame as an image
            if not first_frame_captured:
                cv2.imwrite("/tmp/ff.png", frame)
                print("First frame captured and saved.")
                first_frame_captured = True

            # Break the loop after capturing the first frame
            break

    # Release the video stream and close the OpenCV windows
    stream.close()
    cv2.destroyAllWindows()


def show_camera_with_mask(camera):
    # Input polygon coordinates
    polygons = camera.p_mask

    # Load the image
    image_path = '/tmp/ff.png'
    image = cv2.imread(image_path)

    # Resize the image to match the camera's height while maintaining the aspect ratio
    desired_height = int(camera.height)
    aspect_ratio = desired_height / image.shape[0]
    desired_width = int(image.shape[1] * aspect_ratio)
    resized_image = cv2.resize(image, (desired_width, desired_height))

    # Create a blank canvas with the same size as the camera
    canvas = np.zeros((int(camera.height), int(camera.width), 3), dtype=np.uint8)

    # Calculate the position to center the resized image on the canvas
    x_offset = (int(camera.width) - resized_image.shape[1]) // 2
    y_offset = 0  # Assuming the image should be aligned to the top

    # Place the resized image on the canvas
    canvas[y_offset:y_offset + resized_image.shape[0], x_offset:x_offset + resized_image.shape[1]] = resized_image

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

    # Display the result
    cv2.imshow('Image with Polygon', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


"""
usage

from tmp.gg import get_camera_frame, show_camera_with_mask
from cameras.models import Camera
camera = Camera.objects.last()
get_camera_frame(camera)
show_camera_with_mask(camera)

"""