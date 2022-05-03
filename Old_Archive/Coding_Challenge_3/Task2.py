import sys

newlist = []

newlist.extend((sys.argv[1],sys.argv[2],sys.argv[3]))

print("\nTime to reverse our arguments!\n")

for i in newlist:
    print(i[::-1])