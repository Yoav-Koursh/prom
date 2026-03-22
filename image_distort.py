import cv2
import numpy as np

# --- 1. CAMERA MATRICES (3x3) ---

# Reinforced Camera
reinforced_camera_matrix = np.array([
    [1100.96940, 0.0, 979.155383],
    [0.0, 1092.54843, 530.096336],
    [0.0, 0.0, 1.0]
], dtype=np.float32)

# HP Webcam
hp_webcam_matrix = np.array([
    [995.23136, 0.0, 636.73657],
    [0.0, 992.75340, 373.53640],
    [0.0, 0.0, 1.0]
], dtype=np.float32)

# Red Camera
red_camera_matrix = np.array([
    [1533.25269, 0.0, 858.00021],
    [0.0, 1527.36391, 574.70216],
    [0.0, 0.0, 1.0]
], dtype=np.float32)

# Lenovo Camera
lenovo_camera_matrix = np.array([
    [1000.62216, 0.0, 932.34245],
    [0.0, 1002.47183, 596.58242],
    [0.0, 0.0, 1.0]
], dtype=np.float32)

# Basic Camera
basic_camera_matrix = np.array([
    [1028.73419, 0.0, 352.14599],
    [0.0, 1002.09197, 245.54864],
    [0.0, 0.0, 1.0]
], dtype=np.float32)


# --- 2. DISTORTION COEFFICIENTS (k1, k2, p1, p2, k3) ---

reinforced_camera_distance = np.array([-0.405105, 0.304864, 0.001144, -0.000151, -0.018686], dtype=np.float32)

hp_webcam_distance = np.array([0.024481, -0.107593, 0.001562, -0.002140, 0.019695], dtype=np.float32)

red_camera_distance = np.array([-0.440055, 0.328779, -0.004595, 0.000406, -0.122848], dtype=np.float32)

lenovo_camera_distance = np.array([-0.029972, 0.062954, -0.002643, -0.002080, -0.144175], dtype=np.float32)

basic_camera_distance = np.array([-0.030747, -1.391272, -0.001657, -0.009011, 6.190163], dtype=np.float32)


# --- 3. PROCESS THE IMAGE ---

img = cv2.imread('distorted_image.JPG')

if img is None:
    print("Error: Could not load image. Check the file name.")
else:
    # Example using Reinforced Camera - swap these variables to test other cameras
    new_img = cv2.undistort(img, reinforced_camera_matrix, reinforced_camera_distance)
    cv2.imshow('distorted', img)
    cv2.imshow('Undistorted', new_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()