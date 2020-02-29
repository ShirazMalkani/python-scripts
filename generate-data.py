import os
import sys
from shutil import copyfile
from PIL import Image

new_folder = "./data"
male_folder = os.path.join(new_folder, 'male')
female_folder = os.path.join(new_folder, 'female')

main_folder = "./SOCOFing/Altered/Altered-Easy"

main_folder_entries = os.listdir(main_folder)
male_counter = 0
female_counter = 0
for entry in main_folder_entries:
	# f, e = os.path.splitext(entry)
	# outfile = f + ".jpg"
	if not '__M_' in entry:
		# copyfile(, )
		infile = os.path.join(main_folder, entry)
		outfile = os.path.join(female_folder, 'female.' + str(female_counter) + '.jpg')
		Image.open(infile).save(outfile)
		female_counter = female_counter + 1
	else:
		# copyfile(os.path.join(main_folder, entry), os.path.join(male_folder, 'male.' + str(male_counter)))
		# male_counter = male_counter + 1

		infile = os.path.join(main_folder, entry)
		outfile = os.path.join(male_folder, 'male.' + str(male_counter) + '.jpg')
		Image.open(infile).save(outfile)
		male_counter = male_counter + 1
# # for infile in sys.argv[1:]:
# #     f, e = os.path.splitext(infile)
# #     outfile = f + ".jpg"
# #     if infile != outfile:
# #         try:
# #             Image.open(infile).save(outfile)
# #         except IOError:
#             print("cannot convert", infile)




