from PIL import Image, ImageOps
import numpy as np
import cv2
import math


image_path = 'image.jpg'

image = Image.open(image_path)

class Deformer:

    def set_mesh(self, mesh):
        self.source_shape = mesh

    def getmesh(self, img):
        w, h = img.size
        self.target_rect = (0, 0, w, h)  # left top right bottom
        return [(self.target_rect, self.source_shape)]


selected_corner = None
rectangle_points = np.array([[50, 50], [200, 50], [200, 200], [50, 200]], dtype=np.int32)

def draw_rectangle(image):
    # Draw the rectangle
    cv2.polylines(image, [rectangle_points], True, (0, 255, 0), 2)

def click_event(event, x, y, flags, param):
    global selected_corner
    global rectangle_points

    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if the click is inside any of the rectangle corners
        for i, corner in enumerate(rectangle_points):
            if np.linalg.norm(np.array([x, y]) - corner) < 10:
                selected_corner = i
                break

    elif event == cv2.EVENT_MOUSEMOVE:
        if selected_corner is not None:
            # Update the position of the selected corner
            rectangle_points[selected_corner] = [x, y]

    elif event == cv2.EVENT_LBUTTONUP:
        selected_corner = None


def resize_maintain_aspect_ratio(image, target_size):
    global rectangle_points


    # Calculate the scaling factor for width and height
    width_ratio = target_size[0] / image.shape[1]
    height_ratio = target_size[1] / image.shape[0]

    # Choose the minimum scaling factor to maintain aspect ratio
    scaling_factor = min(width_ratio, height_ratio)

    # Calculate the new dimensions
    new_width = int(image.shape[1] * scaling_factor)
    new_height = int(image.shape[0] * scaling_factor)
    new_dimensions = (new_width, new_height)

    return cv2.resize(image, new_dimensions)


def resie_rect():
    # Calculate the scaling factor used during resizing
    scaling_factor_width = image.width / image_cv2.shape[1]
    scaling_factor_height = image.height / image_cv2.shape[0]

    # Map the rectangle points to the original PIL image dimensions
    rectangle_points_mapped = []
    for point in rectangle_points:
        x_mapped = int(point[0] * scaling_factor_width)
        y_mapped = int(point[1] * scaling_factor_height)
        rectangle_points_mapped.append([x_mapped, y_mapped])

    return rectangle_points_mapped

# Load the image
image_cv2 = cv2.imread(image_path) # Read the Image for cv2


# Load the image
image_cv2 = cv2.imread(image_path)
target_size = (700, 700)

image_cv2 = resize_maintain_aspect_ratio(image_cv2, target_size)

# Create a window and set the mouse callback function
cv2.namedWindow('"q" to quit "ENTER" to proceed')
cv2.setMouseCallback('"q" to quit "ENTER" to proceed', click_event)

while True:
    # Make a copy of the original image to draw on
    image_copy = image_cv2.copy()

    # Draw the rectangle on the image
    draw_rectangle(image_copy)

    # Display the image with the rectangle
    
    cv2.imshow('"q" to quit "ENTER" to proceed', image_copy)

    # Check for key press to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    
    if key == 13:
        #print(np.array(rectangle_points))
        break

cv2.destroyAllWindows()

rectangle_points = resie_rect()

print(rectangle_points)

rectangle_points_converted =[ rectangle_points[0][0], rectangle_points[0][1], rectangle_points[1][0], rectangle_points[1][1], rectangle_points[2][0], rectangle_points[2][1], rectangle_points[3][0], rectangle_points[3][1] ]

print(rectangle_points_converted)

distance_x = math.dist(rectangle_points[0], rectangle_points[1])
distance_y = math.dist(rectangle_points[1], rectangle_points[2])

a = math.gcd(int(distance_x), int(distance_y))

aspectx = int(distance_x // a)
aspecty = int(distance_y // a)


print(aspectx, aspecty)
# Create an instance of Deformer and set the mesh
deformer = Deformer()
deformer.set_mesh(mesh=rectangle_points_converted)

# Deform the image using the Deformer instance
deformed = ImageOps.deform(image, deformer, Image.BICUBIC)
deformed = deformed.rotate(270, expand=True)
deformed = deformed.transpose(Image.FLIP_LEFT_RIGHT)
#deformed = deformed.resize((aspectx, aspecty), Image.BICUBIC)
# Calculate the scaling factor
scaling_factor = image.height / aspecty

# Scale the width proportionally to maintain aspect ratio
new_width = int(aspectx * scaling_factor)

# Resize the image
deformed = deformed.resize((new_width, image.height), Image.BICUBIC)

deformed.show()
