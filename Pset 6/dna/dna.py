import csv, sys

col_names = []
data = []
idx = 0
with open(sys.argv[1]) as database:
    databaseReader = csv.reader(database, delimiter=",")
    line_count = 0
    for row in databaseReader:
        if line_count == 0:
            col_names = row
            line_count += 1
        else:
            data.append(row)
            line_count += 1
sequence = ""
with open(sys.argv[2]) as seq:
    seqReader = csv.reader(seq, delimiter=",")
    for row in seqReader:
        for c in row:
            if (c != '\n'):
                sequence += c

count = 0
number = []
for dna in col_names:
    if (count == 0):
        count += 1
        continue
    occ = 0
    mxOcc = -1
    i = 0
    while i < len(sequence):
        if sequence[i : i + len(dna)] == dna:
            occ += 1
            i += len(dna)
        else:
            mxOcc = max(mxOcc, occ)
            occ = 0
            i += 1
    number.append(mxOcc)

count = 0
seqCount = 0
found = False
for person in data:
    isTrue = True
    seqCount = 0
    count = 0
    for field in person:
        if (count == 0):
            count += 1
            continue
        if (field != str(number[seqCount])):
            isTrue = False
        seqCount += 1
    if isTrue:
        print(person[0])
        found = True
        break
if (found == False):
    print("No match")






