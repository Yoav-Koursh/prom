
import cv2
import numpy as np
import border_grouping
import image_distort
import matplotlib.pyplot as plt


def find_edges(img):
    # Convert to graycsale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

    # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)  # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)  # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1,
                        ksize=5)  # Combined X and Y Sobel Edge Detection

    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)  # Canny Edge Detection
    cv2.imshow('edges', edges)
    edges_arr = np.array(edges)
    edges_arr = edges_arr // 255

    return edges_arr


def image_to_vector(frame1name,frame2name, camera_index):
    frame1 = cv2.imread(frame1name)
    frame2 = cv2.imread(frame2name)

    img1 = image_distort.correct_image(frame1, camera_index)  # fix image distortion
    img2 = image_distort.correct_image(frame2, camera_index)  # fix image distortion

    current_subtracted_frame = cv2.subtract(img1, img2)
    cv2.imshow('subtracted', current_subtracted_frame)
    edges_arr = find_edges(current_subtracted_frame)
    return border_grouping.find_object_locations(edges_arr)

print(image_to_vector('img1.jpg', 'img2.jpg', 0))

cv2.waitKey(0)

"""sub_img = cv2.subtract(cv2.imread("imtest1.jpg"), cv2.imread("imtest2.jpg"))
edges_img = find_edges(sub_img)
loc = border_grouping.find_object_locations(find_edges(sub_img))
x = [-1920 / 2, 1920 / 2, 1920 / 2, -1920 / 2, loc[1]]
y = [1080 / 2, 1080 / 2, -1080 / 2, -1080 / 2, -loc[0]]

# cv2.imshow("sub", sub_img)

plt.plot(x, y, 'o')
plt.show()
"""

