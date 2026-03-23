
import cv2
import numpy as np
from matplotlib.pyplot import imshow

import border_grouping
import image_distort
import matplotlib.pyplot as plt


def find_edges(img,n=0):
    # Convert to graycsale
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = img
    # Blur the image for better edge detection
    # img_blur = cv2.GaussianBlur(img_gray, (1, 1), 0)
    thresh = 50
    img_blur = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)[1]
    if n=='40':
        cv2.imshow('bw', img_blur)
        cv2.waitKey()
    # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)  # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)  # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1,
                        ksize=5)  # Combined X and Y Sobel Edge Detection

    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)  # Canny Edge Detection
    if n == '40':
        cv2.imshow(n, edges)
    edges_arr = np.array(edges)

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
        b, g, r = cv2.split(current_subtracted_frame)
        # cv2.imshow(str(n), current_subtracted_frame)
        if n == 40:
            cv2.imshow('aaa', r)
        edges_arr = find_edges(r,str(n))
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

