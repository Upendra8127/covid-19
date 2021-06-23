# python build_covid_dataset.py --covid covid-chestxray-dataset --output dataset/covid

import pandas as pd
import argparse
import shutil
import os

# constructing the argument parser and parsing the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--covid", required=True,
	help="path to base directory for COVID-19 dataset")
ap.add_argument("-o", "--output", required=True,
	help="path to directory where 'normal' images will be stored")
args = vars(ap.parse_args())

# constructing the path to the metadata CSV file and loading it
csvPath = os.path.sep.join([args["covid"], "metadata.csv"])
df = pd.read_csv(csvPath)

# looping over the rows of the COVID-19 data frame
for (i, row) in df.iterrows():
	if row["finding"] != "COVID-19" or row["view"] != "PA":
		continue

	# building the path to the input image file
	imagePath = os.path.sep.join([args["covid"], "images",
		row["filename"]])

	# if the input image file does not exist (there are some errors in
	# the COVID-19 metadeta file), ignore the row
	if not os.path.exists(imagePath):
		continue

	# extracting the filename from the image path and then constructing the
	# path to the copied image file
	filename = row["filename"].split(os.path.sep)[-1]
	outputPath = os.path.sep.join([args["output"], filename])

	# copy the image
	shutil.copy2(imagePath, outputPath)