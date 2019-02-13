import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os
from show_data import calc_accumulations
#Parameters for runs
dalti = 10 #how often altitude files produced a unit of t=0
dpng  = 100# DESIRED frequency of png outputs, in t0 (ideally a multiple of dalti)
d = 300 #number of rows in CSP
l = 600 #number of columns in CSP

def main():
    (accum_avg, accum_range) = calc_accumulations('../adam/runs/tauMin0_lambdaI0.001/out/ALTI01084_t01.log')
    plt.plot(accum_avg)
    y1 = [tmp[0] for tmp in accum_range] #minimums
    print y1
    y2 = [tmp[1] for tmp in accum_range] #maximums
    #print y2
    plt.fill_between(l, y1, y2)
    #plt.plot([tmp[0] for tmp in accum_range], ':') # minimums
    #plt.plot([tmp[1] for tmp in accum_range], ':') # maximums
    plt.show()