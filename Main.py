from Observation import Observation
from Transient import Transient
from random import randint

# open file
trans_file = open("trans_db/transients.txt", 'r')
t_num_lines = sum(1 for line in open('trans_db/transients.txt'))  # number of lines in the file
trans_file.close()
transients = []  # create list of transients


print('number of lines: ', t_num_lines)

# fill transient array with transients from file
t_count = 0
while t_count <= t_num_lines:
    print(t_count)
    trans_file = open("trans_db/transients.txt", 'r')
    ln = trans_file.readline()  # read a line from the file
    ln_list = ln.split("-")  # split line into parts with space delimiter
    loc = ln_list[0]  # get loc of transient
    cat = ln_list[1]  # get category of transient
    t = Transient(loc, cat)  # create transient
    transients.insert(t_count, t)  # add transient to list of transients
    trans_file.close()
    t_count += 1

# close transients file
print("transients have been populated")

# fill transients with observations from file
ts = 0
while ts <= t_num_lines:
    file_o_name = "trans_db/" + str(ts) + ".txt"
    file_o = open(file_o_name, 'w+')
    ln_o = file_o.readline()
    try:
        ln_o_list = ln_o.split("-")
        time = ln_o_list[0]
        mag = ln_o_list[2]
        obs = Observation(time, ts, mag)
        transients[ts].add_observation(obs)
    except IndexError:
        print("observation not available.")
    file_o.close()
    ts += 1


print("finished populating arrays")

# being MAIN LOOP
# MAIN LOOP
alive = True
while alive:
    print("MENU")
    print("1- Receive Event")
    print("2- Display Transients")
    print("3- Display a Transients Observation")
    print("4- Quit")
    cmd = input()

    if cmd == str(1):
        # get an observation
        obs = Observation(randint(100, 2400), randint(0, 100), randint(0, 20))
        # if transient is available add obs
        if transients[obs.get_loc()]:
            transients[obs.get_loc()].add_observation(obs)
            file_o_name = "trans_db/" + str(obs.get_loc()) + ".txt"
            file_o = open(file_o_name, 'w+')
            file_o.write(str(obs.get_time()) + "-" + str(obs.get_loc()) + "-" + str(obs.get_mag()))
        else:   # else create new transient
            t = Transient(obs.get_loc(), None)
            transients.insert(obs.get_loc(), t)
            t_num_lines += 1

    if cmd == str(4):
        alive = False


# exit

