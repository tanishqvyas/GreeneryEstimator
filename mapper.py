#!/usr/bin/env python

import sys
for line in sys.stdin:



	# Get each line of input
	line = line.strip()

	if(line=="Name,Greenery"):
		continue

	
	# extract resp values outta the entry
	area_name, percentage = map(str, line.split(","))


	if(float(percentage) >= 75):
		# print the area_name
		print(str(area_name)+",1")
		

	