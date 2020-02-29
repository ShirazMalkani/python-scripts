# baseline model for the male vs female finger prints dataset
import sys
from matplotlib import pyplot
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator

# define cnn model
def define_model():
	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=(200, 200, 3)))
	model.add(MaxPooling2D((2, 2)))
	model.add(Flatten())
	model.add(Dense(128, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(1, activation='sigmoid'))
	# compile model
	opt = SGD(lr=0.001, momentum=0.9)
	model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])
	return model

# plot diagnostic learning curves
def summarize_diagnostics(history):
	# plot loss
	pyplot.subplot(211)
	pyplot.title('Cross Entropy Loss')
	pyplot.plot(history.history['loss'], color='blue', label='train')
	pyplot.plot(history.history['val_loss'], color='orange', label='test')
	# plot accuracy
	pyplot.subplot(212)
	pyplot.title('Classification Accuracy')
	pyplot.plot(history.history['accuracy'], color='blue', label='train')
	pyplot.plot(history.history['val_accuracy'], color='orange', label='test')
	# save plot to file
	filename = sys.argv[0].split('/')[-1]
	pyplot.savefig(filename + '_plot.png')
	pyplot.close()

# run the test harness for evaluating a model
def run_test_harness():
	print('defining model')
	# define model
	model = define_model()

	print('image data generator')
	# create data generator
	datagen = ImageDataGenerator(rescale=1.0/255.0)

	print('loading train_it')
	# prepare iterators
	train_it = datagen.flow_from_directory('./data/data/train/',
		class_mode='binary', batch_size=64, target_size=(200, 200))

	print('loading test_it')
	test_it = datagen.flow_from_directory('./data/data/test/',
		class_mode='binary', batch_size=64, target_size=(200, 200))

	print('fitting model')
	# fit model
	history = model.fit_generator(train_it, steps_per_epoch=500,
		validation_data=test_it, validation_steps=250, epochs=20, verbose=0)

	print('evaluating model')
	# evaluate model
	_, acc = model.evaluate_generator(test_it, steps=500, verbose=0)
	print('> %.3f' % (acc * 100.0))
	# learning curves
	summarize_diagnostics(history)

# entry point, run the test harness
run_test_harness()