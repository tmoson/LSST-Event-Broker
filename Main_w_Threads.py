from Observation import Observation
from Transient import Transient
from collections import deque
from random import randint
from collections import defaultdict
import threading
import time


transients = defaultdict(Transient) #stores all transients
#load existing transients EXAMPLES
transients[1] = Transient(1, "Supernova")
transients[2] = Transient(2, "Star")
transients[3] = Transient(3, "Meteor")
queue = deque()
threads = []
alive = True


def daemon_receive_alerts():
    while alive:
        queue.append(Observation(randint(0, 9), randint(1, 3), randint(0, 9)))
        print("Alert received")
        time.sleep(0.1)


def daemon_process_observation():
    while alive:
        if queue:
            obs = queue.popleft()
            #if transients[obs.get_loc]:
             #   transients[obs.get_loc] = Transient(obs.get_loc, None)
            transients[obs.get_loc()].add_observation(obs)
            #transients[obs.get_loc()].update_propability
            print("Observation processed")
        else:
            time.sleep(0.2)


Alertstream = threading.Thread(name='Alertstream', target=daemon_receive_alerts)
Alertstream.setDaemon(True)
Alertstream.start()
processObservation = threading.Thread(name='processObservation', target=daemon_process_observation)
processObservation.setDaemon(True)
processObservation.start()

time.sleep(1)
alive = False

for t in transients:
    print(t)
    print(transients[t].get_cat())
    for o in transients[t].get_observation():
        print("Loc: " + str(o.get_loc()) + " | Time: " + str(o.get_time()) + " | Mag: " + str(o.get_mag()))


