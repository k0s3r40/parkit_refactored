import cv2
import numpy as np

# Input polygon coordinates
polygon = [{'x': 525, 'y': 719.609375}, {'x': 760, 'y': 650.609375}, {'x': 794, 'y': 755.609375},
            {'x': 520, 'y': 764.609375}, {'x': 481, 'y': 735.609375}, {'x': 481, 'y': 735.609375},
            {'x': 525, 'y': 719.609375}]

# Load the image
image_path = '/tmp/ff.png'
image = cv2.imread(image_path)

# Resize the image while maintaining the aspect ratio
desired_height = 800
aspect_ratio = desired_height / image.shape[0]
desired_width = int(image.shape[1] * aspect_ratio)
resized_image = cv2.resize(image, (desired_width, desired_height))

# Create a black mask image
mask = np.zeros_like(resized_image)

# Convert the polygon coordinates to NumPy array
polygon_pts = np.array([[point['x'], point['y']] for point in polygon], dtype=np.int32)

# Draw the polygon on the mask
cv2.fillPoly(mask, [polygon_pts], (255, 255, 255))

# Apply the mask to the resized image
result = cv2.bitwise_and(resized_image, mask)

# Display the result
cv2.imshow('Image with Polygon', result)
cv2.waitKey(0)
cv2.destroyAllWindows()