import cv2
import numpy as np
import time

import config
from getkeys import key_check

IMG_WIDTH = config.IMG_WIDTH
IMG_HEIGHT = config.IMG_HEIGHT


def region_of_interest(img):
	mask = np.zeros_like(img)
	# vertices = np.array([[
	# 	[0, IMG_HEIGHT * 590 / 888],
	# 	[0, IMG_HEIGHT * 200 / 888],
	# 	[IMG_WIDTH / 2, IMG_HEIGHT * 120 / 888],
	# 	[IMG_WIDTH, IMG_HEIGHT * 200 / 888],
	# 	[IMG_WIDTH, IMG_HEIGHT * 590 / 888],
	# 	[IMG_WIDTH / 2, IMG_HEIGHT * 510 / 888],
	# ]], np.int32)
	vertices = np.array([[
		[0, IMG_HEIGHT * 120 / 888],
		[IMG_WIDTH, IMG_HEIGHT * 120 / 888],
		[IMG_WIDTH, IMG_HEIGHT * 510 / 888],
		[0, IMG_HEIGHT * 510 / 888],
	]], np.int32)
	cv2.fillPoly(mask, vertices, 255)
	return cv2.bitwise_and(img, mask)


def process_img(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.Canny(img, 200, 300, True)
	img = region_of_interest(img)
	# img = cv2.GaussianBlur(img, (2, 2), 0)
	# lines = cv2.HoughLinesP(img, 1, np.pi / 180, 200, np.array([]), 100, 5)
	# draw_lines(img, lines)
	return img


def draw_lines(img, lines):
	try:
		for line in lines:
			coords = line[0]
			cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 3)
	except:
		pass


def keys_to_output(keys):
	# Left, Right, A, B
	# = steering left, steering right, accelerate, brake
	output = [0, 0, 0, 0]

	if 'A' in keys:
		output[0] = 1
	if 'D' in keys:
		output[1] = 1
	if 'W' in keys:
		output[2] = 1
	if 'S' in keys:
		output[3] = 1
	return output


def thread_on_key(key, thread):
	while True:
		keys = key_check()
		if key in keys:
			thread.start()
			break
		time.sleep(1)


def rgbfrombytes(byte_a, byte_b):
	byte_a = byte_a << 8
	value = byte_a | byte_b
	r = (value & 0xF800)
	r = (r >> 11)
	r = r / 31 * 255
	g = (value & 0x7C0)
	g = (g >> 6)
	g = g / 31 * 255590
	b = (value & 0x3E)
	b = (b >> 1)
	b = b / 31 * 255
	return [r, g, b]
