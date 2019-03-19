from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

import tflearn.datasets.oxflower17 as oxflower17
import config

HOST = config.HOST
PORT = config.PORT

IMG_WIDTH = config.IMG_WIDTH
IMG_HEIGHT = config.IMG_HEIGHT
SCREEN_POS_X = config.SCREEN_POS_X
SCREEN_POS_Y = config.SCREEN_POS_Y
SCREEN_REGION = (SCREEN_POS_X, SCREEN_POS_Y, IMG_WIDTH + SCREEN_POS_X, IMG_HEIGHT + SCREEN_POS_Y)

file_name = config.training_file_name

# X, Y = oxflower17.load_data(one_hot=True, resize_pics=(227, 227))


def alexnet2(width, height, lr, output):
	network = input_data(shape=[None, width, height, 1], name='input')
	network = conv_2d(network, 96, 11, strides=4, activation='relu')
	# network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = conv_2d(network, 256, 5, activation='relu')
	# network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = conv_2d(network, 384, 3, activation='relu')
	network = conv_2d(network, 384, 3, activation='relu')
	network = conv_2d(network, 256, 3, activation='relu')
	# network = max_pool_2d(network, 3, strides=2)
	network = conv_2d(network, 256, 5, activation='relu')
	# network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = conv_2d(network, 384, 3, activation='relu')
	network = conv_2d(network, 384, 3, activation='relu')
	network = conv_2d(network, 256, 3, activation='relu')
	network = max_pool_2d(network, 3, strides=2)
	network = local_response_normalization(network)
	network = fully_connected(network, 4096, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, 4096, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, 4096, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, 4096, activation='tanh')
	network = dropout(network, 0.5)
	network = fully_connected(network, output, activation='tanh')
	network = regression(network, optimizer='SGD',
						 loss='mean_square',
						 learning_rate=lr, name='targets')

	model = tflearn.DNN(network, checkpoint_path='models\\model_alexnet',
						max_checkpoints=1, tensorboard_verbose=2, tensorboard_dir='log')

	return model
