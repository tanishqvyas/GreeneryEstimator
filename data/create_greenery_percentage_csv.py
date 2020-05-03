import cv2
import os
import csv
import time
import pandas as pd



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

	# Read in the data from CSV to modify
	path_to_csv = os.path.join("csv","greenery_percentage.csv")
	df = pd.read_csv(path_to_csv)


	# Path to the image directory
	path = os.path.join("images","satellite")

	# Image resolution : 256 x 256 pixels
	TOTAL_PIXELS = 65536


	# A dictionary of images with key as sectorname
	# Eg : image_list["sector30"]
	image_list = load_images_from_folder(path)

	count = 0
	for sector, img in image_list.items():

		print("Current count --------------------> ",count)
		count += 1
		print("Sector : ", sector)



		green_pixel_count = 0

		# Find green pixel count for each sector
		for i in img:
			for j in i:

				if(j[1]>j[0] and j[1]>j[2] and j[0]<100 and j[2]<100):
					green_pixel_count += 1

		greenery_percentage = green_pixel_count*100/TOTAL_PIXELS
		
		# Find greenery | Keep lake bias check
		if(greenery_percentage > 60):

			roadmap_img = cv2.imread(os.path.join("images","roadmap",sector+".png"))
			lake_pixel_count = 0

			for i in roadmap_img:
				for j in i:


					# rgb(178, 207, 242)
					if(j[0] == 242 and j[1] == 200 and j[2] == 172):
						lake_pixel_count += 1

			if(lake_pixel_count > 0):
				green_pixel_count -= lake_pixel_count
				print("-----------------percent count changed for sector : ",sector)

		# Find greenery percentage
		greenery_percentage = green_pixel_count*100/TOTAL_PIXELS

		# Entering the number in dataframe
		cur_sector = int(sector.replace("sector",""))
		df["Greenery"][cur_sector] = greenery_percentage


		
			
	# Selecting input columns of name and greenery
	df = df[["Name","Greenery"]]	
	print(df)
	df.to_csv(os.path.join("csv","input.csv"), index=False)
	print("--- %s seconds ---" % (time.time() - start_time))


