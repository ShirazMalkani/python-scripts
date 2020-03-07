# import the necessary packages
import numpy as np
import cv2

# load the image from disk
image = cv2.imread("./horizontal_num.jpg")

# convert the image to grayscale and flip the foreground
# and background to ensure foreground is now "white" and
# the background is "black"
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


# grab the (x, y) coordinates of all pixel values that
# are greater than zero, then use these coordinates to
# compute a rotated bounding box that contains all
# coordinates
coords = np.column_stack(np.where(thresh > 0))
# print(coords)
angle = cv2.minAreaRect(coords)[-1]
# the `cv2.minAreaRect` function returns values in the
# range [-90, 0); as the rectangle rotates clockwise the
# returned angle trends to 0 -- in this special case we
# need to add 90 degrees to the angle
if angle < -45:
	angle = -(90 + angle)
# otherwise, just take the inverse of the angle to make
# it positive
else:
	angle = -angle


# rotate the image to deskew it
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
print("\n\n\n\n\n")
print(M)
rotated = cv2.warpAffine(image, M, (w, h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# # draw the correction angle on the image so we can validate it
# cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
# 	(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
# # show the output image
# print("[INFO] angle: {:.3f}".format(angle))
# cv2.imshow("Input", image)
# cv2.imshow("Rotated", rotated)

# Using cv2.imwrite() method 
# Saving the image 
# cv2.imwrite("./image01-rotated.jpg", rotated) 
# cv2.waitKey(0)

filter = True
# file_path = './image01-rotated.jpg'
# img = cv2.imread(file_path)
img = rotated
img = img[:, 10:]

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,90,150,apertureSize = 3)

kernel = np.ones((3,3),np.uint8)
edges = cv2.dilate(edges,kernel,iterations = 1)


kernel = np.ones((5,5),np.uint8)
edges = cv2.erode(edges,kernel,iterations = 1)
# cv2.imwrite('canny.jpg',edges)

lines = cv2.HoughLines(edges,1,np.pi/180,150)

if not lines.any():
    print('No lines were found')
    exit()

if filter:
    rho_threshold = 15
    theta_threshold = 0.1

    # how many lines are similar to a given one
    similar_lines = {i : [] for i in range(len(lines))}
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i == j:
                continue

            rho_i,theta_i = lines[i][0]
            rho_j,theta_j = lines[j][0]
            if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                similar_lines[i].append(j)

    # ordering the INDECES of the lines by how many are similar to them
    indices = [i for i in range(len(lines))]
    indices.sort(key=lambda x : len(similar_lines[x]))

    # line flags is the base for the filtering
    line_flags = len(lines)*[True]
    for i in range(len(lines) - 1):
        if not line_flags[indices[i]]: # if we already disregarded the ith element in the ordered list then we don't care (we will not delete anything based on it and we will never reconsider using this line again)
            continue

        for j in range(i + 1, len(lines)): # we are only considering those elements that had less similar line
            if not line_flags[indices[j]]: # and only if we have not disregarded them already
                continue

            rho_i,theta_i = lines[indices[i]][0]
            rho_j,theta_j = lines[indices[j]][0]
            if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                line_flags[indices[j]] = False # if it is similar and have not been disregarded yet then drop it now

print('number of Hough lines:', len(lines))

filtered_lines = []

if filter:
    for i in range(len(lines)): # filtering
        if line_flags[i]:
            filtered_lines.append(lines[i])

    print('Number of filtered lines:', len(filtered_lines))
else:
    filtered_lines = lines

for line in filtered_lines:
    rho,theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 2000*(-b))
    y1 = int(y0 + 2000*(a))
    x2 = int(x0 - 2000*(-b))
    y2 = int(y0 - 2000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

# cv2.imwrite('./hough.jpg',img)
# cv2.namedWindow('hough', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('hough', 600,600)
# cv2.imshow("hough", img)
# cv2.waitKey(0)

# file_path = './hough.jpg'
# col_img = cv2.imread(file_path)
col_img = img
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

for row in range(rows-10, 0, -1):
	if img[row, 0] == 0:
		end_index_row = row
		break

for col in range(cols-10, 0, -1):
	if img[0, col] == 0:
		end_index_col = col
		break

# print(start_index_col)
# print(start_index_row)
# print(end_index_col)
# print(end_index_row)

col_img[start_index_row, start_index_col] = (0,255,0)
col_img[end_index_row, end_index_col] = (0,255,0)

img = img[start_index_row:end_index_row, start_index_col:end_index_col]

# cv2.namedWindow('hough', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('hough', 600,600)
# cv2.imshow("hough", img)
# cv2.waitKey(0)

x_grids = 16
y_grids = 10

rows, cols = img.shape

x_next_value = rows // y_grids
y_next_value = cols // x_grids

images = []
x_values = []
y_values = []

x = 0
y = 0
for i in range(y_grids):
	x_values.append(x)
	x = x + x_next_value
x_values.append(x)

for i in range(x_grids):
	y_values.append(y)
	y = y + y_next_value
y_values.append(y)

print(x_values)
print(y_values)

for j in range(y_grids):
	for i in range(x_grids):
		images.append(img[x_values[j]:x_values[j+1], y_values[i]:y_values[i+1]])

folder = './pics/'
for i in range(len(images)):
	# cv2.namedWindow('hough', cv2.WINDOW_NORMAL)
	# cv2.resizeWindow('hough', 600,600)
	# cv2.imshow("hough", images[i])
	# cv2.waitKey(0)
	cv2.imwrite(folder + str(i) + '.jpg',images[i])


# cv2.namedWindow('hough1', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('hough1', 600,600)
# cv2.imshow("hough1", col_img)

cv2.imwrite('./grid.jpg',img)



