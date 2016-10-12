from Observation import Observation
from Transient import Transient
import time
import os

# open file
data_file = open("transients.txt")
# mod_time = os.path.getmtime(data_file)  # time the file was last modified
num_lines = sum(1 for line in open('transients.txt'))  # number of lines in the file
transients = []  # create list of transients

print('number of lines: ', num_lines)

# fill transient array with transients from file
for x in range(0, num_lines - 1):
    print(x)
    ln = data_file.readline()  # read a line from the file
    ln_list = ln.split(" ")  # split line into parts with space delimiter
    loc = ln_list[0]  # get loc of transient
    cat = ln_list[1]  # get category of transient
    t = Transient(loc, cat)  # create transient
    transients.insert(x, t)  # add transient to list of transients

print('First transient location: ', transients[0].get_loc())
print('First transient category: ', transients[0].get_cat())

# being MAIN LOOP
# while True:
    # get time series (or an Observation from Generator

    # compare to current Transients
    # for observation in transients:

# save new transients to file
# close file
data_file.close()

