from sys import argv

run, filename = argv

a = {'1': "mammal", '2': 'bird', '3': 'reptile', '4': 'fish', '5': 'amphibian', '6': 'insect', '7': 'invertebrate'}
b = {'1': "No use", '3': "Short-term", '2': "Long-term"}

f = open(filename)
lines = f.readlines()
f.close()
f = open(filename, 'w')
for line in lines:
    f.write(line[:-2] + b[line[-2]] + '\n')
f.close()