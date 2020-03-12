# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initialising the CNN
model = Sequential()
# Step 1 - Convolution
model.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))
# Step 2 - Pooling
model.add(MaxPooling2D(pool_size = (2, 2)))
# Adding a second convolutional layer
model.add(Conv2D(32, (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))
# Step 3 - Flattening
model.add(Flatten())
# Step 4 - Full connection
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dense(units = 1, activation = 'sigmoid'))
# Compiling the CNN
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])


# # Part 2 - Fitting the CNN to the images
# from keras.preprocessing.image import ImageDataGenerator
# train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
# test_datagen = ImageDataGenerator(rescale = 1./255)
# training_set = train_datagen.flow_from_directory('/home/shiraz/Downloads/socofing/data/data/train', target_size = (64, 64), batch_size = 32, class_mode = 'binary')
# test_set = test_datagen.flow_from_directory('/home/shiraz/Downloads/socofing/data/data/test', target_size = (64, 64), batch_size = 32, class_mode = 'binary')
# model.fit_generator(training_set, steps_per_epoch = 800, epochs = 5, validation_data = test_set, validation_steps = 2000)

# model = Sequential()
model.load_weights('./second_try.h5', by_name=False)

# Part 3 - Making new predictions
import numpy as np
from keras.preprocessing import image

test_image = image.load_img('/home/shiraz/Downloads/socofing/data/data/test/males/male.723.jpg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)

result = model.predict(test_image)
# model.save_weights('first_try.h5')
# training_set.class_indices

if result[0][0] == 1:
	prediction = 'male'
else:
	prediction = 'female'
print(prediction)