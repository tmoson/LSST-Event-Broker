from random import randint

trans = ["star", "black hole", "supernova", "nova", "flare star", "meteoroid", "asteroid", "comet"]

for i in range(0, 11):
    #  x = randint(0, 7)
    print(randint(100, 2400), '-', i, '-', randint(0, 20), sep="")
    print(randint(100, 2400), '-', i, '-', randint(0, 20), sep="")
    print(randint(100, 2400), '-', i, '-', randint(0, 20), '\n', sep="")

#  print("time: ", time.ctime())

i = 11
while i < 10:
    file_name = str(i) + ".txt"
    file = open(file_name, 'w+')
    file.write(str(randint(1000, 2000)) + "-" + i + "-" + str(randint(0, 100)))
    file.close()
    i += 1

