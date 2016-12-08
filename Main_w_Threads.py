import threading
import pyodbc
import os
from Transient import Transient
from Classifier import Classifier
from Observation import Observation
from collections import deque

def buildTableClassifiers():
    lock.acquire()
    try:
        query = "Select ClassifierID, Name, Min, Max, Description From Classifier, Model Where Classifier.ModelID = Model.ModelID"
        cursor.execute(query)
        rows = cursor.fetchall()
        print("+----+----------------------------------------+----------------------------------------+----------------------------------------+---------------------+")
        print("|\033[1m %2s \033[0m|\033[1m %38s \033[0m|\033[1m %38s \033[0m|\033[1m %38s \033[0m|\033[1m %19s \033[0m|" % (
            'ID', 'Name', 'Equation1', 'Equation2', 'Classifies'))
        print("+----+----------------------------------------+----------------------------------------+----------------------------------------+---------------------+")
        for row in rows:
            print("|%4s| %39s| %39s| %39s| %20s|" % (row.ClassifierID, row.Name, row.Min, row.Max, row.Description))
            print(
            "+----+----------------------------------------+----------------------------------------+----------------------------------------+---------------------+")
    finally:
        lock.release()

def buildTableTransients():
    lock.acquire()
    try:
        query = "Select TransientID, Class, Location, Name From Transient, Classifier Where Transient.LastClassifiedWith = Classifier.ClassifierID"
        cursor.execute(query)
        rows = cursor.fetchall()
        print("+----+----------------------------------------+----------------------------------------+----------------------------------------+")
        print("|\033[1m %2s \033[0m|\033[1m %38s \033[0m|\033[1m %38s \033[0m|\033[1m %38s \033[0m|" % (
            'ID', 'Class', 'Location', 'Classifier'))
        print("+----+----------------------------------------+----------------------------------------+----------------------------------------+")
        for row in rows:
            print("|%4s| %39s| %39s| %39s|" % (row.TransientID, row.Class, row.Location, row.Name))
            print(
            "+----+----------------------------------------+----------------------------------------+----------------------------------------+")
    finally:
        lock.release()

def buildTableModel():
    lock.acquire()
    try:
        query = "Select ModelID, Description From Model"
        cursor.execute(query)
        rows = cursor.fetchall()
        print("+----+---------------------+")
        print("|\033[1m %2s \033[0m|\033[1m %19s \033[0m|" % (
            'ID', 'Description'))
        print("|----+---------------------|")
        for row in rows:
            print("|%4s| %20s|" % (row.ModelID, row.Description))
        print("+----+---------------------+")
    finally:
        lock.release()


#connect to database
db = os.getcwd() + "/EventBroker.db"
#cnxn = pyodbc.connect(r'DSN=MyConnection;DBQ='+db)
cnxn = pyodbc.connect('DRIVER={SQLite3};SERVER=localhost;DATABASE='+db)
# Opening a cursor
cursor = cnxn.cursor()
queue = deque()
threads = []
alive = True
lock = threading.RLock()

# Thread that runs in the background
# Constantly stores the received alerts
def daemon_store_transients():
    while alive or queue:
        lock.acquire()
        try:
            # Save loc and magnitude
            loc = '1'
            magnitude = 1
            # Find right transient
            name = "fgjh"

            query = "Select TransientID From Transient Where Class='%s' AND Location = '%s'" %(name, loc)

            cursor.execute(query)
            row = cursor.fetchone()
            try:
                t = row[0]
            # If transient is not stored yet
            except TypeError:
                cursor.execute("Insert into Transient ( Class, RightAscension, Declination, Location, LastClassifiedWith, Classified ) VALUES ('%s', 0, 1,  '%s', 1, 0)" % (name, loc))
                cursor.commit()
                cursor.execute(query)
                row = cursor.fetchone()
                t = row[0]

            # store Observation
            cursor.execute("INSERT INTO Observation (Time, Location, Magnitude, TransientID ) VALUES ('1', '%s', %d, %d)" %(loc, magnitude, t))
            cursor.commit()

            # create tmp Transient and calculate
            query = "Select RightAscension, Declination, LastClassifiedWith From Transient where TransientID = %d" % t
            cursor.execute(query)
            row = cursor.fetchone()
            cid2 = row.LastClassifiedWith
            transienttmp = Transient(row.RightAscension, row.Declination)

            # get Observations
            query = "Select Observation.Time, Observation.Location, Observation.Magnitude From Transient, Observation where Observation.TransientID = %d and Observation.TransientID = Transient.TransientID" % t
            cursor.execute(query)
            row = cursor.fetchall()

            # add observations
            for r in row:
                transienttmp.add_observation(Observation(r.Time, r.Location, r.Magnitude))

            # Create Classifier Instance
            query = "Select Min, Max, Description From Classifier, Model where Classifier.ClassifierID = %d and Classifier.ModelID  = Model.ModelID " % cid2
            cursor.execute(query)
            row = cursor.fetchone()
            c = Classifier(row.Description, row.Min, row.Max, 1)
            # calculate
            bln = c.classify(transienttmp)
            bln = False

            if bln:
                query = "Update Transient Set Classified =  1 where Transient.TransientID = %d" % t
                cursor.execute(query)
                cursor.commit()

            # print("Alert received")
        except pyodbc.DatabaseError:
            print("Oberservation storage error")
        finally:
            lock.release()
            # time.sleep(0.1)

