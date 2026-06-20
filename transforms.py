import numpy as np

def rotate_left(img):
    return np.rot90(img)

def rotate_right(img):
    return np.rot90(img, -1)

def flip_horizontal(img):
    return np.fliplr(img)

def flip_vertical(img):
    return np.flipud(img)

def crop(img, top, bottom, left, right):
    return img[top:bottom, left:right]