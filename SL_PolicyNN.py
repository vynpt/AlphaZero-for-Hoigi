from Main import*
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam

from sklearn.model_selection import train_test_split

"""
# datasets are lists of 18 x 9x9x3 matrices valued 0 or 1
# 0 = empty, 1 = present on board
# each matrix represent an instance of the board position
# 18 = 9 types of white pieces + 9 types of black pieces
# 9x9x3 is the size of board
"""
# To Do: remove duplicates
WinPositions_dataset = AllGamesToNNData(ReadGames(1))
LossPositions_dataset = AllGamesToNNData(ReadGames(-1))
DrawnPositions_dataset = AllGamesToNNData(ReadGames(0))

def RemoveDuplicates(dataset):
    # remove duplicated matrices
    result = [*set(dataset)]
    return result

#WinPositions_dataset = RemoveDuplicates(WinPositions_dataset)
#LossPositions_dataset = RemoveDuplicates(LossPositions_dataset)
#DrawnPositions_dataset = RemoveDuplicates(DrawnPositions_dataset)

Alldataset = numpy.concatenate((WinPositions_dataset, LossPositions_dataset, DrawnPositions_dataset))

Win_len = len(WinPositions_dataset)
Loss_len = len(LossPositions_dataset)
Drawn_len = len(DrawnPositions_dataset)
Alldataset_len = len(Alldataset)

Labels = [1]*Win_len + [-1]*Loss_len + [0]*Drawn_len

"""
# x is the dataset
# y is label set
"""
x_train, x_test, y_train, y_test = train_test_split(Alldataset, Labels)

print("Shape of dataset is ", x_train)

numOutPutResult = 3 ## 1 = win, 0 = draw, -1 = loss

y_train = keras.utils.to_categorical(y_train, numOutPutResult)
y_test = keras.utils.to_categorical(y_test, numOutPutResult)

# The SL PolicyNN 
input_shape = (18,9,9,3)
Model = keras.Sequential(
    [
       keras.Input(shape = input_shape),
       layers.Dense(128, activation = "relu"),
       layers.Dropout(0.2),
       layers.Dense(64, activation = "relu"),
       layers.Dense(32, activation = "relu"),
       layers.Flatten(),
       layers.Dropout(0.5),
       layers.Dense(numOutPutResult, activation='softmax')
    ]
)

Model.summary()

batch_size = 128
epochs = 15
Model.compile(loss="categorical_crossentropy", optimizer = "adam", metrics = "accuracy")
Model.fit(x_train, y_train, batch_size = batch_size, epochs = epochs, validation_split = 0.1)

score = Model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])