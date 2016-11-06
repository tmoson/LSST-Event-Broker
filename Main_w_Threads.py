from Observation import Observation
from Transient import Transient
from collections import deque
from random import randint
from collections import defaultdict
import threading
import time

queue = deque()
threads = []
alive = True

# Thread that runs in the background
# Constantly stores the received alerts in a queue (FIFO)
def daemon_receive_alerts():
    while alive:
        # create Observation and store it
        queue.append(Observation(randint(100, 2400), randint(0, 100), randint(0, 20)))
        # testing purpose
        #print("Alert received")
        time.sleep(0.1)


# Thread that runs in the background
# Constantly checks if there are any unassigned Observation in the Queue
# and assigns them to a transient depending on the location
def daemon_process_observation():
    while alive:
        if queue:
            # get the oldest observation
            obs = queue.popleft()
            # if transient is available add obs
            #print(str(obs.get_loc()))
            # create Transient if it is the first observation or just add Observation
            try:
                transients[obs.get_loc()].add_observation(obs)
            except TypeError:
                transients.setdefault(obs.get_loc(), Transient(obs.get_loc(), None)).add_observation(obs)
                file_t_name = "transients.txt"
                file_t = open(file_t_name, 'a+')
                file_t.write(str(obs.get_loc()) + "-" + str(transients[obs.get_loc()].get_cat()) + "\n")
                file_t.close()

            #add observation to txt
            file_o_name = "trans_db/" + str(obs.get_loc()) + ".txt"
            file_o = open(file_o_name, 'a+')
            file_o.write(str(obs.get_time()) + "-" + str(obs.get_loc()) + "-" + str(obs.get_mag()) + "\n")
            file_o.close()
            # Update probability either by creating a new thread or in the add_observation method
            # TO BE TESTED
            # transients[obs.get_loc()].update_probability
            #print("Observation processed")
        else:
            # wait 0.2 seconds before checking the queue again
            time.sleep(0.2)

# open file
trans_file = open("transients.txt", 'r')
t_num_lines = sum(1 for line in trans_file)  # number of lines in the file
trans_file.close()
transients = defaultdict(Transient)  # create dict of transients

#print('number of lines: ', t_num_lines)

# fill transient1 array with transients from file
t_count = 0

while t_count <= t_num_lines:
    #print(t_count)
    trans_file = open("trans_db/transients.txt", 'r')
    ln = trans_file.readline()  # read a line from the file
    ln_list = ln.split("-")  # split line into parts with space delimiter
    loc = ln_list[0]  # get loc of transient
    cat = ln_list[1]  # get category of transient
    t = Transient(loc, cat)  # create transient
    transients[loc] = t  # add transient to list of transients
    trans_file.close()
    t_count += 1

# close transients file
#print("transients have been populated")

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

# being MAIN LOOP
# MAIN LOOP
alive = True
while alive:
    print("MENU")
    print("1- Display Transients")
    print("2- Display a Transients Observation")
    print("3- Quit")
    cmd = input()

    if cmd == str(3):
        alive = False
