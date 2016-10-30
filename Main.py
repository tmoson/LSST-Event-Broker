from Observation import Observation
from Transient import Transient
from random import randint

# open file
trans_file = open("transients.txt")
t_num_lines = sum(1 for line in open('transients.txt'))  # number of lines in the file
transients = []  # create list of transients


print('number of lines: ', t_num_lines)

# fill transient array with transients from file
for x in range(0, t_num_lines - 1):
    print(x)
    ln = trans_file.readline()  # read a line from the file
    ln_list = ln.split(" ")  # split line into parts with space delimiter
    loc = ln_list[0]  # get loc of transient
    cat = ln_list[1]  # get category of transient
    t = Transient(loc, cat)  # create transient
    transients.insert(x, t)  # add transient to list of transients

# fill transients with observations from file

print('First transient location: ', transients[0].get_loc())
print('First transient category: ', transients[0].get_cat())

# being MAIN LOOP
# MAIN LOOP
alive = True
while alive:
    print("MENU")
    print("1- Receive Alert")
    print("2- Display Transients")
    print("3- Display a Transients Observation")
    print("4- Quit")
    cmd = input()

    if cmd == 1:
        # get an observation
        obs = Observation(randint(1000, 2000), randint(0, 10), randint(0, 100))
        # if transient is available add obs
        if transients[obs.get_loc()]:
            transients[obs.get_loc()].add_observation(obs)
        else:
            t = Transient(obs.get_loc(), None)
            transients.insert(obs.get_loc(), t)
            t_num_lines += 1

    if cmd == 4:
        alive = False


# save new transients to file
# close file
data_file.close()

