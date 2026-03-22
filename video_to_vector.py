import cv2
import numpy as np
import border_grouping
import image_distort
def image_to_vector(cap, camera_index):
    object_locations =[]
    # Check if the video opened correctly
    if not cap.isOpened():
        print("Error: Could not open video file.")
        exit()
    n = 1
    ret, frame2 = cap.read()
    img2 = image_distort.correct_image(frame2, camera_index)
    while True:
        n += 1
        ret, frame1 = cap.read()
        if not ret:
            break   # No more frames -> exit loop

        img1 = image_distort.correct_image(frame1, camera_index) #fix image distortion

        current_subtracted_frame = cv2.subtract(img1, img2)
        # Convert to graycsale
        img_gray = cv2.cvtColor(current_subtracted_frame, cv2.COLOR_BGR2GRAY)

        # Blur the image for better edge detection
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)

        # Sobel Edge Detection
        sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)  # Sobel Edge Detection on the X axis
        sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)  # Sobel Edge Detection on the Y axis
        sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1,
                            ksize=5)  # Combined X and Y Sobel Edge Detection

        # Canny Edge Detection
        edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)  # Canny Edge Detection

        edges_arr = np.array(edges)
        edges_arr = edges_arr // 255

        object_locations.append( border_grouping.find_object_locations(edges_arr))


        img2 = img1
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    return object_locations