# Source - https://stackoverflow.com/a/70125364
# Posted by manaclan, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-21, License - CC BY-SA 4.0



"""img = cv2.imread('imtest1.JPG')
H,W = img.shape[:2]
cv2.waitKey(0)
cropped = img[0:H//2, 0:W//2]
#cv2.imshow('image',image)
cv2.imshow('image',img)
cv2.imshow('cropped',cropped)
cv2.waitKey(0)

#cv2.imwrite('res.jpg',new_img)
#print(image.shape, new_img.shape)
input()"""

import cv2
def image_cut(video, fps_jump):
    for i in range(fps_jump):
        ret, frame = video.read()
    if frame is None:
        return None, video
    H, W = frame.shape[:2]
    cut_h, cut_w = H // 3, W // 3
    return [frame[:, cut_w*i:cut_w*(i+1)] for i in range(3)], video