def daemon_receive_alerts():
    while queue:
        i=0

def daemon_send_transients():
    while alive:
        lock.acquire()
        try:
            query = "Select * From Transient Where Classified = 1"
            # store Observation
            cursor.execute(query)
            row = cursor.fetchone()
            try:
                t = row[0]
                if t:
                    # send Transient
                    id = row.TransientID
                    query = "Delete From Transient Where TransientID = %d" % id
                    cursor.execute(query)
                    cursor.commit()
            except TypeError:
                pass
        except pyodbc.DatabaseError:
            print("Transient Classify error")
        finally:
            lock.release()
            # time.sleep(0.1)

# create a thread that runs the daemon_receive_alerts method
Alertstream = threading.Thread(name='Alertstream', target=daemon_receive_alerts)
Transientstream = threading.Thread(name='Transientstream', target=daemon_send_transients)
DataBasestream = threading.Thread(name='DataBasestream', target=daemon_store_transients)
# run the thread
Alertstream.start()
Transientstream.start()
DataBasestream.start()

# being MAIN LOOP
# MAIN LOOP
alive = True
try:
    while alive:
        print("MENU")
        print("1 Set Classifiers")
        print("2 Show Classifiers")
        print("3 Show Models")
        print("4 Quit")
        cmd1 = raw_input("Enter digit: ")
        # cmd1 = input("Enter digit: ")
        if cmd1 == str(1):
            buildTableTransients()
            tid = raw_input("Enter TransientID: ")
            cid = raw_input("Enter ClassiferID or Classifier name: ")

            lock.acquire()
            try:
                # get Classifier ID
                tid = int(tid)

                try:
                    cid = int(cid)
                    query = "Select ClassifierID From Classifier Where Classifier.ClassifierID=%d" % cid
                    cursor.execute(query)
                    row = cursor.fetchone()
                    if not row:
                        raise pyodbc.DatabaseError
                except ValueError:
                    query = "Select ClassifierID From Classifier Where Classifier.Name='%s'" % cid
                    cursor.execute(query)
                    row = cursor.fetchone()
                    if not row:
                        raise pyodbc.DatabaseError
                    else:
                        cid = row.ClassifierID
                query = "Update Transient Set LastClassifiedWith = %d where Transient.TransientID = %d" %(cid, tid)
                cursor.execute(query)
                cursor.commit()

                # create tmp Transient and calculate
                query = "Select RightAscension, Declination From Transient where TransientID = %d" %tid
                cursor.execute(query)
                row = cursor.fetchone()
                transienttmp = Transient(row.RightAscension, row.Declination)

                # get Observations
                query = "Select Observation.Time, Observation.Location, Observation.Magnitude From Transient, Observation where Observation.TransientID = %d and Observation.TransientID = Transient.TransientID" % tid
                cursor.execute(query)
                row = cursor.fetchall()

                # add observations
                for r in row:
                    transienttmp.add_observation(Observation(r.Time, r.Location, r.Magnitude))

                # Create Classifier Instance
                query = "Select Min, Max, Description From Classifier, Model where Classifier.ClassifierID = %d and Classifier.ModelID  = Model.ModelID " % cid
                cursor.execute(query)
                row = cursor.fetchone()
                c = Classifier(row.Description, row.Min, row.Max, 1)
                # calculate
                bln = c.classify(transienttmp)

                if bln:
                    query = "Update Transient Set Classified =  1 where Transient.TransientID = %d" %tid
                    cursor.execute(query)
                    cursor.commit()
                    # print("true")
                buildTableTransients()
            except pyodbc.DatabaseError:
                print("ClassifierID not found")
            except ValueError:
                print("Input error")
            finally:
                lock.release()
        # CLASSIFIER
        elif cmd1 == str(2):
            lock.acquire()
            try:
                buildTableClassifiers()
            except pyodbc.DatabaseError:
                print("Could not load table")
            finally:
                lock.release()
            menu = True
            while menu:
                print("MENU")
                print("1 ADD Classifier")
                print("2 Change Classifier [-ID]")
                print("3 Delete Classifier [-ID]")
                print("4 Back")
                cmd2 = raw_input("Enter digit: ").split()
                # cmd2 = input("Enter digit: ").split()

                try:
                    if len(cmd2) == 1 and (cmd2[0] != '1' and cmd2[0] != '4'):
                        print("Please choose the ID of the Classifier (e.g. -1)")
                    elif cmd2[0] == str(1):
                        try:
                            name = raw_input("Name: ")
                            min = raw_input("Equation 1: ")
                            max = raw_input("Equation 2: ")
                            desc = raw_input("Transient model (name or ID): ")
                            # name = input("Name: ")
                            # min = float(input("Minimum value: "))
                            # max = float(input("Maximum value: "))
                            # desc = input("Transient model (string or ID): ")

                            lock.acquire()
                            try:
                                # get model ID
                                try:
                                    desc = int(desc)
                                    query = "Select ModelID From Model Where Model.ModelID=%d" %desc
                                    cursor.execute(query)
                                    row = cursor.fetchone()
                                    if not row:
                                        raise pyodbc.DatabaseError
                                except ValueError:
                                    query = "Select ModelID From Model Where Model.Description='%s'" % desc
                                    cursor.execute(query)
                                    row = cursor.fetchone()
                                    if not row:
                                        raise pyodbc.DatabaseError
                                    else:
                                        desc = row.ModelID
                                query = "INSERT INTO Classifier ( Name, Min, Max, ModelID ) VALUES ('%s', '%s', '%s', %d)" % (name, min, max, desc)
                                cursor.execute(query)
                                cursor.commit()
                            except pyodbc.DatabaseError:
                                print("ModelID not found")
                            finally:
                                lock.release()
                        except ValueError:
                            print('Input error')
                        buildTableClassifiers()

                    elif cmd2[0] == str(2):
                        try:
                            id = int(cmd2[1][1:])
                            if cmd2[1][:1] == '-' and id:
                                try:
                                    name = raw_input("Name: ")
                                    min = raw_input("Equation 1: ")
                                    max = raw_input("Equation 2: ")
                                    desc = raw_input("Transient model (string or ID): ")
                                    # name = input("Name: ")
                                    # min = float(input("Minimum value: "))
                                    # max = float(input("Maximum value: "))
                                    # desc = input("Transient model (string or ID): ")

                                    lock.acquire()
                                    try:
                                        # get model ID
                                        try:
                                            desc = int(desc)
                                            query = "Select ModelID From Model Where Model.ModelID=%d" %desc
                                            cursor.execute(query)
                                            row = cursor.fetchone()
                                            if not row:
                                                raise pyodbc.DatabaseError
                                        except ValueError:
                                            query = "Select ModelID From Model Where Model.Description='%s'" % desc
                                            cursor.execute(query)
                                            row = cursor.fetchone()
                                            if not row:
                                                raise pyodbc.DatabaseError
                                            else:
                                                desc = row.ModelID
                                        query = "UPDATE Classifier Set Name = '%s', Min = '%s',  Max = '%s', ModelID = %d where ClassifierID = %d" %(name, min, max, desc, id)
                                        cursor.execute(query)
                                        cursor.commit()
                                    except pyodbc.DatabaseError:
                                        print("ID not found")
                                    finally:
                                        lock.release()
                                except ValueError:
                                    print('Input error')
                                buildTableClassifiers()
                            else:
                                print("ID format incorrect")
                        except ValueError:
                            print("ID format incorrect")
                    elif cmd2[0] == str(3):
                        try:
                            id = int(cmd2[1][1:])
                            if cmd2[1][:1] == '-' and id:
                                incorrect = True
                                while incorrect:
                                    a = raw_input("Delete Classifier with ID " + str(id) + "? [y/n]: ")
                                    # a = input("Delete Classifier with ID " + str(id) + "? [y/n]: ")
                                    if a == 'y':
                                        lock.acquire()
                                        try:
                                            query = "Delete From Classifier Where ClassifierID=%d" % id
                                            cursor.execute(query)
                                            cursor.commit()
                                        except pyodbc.DatabaseError:
                                            print("ID not found")
                                        finally:
                                            lock.release()
                                        buildTableClassifiers()
                                        incorrect = False
                                    elif a == 'n':
                                        incorrect=False
                                    else:
                                        print("Input error")

                        except ValueError:
                            print("ID format incorrect")
                    elif cmd2[0] == str(4):
                        menu = False
                    else:
                        print("Option not available")
                except IndexError:
                    print()
        # MODEL
        elif cmd1 == str(3):
            lock.acquire()
            try:
                buildTableModel()
            except pyodbc.DatabaseError:
                print("Could not load table")
            finally:
                lock.release()
            menu = True
            while menu:
                print("MENU")
                print("1 ADD Model")
                print("2 Change Model [-ID]")
                print("3 Delete Model [-ID]")
                print("4 Back")
                cmd3 = raw_input("Enter digit: ").split()
                # cmd3 = input("Enter digit: ").split()
                try:
                    if len(cmd3) == 1 and (cmd3[0] != '1' and cmd3[0] != '4'):
                        print("Please choose the ID of the Classifier (e.g. -1)")
                    elif cmd3[0] == str(1):
                        try:
                            name = raw_input("Name: ")
                            # name = input("Name: ")
                            lock.acquire()
                            try:
                                query = "INSERT INTO Model ( Description ) VALUES ('%s')" % name
                                cursor.execute(query)
                                cursor.commit()
                            except pyodbc.DatabaseError:
                                print("Insert failed")
                            finally:
                                lock.release()
                        except ValueError:
                            print('Input error')
                        buildTableModel()

                    elif cmd3[0] == str(2):
                        try:
                            id = int(cmd3[1][1:])
                            if cmd3[1][:1] == '-' and id:
                                try:
                                    name = raw_input("Name: ")
                                    # name = input("Name: ")
                                    lock.acquire()
                                    try:
                                        query = "UPDATE Model Set Description = '%s' where ModelID = %d" % (name, id)
                                        cursor.execute(query)
                                        cursor.commit()
                                    except pyodbc.DatabaseError:
                                        print("ID not found")
                                    finally:
                                        lock.release()
                                except ValueError:
                                    print('Input error')
                                buildTableModel()
                            else:
                                print("ID format incorrect")
                        except ValueError:
                            print("ID format incorrect")
                    elif cmd3[0] == str(3):
                        try:
                            id = int(cmd3[1][1:])
                            if cmd3[1][:1] == '-' and id:
                                incorrect = True
                                while incorrect:
                                    a = raw_input("Delete Model with ID " + str(id) + "? [y/n]: ")
                                    # a = input("Delete Model with ID " + str(id) + "? [y/n]: ")
                                    if a == 'y':
                                        lock.acquire()
                                        try:
                                            query = "Delete From Model Where ModelID=%d" % id
                                            cursor.execute(query)
                                            cursor.commit()
                                        except pyodbc.DatabaseError:
                                            print("ID not found")
                                        finally:
                                            lock.release()
                                        buildTableModel()
                                        incorrect = False
                                    elif a == 'n':
                                        incorrect = False
                                        buildTableModel()
                                    else:
                                        print("Input error")

                        except ValueError:
                            print("ID format incorrect")
                    elif cmd3[0] == str(4):
                        menu = False
                    else:
                        print("Option not available")
                except IndexError:
                    print()
        # QUIT
        elif cmd1 == str(4):
            alive = False
        else:
            print("Option not available")
except KeyboardInterrupt:
    print("\nProgram shut down forcefully")
finally:
    alive = False
    Transientstream.join()
    Alertstream.join()
    DataBasestream.join()
    cursor.close()
    cnxn.close()
#
