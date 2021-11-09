import os
from os import listdir
import pandas as pd
import matplotlib.pyplot as plt

filename = str(input("Filename: "))
z = int(input("Number of aquisitions: "))

folder = filename[:-23] + "_asc_files"

try:
    os.mkdir(folder)
except:
    pass
# Separate the raw file in many files (the two windows aquisition are in diferent files)

with open(filename) as file:

    new_line = ""
    c = 1
    for line in file.read().split("\n")[4:]:
        if (line == ""):
            with open(folder + "/" + str(c) + ".asc", "w") as text:
                text.write(new_line)
                text.close()
                new_line = line
                c += 1

        else:
            if new_line == "":
                new_line = line
            else:
                new_line = new_line + "\n" + line
    file.close()


# Append the second window data file in the final of the first window data file

for i in range(2, z*2+1, 2):

    with open(file=(folder + "/" + str(i) + ".asc"), mode="r") as file:
        filedata = file.read().split("\n")

    with open(file=(folder + "/" + str(i-1) + ".asc"), mode="a") as file:
        for line in filedata[10:]:
            file.write("\n" + line)

 # Delete the files which were copyed
    os.remove(folder + "/" + str(i) + ".asc")


# Reading and rewriting the same content. It was used just to rename the files to a continuous enumeration.
n = 2
for i in range(3, z*2, 2):

    with open(file=(folder + "/" + str(i) + ".asc"), mode="r") as file:
        filedata = file.read()

    with open(file=(folder + "/" + str(n) + ".asc"), mode="w") as file:
        file.write(filedata)
# Delete the files which were copyed from
    os.remove(folder + "/" + str(i) + ".asc")
    n += 1

files = []
for file in listdir(folder):
    if file.endswith(".asc"):
        files.append(file)


for file in files:
    df = pd.read_csv(folder + "/" + file, skiprows=10,
                     delim_whitespace=True, header=None).astype(float)
    df = df.drop(1, 1)
    if int(file[:-4]) < 10:
        df.to_csv(folder + "/000" + file, index=False, sep=" ")
    if (int(file[:-4]) >= 10) & (int(file[:-4]) < 100):
        df.to_csv(folder + "/00" + file, index=False, sep=" ")
    if (int(file[:-4]) >= 100) & (int(file[:-4]) < 1000):
        df.to_csv(folder + "/0" + file, index=False, sep=" ")
    if (int(file[:-4]) >= 1000) & (int(file[:-4]) < 10000):
        df.to_csv(folder + "/" + file, index=False, sep=" ")

# Delete the files which were copyed from
for i in range(1, z+1):
    os.remove(folder + "/" + str(i) + ".asc")
