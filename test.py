import cv2
import numpy as np
#from skimage import io, segmentation, color, measure
#from skimage import graph
#import matplotlib.pyplot as plt

def edge_detection(img1_path, img2_path):
    image1= cv2.imread('imtest1.JPG')
    image2= cv2.imread('imtest2.JPG')

    # Read the original image
    img = subtracted = cv2.subtract( image2, image1)

    # Convert to graycsale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)

    # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)  # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)  # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)  # Combined X and Y Sobel Edge Detection

    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)  # Canny Edge Detection

    edges_arr = np.array(edges)
    edges_arr = edges_arr // 255

    return edges_arr
