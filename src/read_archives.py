
# That script was created for moving only the necessary original files that I needed from CSTCorpus.
# By now, it does nothing, but it is pretty nice to have it, if one day it is nedded to copy
# a large quantity of files to one folder to another

# The commit for it was: Extract the useful files for the work in progress

import os, fnmatch

rootdir = 'experiments'

for subdirs, dirs, files in os.walk(rootdir):
    for dir in fnmatch.filter(dirs, "Textos-fonte"):
        if not os.path.exists('output/'+subdirs):
            os.makedirs('output/'+subdirs)
    f = open('output/'+subdirs+'/original.txt', 'w+')
    for file in os.listdir(os.path.join(subdirs, dir)):
        with open(os.path.join(subdirs, dir, file), 'r') as fin:
            f.write(fin.read())
    f.close