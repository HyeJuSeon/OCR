import cv2
import json
import os
from tqdm import tqdm
import numpy as np
import shutil
import random
from google.colab.patches import cv2_imshow
from scipy.ndimage.filters import median_filter




blurring_mask1 = np.array([[1 / 9, 1 / 9, 1 / 9], 
                           [1 / 9, 1 / 9, 1 / 9], 
                           [1 / 9, 1 / 9, 1 / 9]]) 

blurring_mask2 = np.array([[1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25], 
                           [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
                           [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25], 
                           [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25], 
                           [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25]]) 

smoothing_mask = np.array([[1 / 16, 1 / 8, 1 / 16],
                           [1 / 8, 1 / 4, 1 / 8], 
                           [1 / 16, 1 / 8, 1 / 16]]) 

sharpening_mask1 = np.array([[-1, -1, -1], 
                             [-1, 9, -1], 
                             [-1, -1, -1]]) 

sharpening_mask2 = np.array([[0, -1, 0], 
                             [-1, 5, -1], 
                             [0, -1, 0]]) 
 
##unsharp masking
def unsharp(image,sigma,strength):

  image_mf=median_filter(image,sigma)

  lap=cv2.Laplacian(image_mf,cv2.CV_64F)

  sharp=image-strength*lap

  sharp[sharp>255]=255
  sharp[sharp<0]=0

  return sharp




 






base_dir = 'D:/data'

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        img_array = np.fromfile(filename, dtype)
        return cv2.imdecode(img_array, flags)
    except Exception as e:
        print(e)
        return None

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
                return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
  path_origin=f'{base_dir}/data/train'
  print(path_origin)
  path_unsharp=f'{base_dir}/unsharp_data/train'
  files=os.listdir(path_origin)
  for file in tqdm(files):
    img= imread(f'{path_origin}/{file}', cv2.IMREAD_GRAYSCALE)
    bebe=unsharp(img,5,0.8)
    imwrite(f'{path_unsharp}/{file}',bebe)

