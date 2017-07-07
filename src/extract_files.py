# That script was created for moving only the necessary files to my work from the CSTCorpus.
# By now, it does nothing, but it is pretty nice to have it, if one day it is nedded to copy
# a large quantity of files to one folder to another

# The commit for it was: Extract the useful files for the work in progress

import os, fnmatch

rootdir = 'experiments'

for subdirs, dirs, files in os.walk(rootdir):
    for dir in fnmatch.filter(dirs, "Sumarios"):
        if not os.path.exists('output/'+subdirs):
            os.makedirs('output/'+subdirs)
    fe = open('output/'+subdirs+'/extrato_humano.txt', 'w+')
    fs = open('output/'+subdirs+'/sumario_automatico_CSTSumm.txt', 'w+')
    for file in os.listdir(os.path.join(subdirs, dir)):
        if fnmatch.fnmatch(file, '*_extrato_humano.txt'):
            with open(os.path.join(subdirs, dir, file), 'r') as fin:
                fe.write(fin.read())
        elif fnmatch.fnmatch(file, '*_sumario_automatico_CSTSumm.txt'):
            with open(os.path.join(subdirs, dir, file), 'r') as fin:
                fs.write(fin.read())