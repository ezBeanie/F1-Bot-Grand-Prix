import tflearn
from tflearn.layers.conv import conv_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization


def formula_network(width, height, lr, output=4, model_name="formula_network", device="gpu"):
	network = input_data(shape=[None, width, height, 1], name="input")
	network = conv_2d(incoming=network, nb_filter=50, filter_size=15, strides=5, activation="relu", name="conv-layer-1")
	network = local_response_normalization(incoming=network)
	network = conv_2d(incoming=network, nb_filter=100, filter_size=2, strides=1, activation="relu", name="conv-layer-2")
	network = local_response_normalization(incoming=network)
	network = conv_2d(incoming=network, nb_filter=200, filter_size=2, strides=1, activation="relu", name="conv-layer-2")
	network = local_response_normalization(incoming=network)
	network = fully_connected(incoming=network, n_units=3200, activation="relu")
	network = dropout(incoming=network, keep_prob=0.9)
	network = fully_connected(incoming=network, n_units=1600, activation="relu")
	network = dropout(incoming=network, keep_prob=0.9)
	network = fully_connected(incoming=network, n_units=800, activation="relu")
	network = dropout(incoming=network, keep_prob=0.9)
	network = fully_connected(incoming=network, n_units=output, activation="sigmoid")

	network = regression(incoming=network, optimizer="SGD", loss="mean_square", learning_rate=lr, name="targets")

	model = tflearn.DNN(network, max_checkpoints=0, tensorboard_verbose=0, tensorboard_dir="log")

	return model
