wordsStr = 'hi dee hi how are you mr dee'

#split string based on ' ' character
wordsList = wordsStr.split(' ')

countList = []

#count instances of each element
for i in wordsList:
    countList.append(wordsList.count(i))

#print words and counts
for i in range(len(wordsList)):
    print(wordsList[i] + ": " + str(countList[i]))

