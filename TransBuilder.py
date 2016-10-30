from random import randint

trans = ["star", "black hole", "supernova", "nova", "flare star", "meteoroid", "asteroid", "comet"]

# for i in range(1, 5):
#    x = randint(0, 7)
#    print(i, "-", trans[x], sep="")

# print("time: ", time.ctime())

i = 0
while i < 10:
    file_name = str(i) + ".txt"
    file = open(file_name, 'w+')
    file.write(str(randint(1000, 2000)) + " " + str(randint(0, 10)) + " " + str(randint(0, 100)))
    file.close()
    i += 1

