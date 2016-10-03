import os

rootdir = 'output'

for subdirs, dirs, files in os.walk(rootdir):
  for file in files:
    if file.endswith(".txt"):
     print(os.path.join(subdirs, file))
