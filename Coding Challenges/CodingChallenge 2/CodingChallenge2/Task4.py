age = input("What is your age? ")

tillretire = 0

if(int(age) < 65):
    tillretire = 65 - int(age)
    print("You have " + str(tillretire) + " years left to retirement. Hang in there!")
else:
    tillretire = int(age) - 65
    print("You should've retired " + str(tillretire) + " years ago!")

