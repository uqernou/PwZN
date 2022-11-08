import numpy
import random

import numpy as np
from PIL import Image, ImageDraw


def get_energy_neighbors(spin, arr, xi, yi, arr_len):
    max_xi = xi
    max_yi = yi
    if xi - 1 == arr_len:
        max_xi = 0
    if yi - 1 == arr_len:
        max_yi = 0
    return (spin * arr[xi - 1][yi] +
                  spin * arr[xi][max_yi] +
                  spin * arr[max_xi][yi] +
                  spin * arr[xi][yi - 1])


def check_probability(B, dE):
    if random.uniform(0, 1) < numpy.exp(-B * dE):
        return 1


def sum_spin(arr):
    return np.sum(arr)


def draw_mesh(arr, filename, n, imgs):
    width = 1000  # 1920
    height = 1000  # 1024
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            scaled_width = width / n
            scaled_height = height / n
            scaled_x0 = i * scaled_width
            scaled_y0 = j * scaled_height
            scaled_x1 = scaled_x0 + scaled_width
            scaled_y1 = scaled_y0 + scaled_height
            if arr[i][j] == -1:
                draw.rectangle((scaled_x0, scaled_y0, scaled_x1, scaled_y1), (0, 0, 0))
            else:
                draw.rectangle((scaled_x0, scaled_y0, scaled_x1, scaled_y1), (255, 255, 255))
    if filename != 'none':
        img.save(filename)
    imgs.append(img)


def create_file_name(filename, step):
    if filename != 'none':
        return filename + str(step) + '.png'
    return 'none'


def save_gif(filename, arr):
    arr[0].save(filename,
                save_all=True,
                append_images=arr[1:],
                optimize=False,
                duration=250,
                loop=0)


def save_text_file(filename, arr):
    file = open(filename, "w")
    for i in range(len(arr)):
        file.write(str(arr[i]) + "\t" + str(i) + "\n")
    file.close()
