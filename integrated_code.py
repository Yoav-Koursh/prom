import cv2
import numpy as np
import image_cut
import video_to_vector
import math
R = 0.3 # distance from middle to each camera in meters
camera_angles = np.array([[math.pi * 95 /180, math.pi * 95 /180, math.pi * 95 /180, math.pi * 95 /180, math.pi * 95 /180]])
camera_locations = [
    # Camera 1 (top)
    np.array((0, R, 0)),

    # Camera 2
    np.array((R * math.cos(0.1 * math.pi), R * math.sin(0.1 * math.pi), 0)),

    # Camera 3
    np.array((R * math.cos(0.5 * math.pi), R * math.sin(0.5 * math.pi), 0)),

    # Camera 4
    np.array((R * math.cos(0.9 * math.pi), R * math.sin(0.9 * math.pi), 0)),

    # Camera 5
    np.array((R * math.cos(1.3 * math.pi), R * math.sin(1.3 * math.pi), 0)),
]
videos = image_cut.image_cut('video.mp4', 30, 5)
object_locations = []
for i in range(5):
    object_locations.append(video_to_vector.image_to_vector(videos[i], i))
object_locations_np = np.array(object_locations)
directinal_vectors = object_locations_np * np.tan(camera_angles)
