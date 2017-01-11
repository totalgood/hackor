from skimage import io
from skimage.transform import rescale
from numpy import shape
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from PIL import Image

# img_lst = io.imread('num.jpg', as_grey=True)
# plt.imshow(img_lst, cmap = cm.Greys_r)
# plt.show()



print('hi')

img = Image.open('num.jpg')

img.thumbnail((8,8))

a = np.asarray(img)

plt.imshow(img, cmap = cm.Greys_r, interpolation="nearest")
plt.show()

plt.imshow(img, cmap = cm.Greys_r, interpolation="bicubic")
plt.show()

plt.imshow(img, cmap = cm.Greys_r)
plt.show()