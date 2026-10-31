# That script was created to test reading the paths and its files in many folders
# It may be useful, so I'll keep it here

import os

rootdir = 'output'

for subdirs, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".txt"):
            print(os.path.join(subdirs, file))
