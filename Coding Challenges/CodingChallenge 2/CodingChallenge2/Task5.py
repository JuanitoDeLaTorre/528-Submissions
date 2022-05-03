letter_scores = {
    "aeioulnrst": 1,
    "dg": 2,
    "bcmp": 3,
    "fhvwy": 4,
    "k": 5,
    "jx": 8,
    "qz": 10
}

while(True):
    word = input("Gimme a word pls: ")

    if(str(word) in letter_scores):
        print("The score for that (totally legitimate) word is " + str(letter_scores[str(word)]))
        break
    else:
        print("Hmm...that word isn't in the dictionary. Try again.\n")

