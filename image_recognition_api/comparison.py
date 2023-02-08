import cv2 as cv


def get_image_hash(path: str) -> str:
    image = cv.imread(path)
    resized = cv.resize(image, (8,8), interpolation = cv.INTER_AREA)
    gray_image = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
    threshold_image = cv.threshold(gray_image, gray_image.mean(), 255, 0)[1]


    _hash = ""
    for x in range(8):
        for y in range(8):
            val=threshold_image[x, y]
            if val == 255:
                _hash += '1'
            else:
                _hash += '0'

    return _hash


def compare_hash(hash1: str, hash2: str) -> int:
    count = 0
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            count += 1

    return count
