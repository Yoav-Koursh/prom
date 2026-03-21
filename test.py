import cv2
image1= cv2.imread('imtest1.JPG')
image2= cv2.imread('imtest2.JPG')

image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
subtracted = cv2.subtract( image2, image1)
# to convert to numpy use imread ('image' mode= 'RGB')
cv2.imshow('image', subtracted)

cv2.waitKey(0)
cv2.destroyAllWindows()