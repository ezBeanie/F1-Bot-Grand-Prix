import os

import numpy as np

from config import IMG_WIDTH, IMG_HEIGHT, RESIZE_RATIO, training_file_name, testing_file_name
import tflearn
# from models import otherception3
from model import formula_network

# testing_file_name = config.testing_file_name
# training_file_name = config.training_file_name

WIDTH = IMG_WIDTH // RESIZE_RATIO
HEIGHT = IMG_HEIGHT // RESIZE_RATIO
LR = 0.0005
EPOCHS = 3
model = formula_network(width=WIDTH, height=HEIGHT, lr=LR, output=4)
MODEL_NAME = f"f1-bot-formula_network-{LR}-{EPOCHS}.model"


def load_data():
	starting_value = 1
	data = np.load(training_file_name.format(starting_value))
	starting_value += 1

	while True:
		if os.path.isfile(training_file_name.format(starting_value)):
			data = np.append(data, np.load(training_file_name.format(starting_value)), 0)
			print(f"loading training data, so far {len(data)} entries have been loaded.")
			starting_value += 1
		else:
			return data
			break


# for e in range(EPOCHS):
# 	while True:
# 		if os.path.isfile(training_file_name.format(starting_value + 1)):
# 			starting_value += 1
# 		else:
# 			break
# 	i = 1
# 	for x in range(11):
# 		data = np.append(data, np.load("data\\shuffled\\shuffled_data-{}.npy".format(i)), 0)
# 	train = data[:-10500]
# 	test = data[-500:]
# 	X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 3)
# 	Y = [i[1] for i in train]
#
# 	test_X = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 3)
# 	test_Y = [i[1] for i in test]
#
# 	model.fit({"input": X}, {"targets": Y}, n_epoch=EPOCHS, validation_set=({"input": test_X}, {"targets": test_Y}),
# 			  snapshot_step=500, show_metric=True, run_id=MODEL_NAME, batch_size=16)
#
# 	model.save("models\\" + MODEL_NAME + "\\" + MODEL_NAME)
# 	print("model saved for epoch {} from shuffled_data-{}".format(i, i))
# data_flow.ArrayFlow(load_data())
training_data = load_data()
# training_data = np.load("data\\ready\\final_data-12.npy")
train = training_data
test = training_data[-3000:]
#
# print(WIDTH, HEIGHT)
#
X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
Y = [i[1] for i in train]

test_X = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
test_Y = [i[1] for i in test]

model.fit({"input": X}, {"targets": Y}, n_epoch=EPOCHS, validation_set=None, snapshot_step=2000, show_metric=True,
		  run_id=MODEL_NAME, batch_size=4)

model.save("models\\" + MODEL_NAME + "\\" + MODEL_NAME)
