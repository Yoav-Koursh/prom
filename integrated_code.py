import cv2
import numpy as np
import image_cut
import moving_avg
import video_to_vector
import math
import matplotlib.pyplot as plt


R = 0.3 # distance from middle to each camera in meters
camera_angles = np.array([(1,1.9 )])
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
# videos = image_cut.image_cut('video.mp4', 30, 5)
cap = cv2.VideoCapture("testvid.mp4")
video = []
n = 0
while True:
    n += 1
    ret, frame = cap.read()
    if not ret:
        break  # No more frames -> exit loop
    if n % 100 == 0:
        print(n)
    video.append(frame)
object_locations = video_to_vector.image_to_vector(video, 0)
#for i in range(5):
#    object_locations.append(video_to_vector.image_to_vector(videos[i], i))
#object_locations_np = np.array(object_locations)
#directional_vectors = object_locations_np * np.tan(camera_angles)
#print("\n\ndirectional_vectors\n", directional_vectors)

xpoints = np.array([i[1] - (1920/2) for i in object_locations]+ [1920/2, 1920/2, -1920/2, -1920/2])

ypoints = np.array([-i[0] + (540) for i in object_locations]+ [-1080/2, 1080/2, 1080/2, -1080/2])


object_locations = np.array([np.array(p) for p in list(filter(lambda a: a != (0,0), object_locations))]) # np.delete(transpoded_object_location, np.array([0,0]))

transpoded_object_location = np.transpose(object_locations)

transposed_smooth_object_location = (moving_avg.moving_avg(transpoded_object_location[0],3),moving_avg.moving_avg(transpoded_object_location[1],3))
smooth_object_location = np.transpose(transposed_smooth_object_location)
smooth_object_location = (smooth_object_location - np.array([540, 1920/2 ]))*np.array([-1,1])
direction_vector = smooth_object_location * 2 / np.array ([540, 1920/2]) * np.tan(camera_angles[0]/2)
direction_vector_3d = np.array([[vector[1], vector[0],1 ]for vector in direction_vector])
print (direction_vector_3d)
plt.plot( xpoints, ypoints, 'o')
xavgpoints = np.array([i[1]  for i in smooth_object_location]+ [1920/2, 1920/2, -1920/2, -1920/2])
yavgpoints = np.array([i[0] for i in smooth_object_location]+ [-1080/2, 1080/2, 1080/2, -1080/2])
plt.plot( xavgpoints, yavgpoints, 'o')

plt.show()
cv2.waitKey(0)