
import cv2
import numpy as np
from matplotlib.pyplot import imshow

import border_grouping
import image_distort
import matplotlib.pyplot as plt

import moving_avg

camera_angles = np.array([(1,1.9 ),(0.7549, 1.2042 ), (0.7242,1.3676), (0.7927, 1.48827),(0.488, 0.6342)])  #reinforced, HP, red, lenovo, basic



def find_edges(img,n=0):
    thresh = 50
    img_blur = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow(n, img_blur)
    # cv2.imshow(n, img_blur)
    # Sobel Edge Detection
    # sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)  # Sobel Edge Detection on the X axis
    # sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)  # Sobel Edge Detection on the Y axis
    # sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1,ksize=5)  # Combined X and Y Sobel Edge Detection

    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)  # Canny Edge Detection
    edges_arr = np.array(edges)
    # cv2.imshow(n, edges_arr)
    edges_arr = edges_arr // 255

    return edges_arr


def image_to_vector(cap, camera_index):
    object_locations =[]
    # Check if the video opened correctly
    # if not cap.isOpened():
    #    print("Error: Could not open video file.")
    #    exit()
    n = 1
    frame2 = cap[0]
    img2 = image_distort.correct_image(frame2, camera_index)
    while True:
        if n % 5 != 0:
            n += 1
            continue
        if n >= len(cap):
            break
        frame1 = cap[n]

        img1 = image_distort.correct_image(frame1, camera_index) #fix image distortion

        current_subtracted_frame = cv2.subtract(img1, img2)
        # if n ==20 or n==25:
        frame_name = f' camera {camera_index} frame {n}'
        cv2.imshow(frame_name, current_subtracted_frame)
        b, g, r = cv2.split(current_subtracted_frame)
        # cv2.imshow( str(n),b)
        # cv2.imshow(str(n), current_subtracted_frame)
        edges_arr = find_edges(b,str(n))
        # cv2.imshow( str(n)+'border',edges_arr)

        object_locations.append(border_grouping.find_object_locations(edges_arr))
        img2 = img1
        n += 1
    # Release resources
    # cap.release()
    # cv2.destroyAllWindows()
    return object_locations

"""sub_img = cv2.subtract(cv2.imread("imtest1.jpg"), cv2.imread("imtest2.jpg"))
edges_img = find_edges(sub_img)
loc = border_grouping.find_object_locations(find_edges(sub_img))
x = [-1920 / 2, 1920 / 2, 1920 / 2, -1920 / 2, loc[1]]
y = [1080 / 2, 1080 / 2, -1080 / 2, -1080 / 2, -loc[0]]

# cv2.imshow("sub", sub_img)

plt.plot(x, y, 'o')
plt.show()
"""

def find_direction_from_vid(video, camera_index):
    # video = []
    n = 0
    # while True:
    #     n += 1
    #     # ret, frame = cap.read()
    #     # if not ret:
    #     #     break  # No more frames -> exit loop
    #     # if n % 100 == 0:
    #     #     print(n)
    #     video.append(frame)
    object_locations = image_to_vector(video, camera_index)
    object_locations = np.array([np.array(p) for p in list(
        filter(lambda a: a != (0, 0), object_locations))])  # np.delete(transpoded_object_location, np.array([0,0]))
    transpoded_object_location = np.transpose(object_locations)
    transposed_smooth_object_location = (moving_avg.moving_avg(transpoded_object_location[0], 3), moving_avg.moving_avg(transpoded_object_location[1], 3))
    smooth_object_location = np.transpose(transposed_smooth_object_location)
    smooth_object_location = (smooth_object_location - np.array([540, 1920 / 2])) * np.array([-1, 1])
    direction_vector = smooth_object_location * 2 / np.array([540, 1920 / 2]) * np.tan(camera_angles[camera_index] / 2)
    # plt.plot(direction_vector[1], direction_vector[0], 'o')
    direction_vector_3d = np.array([[vector[1], vector[0], 1] for vector in direction_vector])
    return direction_vector_3d

    # viewing the data

    xpoints = np.array([i[1] - (1920 / 2) for i in object_locations] + [1920 / 2, 1920 / 2, -1920 / 2, -1920 / 2])
    ypoints = np.array([-i[0] + (540) for i in object_locations] + [-1080 / 2, 1080 / 2, 1080 / 2, -1080 / 2])
    plt.plot(xpoints, ypoints, 'o')

    xavgpoints = np.array([i[1] for i in smooth_object_location] + [1920 / 2, 1920 / 2, -1920 / 2, -1920 / 2])
    yavgpoints = np.array([i[0] for i in smooth_object_location] + [-1080 / 2, 1080 / 2, 1080 / 2, -1080 / 2])
    plt.plot(xavgpoints, yavgpoints, 'o')

# vid =cv2.VideoCapture('testvid3.mp4')
# find_direction_from_vid(vid, 0)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

