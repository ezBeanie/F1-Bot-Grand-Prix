import os
import time
import threading
import cv2
import numpy as np
import http.server

import config
from getkeys import key_check
from util import thread_on_key
from screen import grab_screen, place_emulator

IMG_WIDTH = config.IMG_WIDTH
IMG_HEIGHT = config.IMG_HEIGHT

SCREEN_POS_X = config.SCREEN_POS_X
SCREEN_POS_Y = config.SCREEN_POS_Y
SCREEN_REGION = (SCREEN_POS_X, SCREEN_POS_Y, IMG_WIDTH + SCREEN_POS_X, IMG_HEIGHT + SCREEN_POS_Y)

CROPPED_WIDTH = config.IMG_WIDTH
CROPPED_HEIGHT = IMG_HEIGHT - 100
CROPPED_POS_X = SCREEN_POS_X
CROPPED_POS_Y = SCREEN_POS_Y + 68
CROPPED_REGION = (CROPPED_POS_X, CROPPED_POS_Y, CROPPED_WIDTH + CROPPED_POS_X, CROPPED_HEIGHT + CROPPED_POS_Y)

INPUT_DATA_RATIO = config.INPUT_DATA_RATIO

HOST = config.HOST
PORT = config.PORT

paused = False
capture_entire_screen = False
connected = False
inputs = []


class HttpServerHandler(http.server.BaseHTTPRequestHandler):
	"""
	A simple HTTP server capable of handling GET and POST requests
	"""

	def _set_headers(self, response=None, connection=None):
		self.send_response(200)
		self.send_header('Content-Type', 'text/html; charset=utf-8')

		if response is not None:
			self.send_header('Content-Length', len(response))
		if connection is not None:
			self.send_header('Connection', connection)
		self.end_headers()

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		# print('POST received\n')
		self.send_response(200)
		self.protocol_version = 'HTTP/1.1'
		self.end_headers()
		content_length = int(self.headers['Content-Length'])
		set_inputs(self.rfile.read(content_length).decode('utf-8').replace('payload=', '').split("x"))
		set_connected()
		response = b'ok'
		self.wfile.write(response)

	def log_message(self, format, *args):
		return


def set_inputs(i):
	global inputs
	inputs = i

def set_connected():
	global connected
	if not connected:
		connected = True
		print("Emulator connected! Ready to record.")


def get_file_name(starting_value=1):
	while True:
		file_name = config.training_file_name.format(starting_value)

		if os.path.isfile(file_name):
			print("File", file_name, "already exists. Counting up.")
			starting_value += 1
		else:
			print("Data output:", file_name)
			return file_name, starting_value


def key_output(keys):
	output = [0, 0, 0, 0]
	if "W" in keys:
		output[0] = 1
	if "S" in keys:
		output[1] = 1
	if "A" in keys:
		output[2] = 1
	if "D" in keys:
		output[3] = 1

	return output


def record_data():
	name_and_position = get_file_name()
	file_name = name_and_position[0]
	starting_value = name_and_position[1]

	for i in range(0, 3):
		print("Recording data in", 3 - i, "...")
		time.sleep(1)

	training_data = []
	paused = False

	print("- - - RECORDING - - -")

	while True:
		# timestamp = time.time()
		if not paused:
			# if capture_entire_screen:
			# 	screen = grab_screen(SCREEN_REGION)
			# 	screen = cv2.resize(screen, (int(IMG_WIDTH / 4), int(IMG_HEIGHT / 4)))
			# else:
			# 	screen = grab_screen(CROPPED_REGION)
			# 	screen = cv2.resize(screen, (int(CROPPED_WIDTH / 4), int(CROPPED_HEIGHT / 4)))
			screen = grab_screen(CROPPED_REGION)
			screen = cv2.resize(screen, (int(CROPPED_WIDTH // INPUT_DATA_RATIO),
										 int(CROPPED_HEIGHT // INPUT_DATA_RATIO)))
			# screen = cv2.Canny(screen, 200, 300, True)
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			#

			# cv2.imshow("test", screen)
			# if cv2.waitKey(25) & 0xFF == ord("q"):
			#  	cv2.destroyAllWindows()
			keys = key_check()
			output = key_output(keys)
			print(output)
			# training_data.append([screen, screen_grey, screen_canny, output])
			# print(inputs)
			training_data.append([screen, output])
			# training_data.append([screen, inputs])
			# print(training_data)

			# print("look toop {} seconds".format(time.time() - timestamp))

			if len(training_data) % 100 == 0:
				print("{} captures made".format(len(training_data)))
				if len(training_data) % 1000 == 0:
					np.save(file_name, training_data)
					print("1000 captures saved at {}".format(file_name))
					training_data = []
					starting_value += 1
					file_name = config.training_file_name.format(starting_value)
		keys = key_check()
		if "P" in keys:
			if paused:
				paused = False
				print("Continue recording in 3...")
				time.sleep(1)
				print("Continue recording in 2...")
				time.sleep(1)
				print("Continue recording in 1...")
				time.sleep(1)
				print("- - - RECORDING RESUMED - - -")

			else:
				paused = True
				print("Recording paused...")
				time.sleep(1)


def main():
	place_emulator()
	print("Starting HTTP Server")
	httpd = http.server.HTTPServer((HOST, PORT), HttpServerHandler)
	print("Running HTTP server at: {}:{}".format(httpd.server_address[0], httpd.server_address[1]))
	thread_http = threading.Thread(target=httpd.serve_forever, name="thread_http")
	thread_recording = threading.Thread(target=record_data, name="thread_recording")
	thread_http.start()
	print("")
	print("Waiting for you to setup connection between emulator and http server in order to record input data")
	print("Hold \'G\' on your keyboard to start recording")
	thread_control = threading.Thread(target=thread_on_key, name="thread_control",
									  args=("G", thread_recording))
	thread_control.start()
	time.sleep(4)


main()
