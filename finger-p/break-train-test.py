import os
import sys
from shutil import copyfile
from PIL import Image
import random

# create directories
dataset_home = "./data/data/"
subdirs = ['train/', 'test/']
for subdir in subdirs:
	# create label subdirectories
	labeldirs = ['males/', 'females/']
	for labldir in labeldirs:
		newdir = dataset_home + subdir + labldir
		os.makedirs(newdir, exist_ok=True)

# seed random number generator
random.seed(1)
# define ratio of pictures to use for validation
val_ratio = 0.25
# copy training dataset images into subdirectories
src_directory = dataset_home
for file in os.listdir(src_directory):
	src = os.path.join(src_directory, file)
	dst_dir = 'train/'
	if random.random() < val_ratio:
		dst_dir = 'test/'
	if file.startswith('female'):
		# dst = dataset_home + dst_dir + 'cats/'  + file
		dst = os.path.join(dataset_home, dst_dir, 'females', file)
		copyfile(src, dst)
	elif file.startswith('male'):
		# dst = dataset_home + dst_dir + 'dogs/'  + file
		dst = os.path.join(dataset_home, dst_dir, 'males', file)
		copyfile(src, dst)