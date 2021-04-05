import file2
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Convolution2D, MaxPooling2D, Dense, Dropout, Flatten
from sklearn.utils import shuffle
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

X, Y = file2.gen_data(size=1000, img_size=50)
X, Y = shuffle(X, Y)
encoder = LabelEncoder()
encoder.fit(Y)
Y = encoder.transform(Y)
Y = np_utils.to_categorical(Y, 3)

num_train, height, width = X.shape
batch_size = 32
num_epochs = 10
kernel_size = 6
pool_size = 4
conv_depth_1 = 32
conv_depth_2 = 64
drop_prob_1 = 0.25
drop_prob_2 = 0.5
hidden_size = 512

inp = Input(shape=(height, width, 1))

conv_1 = Convolution2D(conv_depth_1, (kernel_size, kernel_size), padding='same', activation='relu', data_format='channels_last')(inp)
conv_2 = Convolution2D(conv_depth_1, (kernel_size, kernel_size), padding='same', activation='relu', data_format='channels_last')(conv_1)
pool_1 = MaxPooling2D(pool_size=(pool_size, pool_size))(conv_2)
drop_1 = Dropout(drop_prob_1)(pool_1)

conv_3 = Convolution2D(conv_depth_2, (kernel_size, kernel_size), padding='same', activation='relu', data_format='channels_last')(drop_1)
conv_4 = Convolution2D(conv_depth_2, (kernel_size, kernel_size), padding='same', activation='relu', data_format='channels_last')(conv_3)
pool_2 = MaxPooling2D(pool_size=(pool_size, pool_size))(conv_4)
drop_2 = Dropout(drop_prob_1)(pool_2)

flat = Flatten()(drop_2)
hidden = Dense(hidden_size, activation='relu')(flat)
drop_3 = Dropout(drop_prob_2)(hidden)
out = Dense(3, activation='softmax')(drop_3)

model = Model(inputs=inp, outputs=out)

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

###########################################################################

accuracy_list = []
val_accuracy_list = []

try:
    epoch_list = input("Enter epoch with spaces: ").split(' ')
    epoch_list = list(map(int, epoch_list))
except ValueError:
    print("Wrong input")
    epoch_list = [-1]

class CustomCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):

        accuracy_list.append(logs['accuracy'])
        val_accuracy_list.append(logs['val_accuracy'])

        ne_val_accuracy_list = []

        for i in val_accuracy_list:
            ne_val_accuracy_list.append(1-i);


        if epoch_list.count(epoch + 1) != 0:
            data = {'val_accuracy': val_accuracy_list,
                    '1 - val_accutacy': ne_val_accuracy_list}
            fig, ax = plt.subplots()
            df = pd.DataFrame(data)
            df.plot(kind='bar', stacked=True)
            plt.savefig("plot_" + str(epoch + 1))
            plt.show()


###########################################################################

history = model.fit(X, Y,
                    batch_size= batch_size,
                    epochs= num_epochs,
                    validation_split=0.1,
                    callbacks=[CustomCallback()])

X_test, Y_test = file2.gen_data(size= 1000, img_size=50)
encoder = LabelEncoder()
encoder.fit(Y_test)
Y_test = encoder.transform(Y_test)
Y_test = np_utils.to_categorical(Y_test, 3)
model.evaluate(X_test, Y_test)