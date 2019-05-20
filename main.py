from __future__ import division
import sys, os, datetime, pickle
import fileutils as fl
import controller as CR
import utils
import parameters

cwl = os.getcwd()

def parseInput(fileLoc):
    data = fl.readLinesAndSplit(fileLoc, ',')
    KEYS = []
    NAMES = []
    for entry in data:
        if utils.validate_linkedIn_URL(entry[0]) == 0:
            KEYS.append(entry[0])
        else:
            NAMES.append(entry[0])
    return KEYS, NAMES

#def queryNameUrls(NAMES):

def execute(KEYS):
    H, I = CR.executeSCAP(KEYS)
    H_, I_, C, D = CR.executeCMapper(H, I)
    Clusters = CR.executeCVF(H_, I_, C, D)

if __name__=="__main__":
    script, inputfile = sys.argv
    K, N = parseInput(inputfile)
#    queryNameUrls(N)
    execute(K)
   
