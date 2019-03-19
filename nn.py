import socket
import time
# import tflearn

import cv2
import numpy as np

import config
from screen import grab_screen, place_emulator
from util import process_img

HOST = config.HOST
PORT = config.PORT

IMG_WIDTH = config.IMG_WIDTH
IMG_HEIGHT = config.IMG_HEIGHT
SCREEN_POS_X = config.SCREEN_POS_X
SCREEN_POS_Y = config.SCREEN_POS_Y
SCREEN_REGION = (SCREEN_POS_X, SCREEN_POS_Y, IMG_WIDTH + SCREEN_POS_X, IMG_HEIGHT + SCREEN_POS_Y)

file_name = config.training_file_name

def test():
	screen = grab_screen(SCREEN_REGION)
	screen = np.array(screen, np.uint8)
	# screen = process_img(screen)
	cv2.imshow("test", screen)
	if cv2.waitKey(25) & 0xFF == ord("q"):
		cv2.destroyAllWindows()


# cv2.namedWindow("test", cv2.WINDOW_AUTOSIZE)
place_emulator()
while True:
	last_time = time.time()
	test()
	print("frametiem:", time.time() - last_time)
