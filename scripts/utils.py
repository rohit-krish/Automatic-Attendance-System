import cv2
import numpy as np
import time


class GetFPS:
    def __init__(self) -> None:
        self.prev_time = 0
        self.curr_time = 0

    def get(self):
        self.curr_time = time.time()
        fps = 1 / (self.curr_time - self.prev_time)
        self.prev_time = self.curr_time
        return int(fps)

    def draw_in_img(self, img, scale=1):
        cv2.rectangle(
            img, (0, 0), (int(200 * scale), int(50 * scale)), (100, 46, 21), cv2.FILLED
        )
        cv2.putText(
            img,
            f"FPS: {self.get()}",
            (int(10 * scale), int(40 * scale)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5 * scale,
            (255, 255, 255),
            int(2 * scale),
        )
        return img


def _resize_and_fill_gaps(matrix, scale, label_height):
    # height and width of the first image
    height, width, *_ = matrix[0][0].shape
    height = int(height * scale)
    width = int(width * scale)

    n_rows = len(matrix)
    n_cols = 0

    for row in matrix:
        if len(row) > n_cols:
            n_cols = len(row)

    result = np.zeros((n_rows, n_cols, height + label_height, width, 3), dtype=np.uint8)

    for r_idx, row in enumerate(matrix):
        for c_idx, img in enumerate(row):
            img = np.squeeze(img)
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            img = cv2.resize(img, (width, height))
            text_place = np.zeros((label_height, width, 3))

            result[r_idx, c_idx] = np.vstack((img, text_place))

    return result


def stackIt(img_matrix, label_matrix=None, img_scale=1, label_height=30, **kwargs):
    label_height = 0 if label_matrix == None else label_height
    img_matrix = _resize_and_fill_gaps(img_matrix, img_scale, label_height)

    # putting the labels in each images
    if label_matrix:
        for img_row, label_row in zip(img_matrix, label_matrix):
            for image, label in zip(img_row, label_row):
                h, *_ = image.shape
                cv2.putText(image, label, (10, h - 10), **kwargs)

    row_images = []
    for row in img_matrix:
        row_images.append(np.hstack(tuple([*row])))

    return np.vstack(tuple([*row_images]))
