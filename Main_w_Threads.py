import threading
import pyodbc
import os
import time

def buildTableClassifiers():
    lock.acquire()
    try:
        query = "Select ClassifierID, Name, Min, Max, Description From Classifier, Model Where Classifier.ModelID = Model.ModelID"
        cursor.execute(query)
        rows = cursor.fetchall()
        print("+----+---------------------+------+------+---------------------+")
        print("|\033[1m %2s \033[0m|\033[1m %19s \033[0m|\033[1m %4s \033[0m|\033[1m %4s \033[0m|\033[1m %19s \033[0m|" % (
            'ID', 'Name', 'Min', 'Max', 'Classifies'))
        print("|----+---------------------+------+------+---------------------|")
        for row in rows:
            print("|%4s| %20s| %5s| %5s| %20s|" % (row.ClassifierID, row.Name, row.Min, row.Max, row.Description))
        print("+----+---------------------+------+------+---------------------+")
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
db = os.getcwd() + "\EventBroker.accdb"
cnxn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+db)
# Opening a cursor
cursor = cnxn.cursor()
#queue = deque()
threads = []
alive = True
lock = threading.RLock()

# Thread that runs in the background
# Constantly stores the received alerts
def daemon_receive_alerts():
    while alive:
        lock.acquire()
        try:
            # Save loc and magnitude
            loc = 1
            magnitude = 1
            # Find right transient
            name = "fgjh"

            query = "Select TransientID From Transient Where Class='%s' AND Location = %d" %(name, loc)

            cursor.execute(query)
            row = cursor.fetchone()
            try:
                t = row[0]
            # If transient is not stored yet
            except TypeError:
                cursor.execute("Insert into Transient ( Class, Location, ModelID, LastClassifiedWith, Classified ) VALUES ('%s', %d, 1, 1, False)" % (name, loc))
                cursor.commit()
                cursor.execute(query)
                row = cursor.fetchone()
                t = row[0]

            # store Observation
            cursor.execute("INSERT INTO Observation ( Location, Magnitude, TransientID ) VALUES ( %d, %d, %d)" %(loc, magnitude, t))
            cursor.commit()
            # testing purpose
            # print("Alert received")
        except pyodbc.DatabaseError:
            print("Oberservation storage error")
        finally:
            lock.release()
            # time.sleep(0.1)

def daemon_send_transients():
    while alive:
        lock.acquire()
        try:
            query = "Select * From Transient Where Classified = True"
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
# run the thread
Alertstream.start()
Transientstream.start()

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
        cmd1 = input("Enter digit: ")

        if cmd1 == str(1):
            print("Choose File")
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
                cmd2 = input("Enter digit: ").split()

                try:
                    if len(cmd2) == 1 and (cmd2[0] != '1' and cmd2[0] != '4'):
                        print("Please choose the ID of the Classifier (e.g. -1)")
                    elif cmd2[0] == str(1):
                        try:
                            name = input("Name: ")
                            min = float(input("Minimum value: "))
                            max = float(input("Maximum value: "))
                            if min > max:
                                raise ValueError
                            desc = input("Transient model (string or ID): ")
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
                                query = "INSERT INTO Classifier ( Name, Min, Max, ModelID ) VALUES ('%s', %d, %d, %d)" % (name, min, max, desc)
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
                                    name = input("Name: ")
                                    min = float(input("Minimum value: "))
                                    max = float(input("Maximum value: "))
                                    if min > max:
                                        raise ValueError
                                    desc = input("Transient model (string or ID): ")
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
                                        query = "UPDATE Classifier Set Name = '%s', Min = %d,  Max = %d, ModelID = %d where ClassifierID = %d" %(name, min, max, desc, id)
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
                                    a = input("Delete Classifier with ID " + str(id) + "? [y/n]: ")
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
                cmd3 = input("Enter digit: ").split()

                try:
                    if len(cmd3) == 1 and (cmd3[0] != '1' and cmd3[0] != '4'):
                        print("Please choose the ID of the Classifier (e.g. -1)")
                    elif cmd3[0] == str(1):
                        try:
                            name = input("Name: ")
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
                                    name = input("Name: ")
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
                                    a = input("Delete Model with ID " + str(id) + "? [y/n]: ")
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
finally:
    Alertstream.join()
    cursor.close()
    cnxn.close()
#
