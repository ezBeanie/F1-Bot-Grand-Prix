# coordinates and dimensions of the emulator window
WINDOW_POS_X = 1912
WINDOW_POS_Y = 0
WINDOW_WIDTH = 946
WINDOW_HEIGHT = 771

# dimensions of the image captured
IMG_WIDTH = 800
IMG_HEIGHT = 600

# the ratio by which IMG_WIDHT and IMG_HEIGHT are divided for our data
RESIZE_RATIO = 4

# coordinates of capture
SCREEN_POS_X = WINDOW_POS_X + 12
SCREEN_POS_Y = WINDOW_POS_Y + 54 + 50

# tuple defining the screen region
SCREEN_REGION = (SCREEN_POS_X, SCREEN_POS_Y, IMG_WIDTH + SCREEN_POS_X, IMG_HEIGHT + SCREEN_POS_Y)

# file names for all training data to be recorded or used for training
training_file_name = "data\\raw\\training_data-{}.npy"
testing_file_name = "data\\ready\\final_data-{}.npy"

# host ip and port for receiving controller inputs when recording training data
# aswell as sending controller inputs when testing
HOST = "127.0.0.1"
PORT = 8000
