#Reads altitude files and makes pngs of topograpy of cellular space. -Adam Rubin
import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import colormaps as cmaps
#Parameters for runs
dalti = 10 #how often altitude files produced a unit of t=0
dpng  = 100 #DESIRED frequency of png outputs, in t0 (ideally a multiple of dalti)
d = 3 #number of rows in CSP
l = 4	#number of items in each row

#Reads an altitude file into a matrix
def Read_alti_files(filename,d,l):
	altitude_data = np.empty(shape = [d,l])
	with open(filename, "r") as csvfile:
		reader = csv.reader(csvfile, delimiter = " ")
		current_row = 0
		for row in reader:	
			if '' in row: row.remove('')
			assert(current_row < d),"Wrong row length: d = " + str(d) + "; row length = " + str(len(row))
			assert(len(row) == l)
			for i, value in enumerate(row):
				altitude_data[current_row,i] = int(value)
			current_row += 1
	csvfile.close()
	return altitude_data

#reads the altitude data matrix and generates an image in the form of a png
def build_png_files(altitude_data, outname):
	plt.imshow(altitude_data%20, cmap=cmaps.viridis)
	plt.savefig(outname)
	print("saved figure")

# Find the names of altitude files to be processed
#Assumes in run directory with altitude files in out subdirectory. 
#Naming convention is "ALTI***.log" however is not sequential.
def find_alti_files(run_directory):
	# Find altitude files, sort
	all_alti_files = []
	for f in os.listdir(run_directory + "/out"):
		if f[0:4] == 'ALTI':
			all_alti_files.append(run_directory + "/out/" + f)
	all_alti_files.sort()

	#input them at desired frequency (see dpng and dalti)
	alti_files = []
	next_input = 0
	for i, f in enumerate(all_alti_files):
		assert(os.path.isfile(f))
		print(f, next_input)
		if i*dalti >= next_input:
			assert(os.path.isfile(f))
			alti_files.append(f)
			print("planning to work on " + f)
			next_input += dpng 
	return alti_files

def make_png_timeseries(run_directory):
	# get the filenames
	print("Making time series from: " + run_directory)
	alti_files = find_alti_files(run_directory)
	for i, fname in enumerate(alti_files):
		print("Making plot from " + fname)
		outname = run_directory + "/out/" + "plot_" + str(i*dpng) + "_t0.png"
		try:
			altitude_data = Read_alti_files(fname,d,l)
			build_png_files(altitude_data, outname)
		except AssertionError:
			print("skipping" + fname)

def calc_accumulations(run_directory):
    accum_avg = []
    accum_range = []
    current_col = 0
    print("Calculating accumulations from: " + run_directory)
    alti_files = find_alti_files(run_directory)
    for i, fname in enumerate(alti_files):
    	altitude_data = Read_alti_files(fname,d,l)
    	for column in range(l):
   	        accum_so_far = 0
   	        max_so_far = -float('inf')
   	        min_so_far = +float('inf')
   	        for row in altitude_data:
   	        	accum_so_far += row[column]
   	        	max_so_far = max(max_so_far, row[column])
   	        	min_so_far = min(min_so_far, row[column])
   	        accum_avg.append(accum_so_far / float(d))
   	        accum_range.append((min_so_far, max_so_far))
    print "average: " + str(accum_avg)
    print "range: " + str(accum_range)
    return (accum_avg, accum_range)


def main():
	#make_png_timeseries("../adam/runs/tauMin200_lambdaI0.0001")
	calc_accumulations("../adam/runs/TEST")

main()





	

	