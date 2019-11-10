import os
import os.path
import tempfile
import matplotlib.pyplot as plt
import keras
from keras.datasets import mnist

# Construct a location in /tmp dir to hold cached data
dataPath = os.path.join(tempfile.gettempdir(), str(os.getuid()))
print(dataPath)
if not os.path.exists(dataPath):
    os.mkdir(dataPath)
filenameWithPath = os.path.join(dataPath, "mnist")

# Get training and testing sets
(x_train, y_train), (x_test, y_test) = mnist.load_data(path=filenameWithPath)

# Save single image to a file to view
plt.imshow(x_train[0], cmap='Greys')
plt.savefig('digit.png')
