import sys, csv, cs50

if len(sys.argv) != 2:
    exit()

with open(sys.argv[1], "r") as file:
    reader = csv.reader(file);
    line_count = 0
    db = cs50.SQL("sqlite:///students.db")
    for line in reader:
        if line_count == 0:
            line_count += 1
            continue
        name = line[0]
        names = [""]
        i = 0
        j = 0
        while i < len(name):
            if (name[i] != ' '):
                names[j] += name[i]
            else:
                names.append("")
                j += 1
            i += 1
        firstName = names[0]
        lastName = names[-1]
        middleName = ""
        if len(names) == 3:
            middleName = names[1]
        house = line[1]
        birth = int(line[2])
        if middleName == "":
            db.execute("INSERT INTO students (first, last, house, birth) VALUES (?, ?, ?, ?);", firstName, lastName, house, birth);
        else:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?);", firstName, middleName, lastName, house, birth);


