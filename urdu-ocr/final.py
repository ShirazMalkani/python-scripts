import cv2
import numpy as np

file_path = './hough.jpg'
col_img = cv2.imread(file_path)
img = cv2.cvtColor(col_img, cv2.COLOR_BGR2GRAY)
rows, cols = img.shape
# print(rows, cols)

ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
start_index_row = 0
start_index_col = 0
for row in range(rows):
	if img[row, 0] == 0:
		start_index_row = row
		break

for col in range(cols):
	if img[0, col] == 0:
		start_index_col = col
		break

for row in range(rows-1, 0, -1):
	if img[row, 0] == 0:
		end_index_row = row
		break

for col in range(cols-1, 0, -1):
	if img[0, col] == 0:
		end_index_col = col
		break

# print(start_index_col)
# print(start_index_row)
# print(end_index_col)
# print(end_index_row)

# col_img[start_index_row, start_index_col] = (0,255,0)
# col_img[end_index_row, end_index_col] = (0,255,0)

img = img[start_index_row:end_index_row, start_index_col:end_index_col]

x_grids = 7
y_grids = 10

rows, cols = img.shape

x_next_value = rows // x_grids
y_next_value = cols // y_grids

images = []
x_values = []
y_values = []

x = 0
y = 0
for i in range(x_grids):
	x_values.append(x)
	x = x + x_next_value
x_values.append(x)

for i in range(y_grids):
	y_values.append(y)
	y = y + y_next_value
y_values.append(y)

print(x_values)
print(y_values)

for i in range(x_grids):
	images.append(img[x_values[i]:x_values[i+1], y_values[0]:y_values[1]])


# for i in range(len(images)):
# 	cv2.namedWindow('hough', cv2.WINDOW_NORMAL)
# 	cv2.resizeWindow('hough', 600,600)
# 	cv2.imshow("hough", images[i])
# 	cv2.waitKey(0)

# cv2.namedWindow('hough1', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('hough1', 600,600)
# cv2.imshow("hough1", col_img)

cv2.imwrite('./grid.jpg',img)
cv2.waitKey(0)



