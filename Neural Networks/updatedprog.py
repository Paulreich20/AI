import os
import os.path
import tempfile
import matplotlib.pyplot as plt
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

# Construct a location in /tmp dir to hold cached data
dataPath = os.path.join(tempfile.gettempdir(), str(os.getuid()))
print(dataPath)
if not os.path.exists(dataPath):
    os.mkdir(dataPath)
filenameWithPath = os.path.join(dataPath, "mnist")

# Get training and testing sets
(x_train, y_train), (x_test, y_test) = mnist.load_data(path=filenameWithPath)

batch_size = 128
num_classes = 10
epochs = 20

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

#Layers created here
model = Sequential()
#model.add(Dense(512, activation='relu', input_shape=(784,))) #First hidden later with 512 nodes, 784 input nodes
#model.add(Dropout(0.2))
#model.add(Dense(512, activation='relu')) #Second hidden layer
#model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax', input_shape=(784,))) #Output layer




model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))

layer = model.get_layer(index=0)
weights = layer.get_weights()[0]
print(layer.get_weights()[0])

# List of weights is as so: Array of 784 arrays of length 10. each input node has its weights to
# all output nodes
weightsPerPixel = []
for i in range(10):
    weightsPerPixel.append(weights[:,i])
#print(weightsPerPixel[0])
#print(weightsPerPixel[0].reshape(28,28))
for i in range(10):
    plt.imshow(weightsPerPixel[i].reshape(28,28), cmap='Greys')
    plt.savefig('newDigit' + str(i) + '.png')

score = model.evaluate(x_test, y_test, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])
