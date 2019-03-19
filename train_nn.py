import os

import numpy as np

import config
import tflearn
from models import otherception3

testing_file_name = config.testing_file_name
training_file_name = config.training_file_name

WIDTH = config.IMG_WIDTH // config.INPUT_DATA_RATIO
HEIGHT = (config.IMG_HEIGHT - 100) // config.INPUT_DATA_RATIO
LR = 0.01
EPOCHS = 2
MODEL_NAME = "f1-bot-{}-{}-{}.model".format("otherception3", LR, EPOCHS)
starting_value = 1


def load_data():
	starting_value = 1
	data = np.load(training_file_name.format(starting_value))
	starting_value += 1

	while True:
		if os.path.isfile(training_file_name.format(starting_value)):
			data = np.append(data, np.load("data\\\shuffled\\shuffled_data-{}.npy".format(starting_value)), 0)
			starting_value += 1
		else:
			return data
			break


model = otherception3(WIDTH, HEIGHT, LR, 4, model_name=MODEL_NAME)

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
train = training_data[:-3000]
test = training_data[-3000:]
#
# print(WIDTH, HEIGHT)
#
X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
Y = [i[1] for i in train]

test_X = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
test_Y = [i[1] for i in test]

model.fit({"input": X}, {"targets": Y}, n_epoch=EPOCHS, validation_set=({"input": test_X}, {"targets": test_Y}),
		  snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

model.save("models\\" + MODEL_NAME + "\\" + MODEL_NAME)
