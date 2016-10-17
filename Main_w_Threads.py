from Observation import Observation
from Transient import Transient
from collections import deque
from random import randint
from collections import defaultdict
import threading
import time


transients = defaultdict(Transient) #stores all transients
#load existing transients EXAMPLES
#transients[1] = Transient(1, "Supernova")
#transients[2] = Transient(2, "Star")
#transients[3] = Transient(3, "Meteor")
queue = deque()
threads = []
alive = True


#Thread that runs in the background
#Constantly stores the received alerts in a queue (FIFO)
def daemon_receive_alerts():
    while alive:
        #create Observation and store it
        queue.append(Observation(randint(0, 9), randint(1, 3), randint(0, 9)))
        #testing purpose
        print("Alert received")
        time.sleep(0.1)


#Thread that runs in the background
#Constantly checks if there are any unassigned Observation in the Queue
#and assigns them to a transient depending on the location
def daemon_process_observation():
    while alive:
        if queue:
            #get the oldest observation
            obs = queue.popleft()
            #create Transient if it is the first observation or just add Observation
            transients.setdefault(obs.get_loc(), Transient(obs.get_loc, None)).add_observation(obs)
            #Update probability either by creating a new thread or in the add_observation method
            #TO BE TESTED
            #transients[obs.get_loc()].update_probability
            print("Observation processed")
        else:
            #wait 0.2 seconds before checking the queue again
            time.sleep(0.2)


#create a thread that runs the daemon_receive_alerts method
Alertstream = threading.Thread(name='Alertstream', target=daemon_receive_alerts)
#set the thread as a daemon so it runs constantly in the background
Alertstream.setDaemon(True)
#run the thread
Alertstream.start()
#create a thread that runs the daemon_process_observations method
processObservation = threading.Thread(name='processObservation', target=daemon_process_observation)
#set the thread as a daemon so it runs constantly in the background
processObservation.setDaemon(True)
#run the thread
processObservation.start()

#stop threads / testing purpose only
time.sleep(1)
alive = False

#print observations per transient / testing purpose only
for t in transients:
    print(t)
    print(transients[t].get_cat())
    for o in transients[t].get_observation():
        print("Loc: " + str(o.get_loc()) + " | Time: " + str(o.get_time()) + " | Mag: " + str(o.get_mag()))


