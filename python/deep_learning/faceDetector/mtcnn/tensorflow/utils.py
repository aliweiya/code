import numpy as np

from PIL import Image

def show_image(img):
   img = Image.fromarray((img * 128+127.5).astype(np.uint8))
   img.show()