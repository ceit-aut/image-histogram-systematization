from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from reader import read_image_file
from utils import rgb2gray


def transform_cell(c_sum, width, height, color_levels):  # the transform function
    return round(((color_levels - 1) * c_sum) / (width * height))


if __name__ == "__main__":
    path = "assets/image.png"  # input("[Enter the file path] > ")
    pix, w, h = read_image_file(path)

    print(f'Image read: {w}x{h}')

    pix = rgb2gray(pix)

    histogram = {}
    counter = 0

    for row in pix:
        for element in row:
            if element in histogram.keys():
                histogram[element]["intensity"] = histogram[element]["intensity"] + 1
            else:
                histogram[element] = {}
                histogram[element]["intensity"] = 1
                histogram[element]["sum"] = 0
                histogram[element]["normalized_sum"] = 0

        counter = counter + 1

    print(f'Histogram validation: {len(pix) == counter}')

    keys = sorted(histogram.keys())

    for index in range(len(keys)):
        current = keys[index]
        if index == 0:
            histogram[current]["sum"] = histogram[current]["intensity"]
        else:
            histogram[current]["sum"] = histogram[current]["intensity"] + histogram[keys[index-1]]["sum"]

    total = len(keys)
    for key in keys:  # transform each of the colors
        histogram[key]["normalized_sum"] = transform_cell(histogram[key]["sum"], w, h, total)

    newPix = []
    for row in range(h):  # apply the transformation
        temp = []
        for col in range(w):
            key = pix[row][col]
            element = histogram.get(key)
            temp.append(element["normalized_sum"])
        newPix.append(temp)

    img = Image.fromarray(np.asarray(newPix))
    img.show()

    f, plt_array = plt.subplots(2)
    plt_array[0].stem(keys, [histogram[key]["intensity"] for key in keys])
    plt_array[0].set_title("Intensity of colors")
    plt_array[0].set_xlabel("Colors")
    plt_array[0].set_ylabel("Intensity")

    plt_array[1].stem(keys, [histogram[key]["sum"] for key in keys])
    plt_array[1].set_title("Cumulative sum of colors")
    plt_array[1].set_xlabel("Colors")
    plt_array[1].set_ylabel("Cumulative sum")

    plt.subplot_tool()
    plt.show()
