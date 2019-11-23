from sys import argv

run, filename = argv

a = {'1': "mammal", '2': 'bird', '3': 'reptile', '4': 'fish', '5': 'amphibian', '6': 'insect', '7': 'invertebrate'}

f = open(filename)
lines = f.readlines()
f.close()
f = open(filename, 'w')
for line in lines:
    line = line.split(",")
    line = ",".join(line[1:])
    f.write(line)
f.close()