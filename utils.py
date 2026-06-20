from PIL import Image
import numpy as np


def load_image(path):
    img = Image.open(path)
    img = img.convert("RGB")
    img_array = np.array(img)
    return img_array


def save_image(image_array, path):
    img = Image.fromarray(image_array.astype(np.uint8))
    img.save(path)


def clamp(value):
    return max(0, min(255, value))


def clamp_array(image_array):
    return np.clip(image_array, 0, 255)