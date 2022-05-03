nums = [1, 2, 3, 6, 8, 12, 20, 32, 46, 85]
newnums = []

for i in nums:
    if i < 5:
        newnums.append(i)

print newnums

print([i for i in nums if i < 5])

