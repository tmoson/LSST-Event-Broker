from Observation import Observation
from Transient import Transient
from collections import deque
from random import randint
from collections import defaultdict
import threading
import time
import sys


queue = deque()
threads = []
alive = True


# Thread that runs in the background
# Constantly stores the received alerts in a queue (FIFO)
def daemon_receive_alerts():
    while alive:
        # create Observation and store it
        queue.append(Observation(randint(100, 2400), randint(0, 10), randint(0, 20)))
        # testing purpose
        print(">>Thread 1: ALERT CREATED")
        time.sleep(2)
        print(">>Thread 1: Slept")


# Thread that runs in the background
# Constantly checks if there are any unassigned Observation in the Queue
# and assigns them to a transient depending on the location
def daemon_process_observation():
    while alive:
        if queue:
            # get the oldest observation
            new_obs = queue.popleft()
            # if transient is available add obs
            print(">>Thread 2: RECEIVED LOCATION: ", str(new_obs.get_loc()))
            # create Transient if it is the first observation or just add Observation
            try:
                transients[str(new_obs.get_loc())].add_observation(new_obs)
                print(">>Thread 2: OBS ADDED SUCCESS", new_obs.get_mag())
            except TypeError:
                print(">>>Thread 2: TRANSIENT NOT FOUND: Creating new transient..")
                transients.setdefault(str(new_obs.get_loc()),
                                      Transient(new_obs.get_loc(), None)).add_observation(new_obs)
                file_t_name = "transients.txt"
                file_t = open(file_t_name, 'a+')
                file_t.write(str(new_obs.get_loc()) + "-" + str(transients[str(new_obs.get_loc())].get_cat()) + "\n")
                print(">>>Thread 2: NEW TRANS CREATED.")
                file_t.close()

            # Update probability either by creating a new thread or in the add_observation method
            # TO BE TESTED
            # transients[obs.get_loc()].update_probability
            # print("Observation processed")
        else:
            # wait 0.2 seconds before checking the queue again
            time.sleep(1)
            print(">>Thread 2: Slept")


# open file
trans_file = open("trans_db/transients.txt", 'r')
t_num_lines = sum(1 for line in trans_file)  # number of lines in the file
trans_file.close()
transients = defaultdict(Transient)  # create dict of transients

# ~~Fill transient array with transients from file~~
t_count = 0
trans_file = open("trans_db/transients.txt", 'r')
while t_count < t_num_lines:
    # print(t_count)
    ln = trans_file.readline()  # read a line from the file
    ln_list = ln.split("-")  # split line into parts with space delimiter
    loc = ln_list[0]  # get loc of transient
    cat = ln_list[1]  # get category of transient
    t = Transient(loc, cat)  # create transient
    transients[loc] = t  # add transient to list of transients
    t_count += 1

trans_file.close()  # close transients file


# ~~Load Transients with their observations~~
ts = 0
while ts < t_num_lines:
    file_o_name = "trans_db/" + str(ts) + ".txt"
    file_o = open(file_o_name, 'r+')
    ln_o = file_o.readline()
    print(file_o_name)
    try:
        ln_o_list = ln_o.split("-")
        o_time = ln_o_list[0]
        mag = ln_o_list[2]
        obs = Observation(o_time, ts, mag)
        transients[str(ts)].load_observation(obs)
        print("Observations LOADED")
    except TypeError:
        print('>>>TYPE ERROR')
        file_o.write(str(randint(100, 2400)) + "-" + str(ts) + "-" + str(randint(0, 15)) + '\n')
    file_o.close()
    ts += 1


# create a thread that runs the daemon_receive_alerts method
Alertstream = threading.Thread(name='Alertstream', target=daemon_receive_alerts)
# set the thread as a daemon so it runs constantly in the background
Alertstream.setDaemon(True)
# run the thread
Alertstream.start()
# create a thread that runs the daemon_process_observations method
processObservation = threading.Thread(name='processObservation', target=daemon_process_observation)
# set the thread as a daemon so it runs constantly in the background
processObservation.setDaemon(True)
# run the thread
processObservation.start()

# Exit Code
while True:
    print("ENTER 0 TO QUIT")
    cmd = input()
    if cmd == str(0):
        sys.exit()

