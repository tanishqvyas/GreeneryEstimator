import cv2
import os
import csv
import time



def load_images_from_folder(folder):
	images = {}
	for filename in os.listdir(folder):

		img = cv2.imread(os.path.join(folder,filename))
		
		current_sector = filename.replace(".png","")
		
		if img is not None:
			images[current_sector] = img

	return images


if __name__ == '__main__':

	# Start the clock
	start_time = time.time()

	# Path to the image directory
	path = os.path.join("images","satellite")

	# Image resolution : 256 x 256 pixels
	TOTAL_PIXELS = 65536

	# File path
	file_path = os.path.join("csv","sector_image.csv")

	# File handling
	f = open(file_path , mode = "w", newline = '')
	f_wr = csv.writer(f, delimiter = ",", quoting = csv.QUOTE_MINIMAL)
	f_wr.writerow(['Sector', "satellite","roadmap"])
	# 4142



	# A dictionary of images with key as sectorname
	# Eg : image_list["sector30"]
	image_list = load_images_from_folder(path)


	for sector, img in image_list.items():

		print("Sector : ", sector)

		# Getting roadmap image
		roadmap_img = cv2.imread(os.path.join("images","roadmap",sector+".png"))



		# Enter data in file
		f_wr = csv.writer(f, delimiter = ",", quoting = csv.QUOTE_MINIMAL)
		f_wr.writerow([sector,img, roadmap_img])
			

	f.close()
	print("--- %s seconds ---" % (time.time() - start_time))


