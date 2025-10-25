import sqlite3
import cv2
import numpy as np
import os
from math import sqrt, ceil, floor

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def get_winners_img(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(''' 
                SELECT image FROM winners 
                INNER JOIN prizes ON 
                winners.prize_id = prizes.prize_id
                WHERE user_id = ?
            ''', (user_id, ))
            return cur.fetchall()

def create_collage(image_paths):
    images = []
    for path in image_paths:
        image = cv2.imread(path)
        if image is not None:
            images.append(image)

    if not images:
        return None

    num_images = len(images)
    num_cols = int(sqrt(num_images))
    num_rows = ceil(num_images / num_cols)
    h, w = images[0].shape[:2]
    collage = np.zeros((num_rows * h, num_cols * w, 3), dtype=np.uint8)

    for i, image in enumerate(images):
        row = i // num_cols
        col = i % num_cols
        collage[row*h:(row+1)*h, col*w:(col+1)*w] = image
    return collage
