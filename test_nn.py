import numpy as np
# from nn_tflearn import alexnet2
# from nn_inception import inception_v3
# from models import inception_v3
from model import formula_network
from screen import grab_screen, place_emulator
import cv2
import time
from config import IMG_WIDTH, IMG_HEIGHT, SCREEN_REGION, RESIZE_RATIO, training_file_name, testing_file_name, HOST, PORT
from util import thread_on_key
from getkeys import key_check
import http.server
import threading


WIDTH = IMG_WIDTH // RESIZE_RATIO
HEIGHT = IMG_HEIGHT // RESIZE_RATIO

# file_name = config.file_name
LR = 0.0005
# EPOCHS = 1
# MODEL_NAME = "f1-bot-{}-{}-{}.model".format("alexnet2", LR, EPOCHS)
MODEL_NAME = "models\\f1-bot-formula_network-0.0005-3.model\\f1-bot-formula_network-0.0005-3.model"

model = formula_network(width=WIDTH, height=HEIGHT, lr=LR, output=4)
model.load(MODEL_NAME)

inputs = []
connected = False


class HttpServerHandler(http.server.BaseHTTPRequestHandler):
	"""
	A simple HTTP server capable of handling GET and POST requests
	"""
	inputs = []

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

	def do_GET(self):
		self.protocol_version = 'HTTP/1.1'
		response = encoded_inputs()
		self._set_headers(response=response)
		self.wfile.write(response)

	# def do_POST(self):
	# 	# print('POST received\n')
	# 	self.send_response(200)
	# 	self.protocol_version = 'HTTP/1.1'
	# 	self.end_headers()
	# 	content_length = int(self.headers['Content-Length'])
	# 	set_inputs(self.rfile.read(content_length).decode('utf-8').replace('payload=', '').split("x"))
	# 	response = b'ok'
	# 	self.wfile.write(response)

	def log_message(self, format, *args):
		return


def set_connected():
	global connected
	if not connected:
		connected = True
		print("Emulator connected! Ready to record.")


def encoded_inputs():
	global inputs
	if len(inputs) < 4:
		return b"0x0x0.5x0.5"
	else:
		if int(round(inputs[0])) == 1:
			i = "Truex"
		else:
			i = "Falsex"
		if int(round(inputs[1])) == 1:
			i += "Truex"
		else:
			i += "Falsex"
		if inputs[2] > inputs[3]:
			i += str(-inputs[2])
		else:
			i += str(inputs[3])
		# i = str(int(round(inputs[0]))) + "x"
		# i += str(int(round(inputs[1]))) + "x"
		# i += str(inputs[2]) + "x"
		# i += str(inputs[3])
		# i += str((0 - input[2]) + input[3])
		return i.encode()


def test_nn():
	place_emulator()
	for i in range(0, 3):
		print("Taking control in", 3 - i, "...")
		time.sleep(1)

	paused = False

	print("- - - DRIVING - - -")

	while True:
		timestamp = time.time()
		if not paused:
			# screen = grab_screen(CROPPED_REGION)
			screen = cv2.resize(grab_screen(SCREEN_REGION), ((IMG_WIDTH // RESIZE_RATIO), (IMG_HEIGHT // RESIZE_RATIO)))
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

			# print("frame took {} seconds".format(time.time() - timestamp))

			# screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			# cv2.imshow("test", screen)
			# if cv2.waitKey(25) & 0xFF == ord("q"):
			# 	cv2.destroyAllWindows()

			prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]

			global inputs
			inputs = prediction

			# print("L:" + str(round(inputs[2], 8)) + " R:" + str(round(inputs[3], 8)))
			print(encoded_inputs())

		keys = key_check()
		if "P" in keys:
			if paused:
				paused = False
				print("Taking back control in 3...")
				time.sleep(1)
				print("Taking back control in 2...")
				time.sleep(1)
				print("Taking back control in 1...")
				time.sleep(1)
				print("- - - DRIVING RESUMED - - -")

			else:
				paused = True
				print("Network paused...")
				time.sleep(1)


def main():
	place_emulator()
	print("Starting HTTP Server")
	httpd = http.server.HTTPServer((HOST, PORT), HttpServerHandler)
	print("Running HTTP server at: {}:{}".format(httpd.server_address[0], httpd.server_address[1]))
	thread_http = threading.Thread(target=httpd.serve_forever, name="thread_http")
	thread_testing = threading.Thread(target=test_nn, name="thread_testing")

	thread_http.start()
	print("")
	print("Waiting for you to setup connection between emulator and http server in order to send inputs from the NN")
	print("Hold \'G\' on your keyboard to hand over control to the network")
	thread_control = threading.Thread(target=thread_on_key, name="thread_control",
									  args=("G", thread_testing))
	thread_control.start()


main()
