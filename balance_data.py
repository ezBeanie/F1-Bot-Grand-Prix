import numpy as np
import cv2
import os
from config import *
from random import randint

# training_file_name = config.training_file_name
# testing_file_name = config.testing_file_name

starting_value = 0
final_value = 1
# training_data = np.load(training_file_name.format(starting_value))
final_data = np.load(training_file_name.format(starting_value + 1))
done_batches = []


def shuffle_data(data):
	for x in range(len(data)):
		i = randint(0, len(data) - 1)
		j = randint(0, len(data) - 1)
		tmp_a = data[i]
		tmp_b = data[j]
		data[i] = tmp_b
		data[j] = tmp_a
	return data


while True:
	if os.path.isfile(training_file_name.format(starting_value + 1)):
		# training_data = np.append(training_data, np.load(training_file_name.format(starting_value)), 0)
		starting_value += 1
	# print(starting_value)
	else:
		break

# final_data = shuffle_data(final_data)
# np.save("data\\shuffled\\shuffled_data-{}.npy".format(final_value), final_data)

while True:
	r = randint(1, starting_value)
	while r in done_batches:
		r = randint(1, starting_value)
	# start = (r - 1) * 1000
	# end = (r * 1000)
	# final_data = shuffle_data(training_data[start:end:])
	final_data = shuffle_data(np.load(training_file_name.format(r)))
	np.save(testing_file_name.format(final_value), final_data)
	final_value += 1
	done_batches.append(r)
	if len(done_batches) == starting_value:
		break

# print(final_data)
# print(len(final_data))
# print(len(training_data))


# final_data = final_data[-1000:]
# done_list_items = []
# for x in range(len(training_data)):
# 	i = randint(0, len(training_data) - 1)
# 	while i in done_list_items:
# 		i = randint(0, len(training_data) - 1)
# 	done_list_items.append(i)
# 	final_data.append(training_data[i])
# 	training_data = np.delete(training_data, i, 0)
# 	print(len(training_data), len(final_data))
# df = pd.DataFrame(training_data)
# print(df.all)
# print(len(training_data))
# df = pd.DataFrame(final_data)
# print(df.all)
# print(len(final_data))

# for data in final_data:
# 	img = data[0]
# 	print(data[1])
# 	cv2.imshow("test", img)
# 	print(cv2.getWindowImageRect("test"))
# 	if cv2.waitKey(25) & 0xFF == ord("q"):
#  		cv2.destroyAllWindows()

i = 1
while True:
	if os.path.isfile(testing_file_name.format(i)):
		i += 1
	else:
		break
print("current latest final dataset is named final_data-{}".format(i))
label_number = input("enter a number for your final data set \"final_data-XX.npy\n")
np.save(testing_file_name.format(label_number), final_data)
print("final_data-{}.npy saved (location:{})".format(label_number, testing_file_name))

# test = np.load("data\\final_data.npy")
# print(len(test))
# df = pd.DataFrame(test)
# print(df)
# print(training_data[1])
# print(Counter(df[1].apply(str )))

# Code to replay training data
# starting_value = 1
# while True:
# 	training_data = np.load("data\\training_data-{}.npy".format(starting_value))
# 	for data in training_data:
# 		img = data[0]
# 		choice = data[1]
# 		cv2.imshow("test", img)
# 		print(choice)
# 		if cv2.waitKey(25) & 0xFF == ord("q"):
# 			cv2.destroyAllWindows()
# 	starting_value += 1
