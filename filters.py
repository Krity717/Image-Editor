import numpy as np

def grayscale(img):
    gray = np.mean(img, axis=2)
    gray = np.stack((gray, gray, gray), axis=2)

    return gray.astype(np.uint8)

def brighten(img, value=5):
    bright = img + value

    bright = np.clip(bright, 0, 255)

    return bright.astype(np.uint8)

def darken(img, value=20):
    dark = img.astype(np.int32) - value

    dark = np.clip(dark, 0, 255)

    return dark.astype(np.uint8)

def contrast(img, factor=1.2):
    adjusted = (img - 128) * factor + 128

    adjusted = np.clip(adjusted, 0, 255)

    return adjusted.astype(np.uint8)

def invert(img):
    return 255 - img   

def red_filter(img):
    red_img = img.copy()

    red_img[:, :, 1] = 0   # remove Green
    red_img[:, :, 2] = 0   # remove Blue

    return red_img    