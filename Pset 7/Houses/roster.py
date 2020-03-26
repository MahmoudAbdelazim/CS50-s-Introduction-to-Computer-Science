import sys, cs50

if (len(sys.argv) != 2):
    exit()

db = cs50.SQL("sqlite:///students.db")
house = sys.argv[1]

data = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last ASC, first ASC", house)
firstNames = []
middleNames = []
lastNames = []
births = []
for dic in data:
    firstNames.append(dic["first"])
    middleNames.append(dic["middle"])
    lastNames.append(dic["last"])
    births.append(dic["birth"])
i = 0
while (i < len(firstNames)):
    if (middleNames[i] == None):
        print(f"{firstNames[i]} {lastNames[i]}, born {births[i]}")
    else:
        print(f"{firstNames[i]} {middleNames[i]} {lastNames[i]}, born {births[i]}")
    i += 1