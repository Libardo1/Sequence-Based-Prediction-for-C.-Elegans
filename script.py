# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:06:23 2016

@author: SYARLAG1
"""
import os
import numpy as np
import pandas as pd

os.chdir('C:/Users/SYARLAG1/Desktop/Sequence-Based-Prediction-for-C.-Elegans') #change this to where you hold your data. Also note the way the data is saved

dataRaw = pd.read_csv('./movementData.csv',usecols = [2,3]) #only selected the last two cols

def genPairPermutations(uniqueSet):
    permutationLst = []
    for i in uniqueSet:
        for j in uniqueSet:
            permutationLst.append((i,j))
    return permutationLst

def createProbMatrix(data = dataRaw): 
    seqLst = []
    for i in range(data.shape[0]):
        seqLst.append(str(data.iloc[i,0]+' '+data.iloc[i,1]))
    seqSet = set(seqLst)
    permutationLst = genPairPermutations(seqSet)
    probDict = {str(x):[0 for i in range(len(permutationLst)) ] for x in seqSet}
    countMatrix = pd.DataFrame(data=probDict, index = permutationLst)  
    for index, seq in enumerate(seqLst[1:len(seqLst)]):
        for permutation in permutationLst:
            if (seqLst[index-1], seqLst[index]) == permutation:
                for key in probDict.keys():
                    if index + 1 > len(seqLst): break
                    if seqLst[index+1] == key:
                        countMatrix[key][permutation] += 1
    probMatrix = countMatrix.apply(lambda c: c / c.sum() if c.sum() > 0 else 0, axis=1)
    return probMatrix

createProbMatrix(data=dataRaw).to_csv('./result.csv')
