import numpy as np
import cv2
import os
import time
from getkeys import key_check
from screen import grab_screen

file_name = "training_data.npy"
starting_value = 1
paused = False

accelerate = [1, 0, 0, 0, 0, 0, 0, 0, 0]
brake = [0, 1, 0, 0, 0, 0, 0, 0, 0]
left = [0, 0, 1, 0, 0, 0, 0, 0, 0]
right = [0, 0, 0, 1, 0, 0, 0, 0, 0]
acc_left = [0, 0, 0, 0, 1, 0, 0, 0, 0]
acc_right = [0, 0, 0, 0, 0, 1, 0, 0, 0]
brake_left = [0, 0, 0, 0, 0, 0, 1, 0, 0]
brake_right = [0, 0, 0, 0, 0, 0, 0, 1, 0]
no_action = [0, 0, 0, 0, 0, 0, 0, 0, 1]

while True:
	file_name = "training_data-{}.npy".format(starting_value)

	if os.path.isfile(file_name):
		print("File", file_name, "already exists. Counting up.")
		starting_value += 1
	else:
		print("Data output:", file_name)
	break


def key_output(keys):
	if "W" in keys:
		output = accelerate
	elif "S" in keys:
		output = brake
	elif "A" in keys:
		output = left
	elif "D" in keys:
		output = right
	elif "W" in keys and "A" in keys:
		output = acc_left
	elif "W" in keys and "D" in keys:
		output = acc_right
	elif "S" in keys and "A" in keys:
		output = brake_left
	elif "S" in keys and "D" in keys:
		output = brake_right
	else:
		output = no_action

	return output


def main(file_name=file_name, starting_value=starting_value):
	training_data = []

	for i in range(0, 5):
		print("Recording data in", 5 - i, "...")
		time.sleep(1)

	print("BEGIN RECORDING")

	time = time.time()


main(file_name, starting_value)
