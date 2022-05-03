list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']

presentboth = []
unique = []

#check if elements from list_a are in list_b
#if they are, add to presentboth
#if they aren't, add to unique
for i in list_a:
    if i in list_b:
        presentboth.append(i)
    else:
        unique.append(i)

#check if elements from list_b are not in the presentboth list
#if they aren't, add to unique list
for i in list_b:
    if i not in presentboth:
        unique.append(i)

print(presentboth)
print(unique)
