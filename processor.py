import numpy as np
import cv2


class Processor:
    def load(self, path):
        return cv2.imread(path, 0)

    def gray(self, color_image):
        dimension = np.array(color_image).shape
        if len(dimension) == 2:
            return color_image
        return cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    def toActions(self, image):
        last_row = 0
        last_col = 0

        actions = []
        for col in range(len(image[0])):
            for row in range(len(image)):
                if image[row][col] < 0.5:
                    actions.append((row, col, last_row, last_col))
                    last_row = row
                    last_col = col
        return actions
