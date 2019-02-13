#Reads altitude files and makes pngs of topograpy of cellular space. -Adam Rubin
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import colormaps as cmaps
import os
#import colormaps as cmaps
#Parameters for runs
dalti = 10 #how often altitude files produced a unit of t=0
dpng  = 100# DESIRED frequency of png outputs, in t0 (ideally a multiple of dalti)
d = 300 #number of rows in CSP
l = 600 #number of columns in CSP

#Reads an altitude file into a matrix
#Returns (True, data) if successful, else (False, baddata)
def Read_alti_files(filename,d,l):
    altitude_data = np.empty(shape = [d,l])
    current_d     = d
    maxv = 0
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter = " ")
        current_row = 0
        for row in reader:    
            # Delimiter leaves dangling empty strings at ends of rows
            if '' in row: row.remove('')
            # require correct value for l
            if len(row) != l:
                print("Warning: Irregular row length. Skipping file.")
                return (False, altitude_data)
            # Resize array if d value was incorrect
            if current_row >= current_d: 
                current_d     = 2*current_d 
                tmp           = altitude_data
                altitude_data = np.empty(shape = [current_d,l])
                altitude_data[:current_row, :l] = tmp[:current_row,:l]
                #print("Warning: Unexpected row count. Expected " + str(d) + " lines, got at least " + str(current_row))
            for i, value in enumerate(row):
                altitude_data[current_row,i] = int(value)
                #if value > maxv:
            current_row += 1
    csvfile.close()
    # Hacky fix: return *last* d lines of files that were wrong length
    # return (True, altitude_data[:current_row-1, :l]) # w/o hacky fix
    #print altitude_data
    return (True, altitude_data[current_row-d:current_row, :l]) # hacky fix

#reads the altitude data matrix and generates an image in the form of a png
def build_png_files(altitude_data, outname):
    vmax = 10
    if altitude_data.any() > vmax: print("Warning: saturated color range.")
    plt.imshow(altitude_data % vmax, cmap=cmaps.inferno, vmin=2, vmax=10)
    plt.xlabel('x (cells)')
    plt.ylabel('y (cells)')
    plt.savefig(outname)
    plt.clf()

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
    alti_files   = []
    alti_t0      = []
    t0           = 0
    next_plot_t0 = 0
    for i, f in enumerate(all_alti_files):
        assert(os.path.isfile(f))
        if t0 >= next_plot_t0:
            assert(os.path.isfile(f))
            alti_t0.append(t0)
            alti_files.append(f)
            # print("planning to work on " + f)
            next_plot_t0 += dpng 
        t0 += dalti
    return (alti_files, alti_t0)

def make_png_timeseries(run_directory):
    # get the filenames
    print("Making time series from: " + run_directory)
    (alti_files, alti_t0) = find_alti_files(run_directory)
    for i, fname in enumerate(alti_files):
        #print("Making plot from " + fname)
        outname = run_directory + "/out/" + "plot_" + str(alti_t0[i]) + "t0.png"
        (successful_read, altitude_data) = Read_alti_files(fname,d,l)
        if successful_read: build_png_files(altitude_data, outname)
        else: print("Skipped " + fname)

def calc_accumulations(filename):
    accum_avg = []
    accum_range = []
    current_col = 0
        #altitude_data = Read_alti_files(fname,d,l)
    (value, altitude_data) = Read_alti_files(filename,d,l)
    #print altitude_data
    if value is False:
        return False
    for column in range(l):
        accum_so_far = 0
        max_so_far = -float('inf')
        min_so_far = +float('inf')
        for row in altitude_data:
            #print row
            accum_so_far += row[column]
            max_so_far = max(max_so_far, row[column])
            min_so_far = min(min_so_far, row[column])
        accum_avg.append(accum_so_far / float(d))
        accum_range.append((min_so_far, max_so_far))
    #print "average: " + str(accum_avg)
    #print "range: " + str(accum_range)
    return (accum_avg, accum_range)

#Use this function in order to change properties of plot
def build_plot(filename):
    (accum_avg, accum_range) = calc_accumulations(filename)
    plt.title('Height of bedform vs distance', fontsize = 20) #Title
    plt.xlabel('distance', fontsize = 20) #x-axis label
    plt.ylabel('height', fontsize = 20) #y-axis label
    x = np.arange(0.0, l, 1)
    y1 = [tmp[0] for tmp in accum_range] #minimums
    #print y1
    y2 = [tmp[1] for tmp in accum_range] #maximums
    #print y2
    plt.fill_between(x, y1, y2, color = 'silver', alpha = 0.7) #alpha changes transparency of the filled color
    plt.plot(accum_avg, color = 'black')
    plt.savefig(filename+'.png', dpi=300)
    plt.clf()
    #plt.show()

def build_all_plots(run_directory):
    # get the filenames
    print("Making plot series from: " + run_directory)
    (alti_files, alti_t0) = find_alti_files(run_directory)
    for i, fname in enumerate(alti_files):
        #print("Making plot from " + fname)
        #outname2 = run_directory + "/out/" + "line_plot_" + str(alti_t0[i]) + "t0.png"
        #print(outname2)
        build_plot(fname)


def main():
        #build_plot('../adam/runs/tauMin0_lambdaI0.001/out/ALTI01084_t01.log')
        #build_all_plots('../adam/runs/tauMin0_lambdaI0.001')
        root = '../adam/runs'
        for d in os.listdir(root):
            d = os.path.join(root, d)
            if os.path.isdir(d):
                try:
                    make_png_timeseries(d)
                    build_all_plots(d)
                except:
                    print("ERROR: Time series field for directory " + d)

main()


