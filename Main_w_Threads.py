import threading
import pyodbc
import os


def buildTableClassifiers():
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
            name = "Lyrae"

            query = "Select TransientID From Transient Where Class='%s' AND Location = %d" %(name, loc)

            cursor.execute(query)
            row = cursor.fetchone()
            t = row[0]
            if not t:
                cursor.execute("Insert into Transient ( Class, Location, ModelID, ClassifiedWith ) VALUES ('%s', %d, '1', '1'" %(name, loc))
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
            print("rip")
        finally:
            lock.release()
            # time.sleep(0.1)


# create a thread that runs the daemon_receive_alerts method
Alertstream = threading.Thread(name='Alertstream', target=daemon_receive_alerts)
# set the thread as a daemon so it runs constantly in the background
Alertstream.setDaemon(True)
# run the thread
#Alertstream.start()

# being MAIN LOOP
# MAIN LOOP
alive = True
try:
    while alive:
        print("MENU")
        print("1 Classify Transients")
        print("2 Show Classifiers")
        print("3 Show Models")
        print("4 Quit")
        cmd1 = input()

        if cmd1 == str(1):
            print("Choose File")
        elif cmd1 == str(2):
            lock.acquire()
            try:
                buildTableClassifiers()
            except pyodbc.DatabaseError:
                print("rip")
            finally:
                lock.release()
            menu = True
            while menu:
                print("MENU")
                print("1 ADD Classifier")
                print("2 Change Classifier [-ID]")
                print("3 Delete Classifier [-ID]")
                print("4 Back")
                cmd2 = input().split()

                try:
                    if len(cmd2) == 1 and (cmd2[0] != '1' and cmd2[0] != '4'):
                        print("Please choose the ID of the Classifier")
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
                                        query = "UPDATE Classifier Set Name = '%s', Min = %d,  Max = %d where ClassifierID = %d" %(name, min, max, desc)
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
        elif cmd1 == str(3):
            print("Choose File")
        elif cmd1 == str(4):
            alive = False
        else:
            print("Option not available")
finally:
    cursor.close()
    cnxn.close()
#
