import cv2
import numpy as np
from PIL import ImageGrab, Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
import matplotlib.pyplot as plt

def detector(image, template):

    image = np.asarray(image)
    template = np.asarray(template)

    w, h = template.shape[:2]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    # Apply template Matching
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    #plt.imshow(image[top_left[1]:bottom_right[1], top_left[0], bottom_right[0]])
    #plt.show()
    center = np.mean((top_left, bottom_right), axis=0)

    return center

def get_windows_logo(scr):
    square_size = 40
    scr = scr.crop((0, scr.size[1] - square_size, square_size, scr.size[1]))
    return scr

def read_screen_neg(img, box, threshold):
    im_crop = img.crop(box)
    #plt.imshow(im_crop)
    #plt.show()
    #print(im_crop.size)
    size_w, size_h = im_crop.size
    im_crop = im_crop.resize((int(size_w * 20), int(size_h * 20)), Image.ANTIALIAS)
    im_crop = np.asarray(im_crop.convert('L'))
    vect_func = np.vectorize(lambda x: x if x > threshold else 0)
    im_bw = vect_func(im_crop)
    #plt.imshow(im_bw)
    #plt.show()
    char = pytesseract.image_to_string(im_bw)
    return char

def multi_detector(img, template):
    img = np.asarray(img)
    template = np.asarray(template)
    template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    w, h = template.shape[:2]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    #for pt in zip(*loc[::-1]):
    #    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    #cv2.imwrite('img_aux/res.png', img)
    points = []
    for pt in zip(*loc[::-1]):
        points.append((pt[0] + w/2, pt[1] + h/2))
    return points