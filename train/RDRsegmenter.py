# -*- coding: utf-8 -*-

import os
import sys
os.chdir("../")
sys.setrecursionlimit(100000)
sys.path.append(os.path.abspath(""))
os.chdir("./train")

from multiprocessing import Pool
from SCRDRlearner.Object import FWObject, getWordTag
from SCRDRlearner.SCRDRTree import SCRDRTree
from SCRDRlearner.SCRDRTreeLearner import SCRDRTreeLearner
from Utility.Config import NUMBER_OF_PROCESSES, THRESHOLD

def printHelp():
    print("\n===== Train ====="  )
    print('\ntrain$ python RDRsegmenter.py train PATH-TO-GOLD-SEGMENTATION-TRAINING-CORPUS.BI PATH-TO-TRAINING-CORPUS.RAW.Init')
    print('\nExample: \n\ntrain$ python RDRsegmenter.py train Train_gold.txt.BI Train_gold.txt.RAW.Init')

def run(args = sys.argv[1:]):
    print(args)
    print(THRESHOLD)
    if (len(args) == 0):
        printHelp()
    elif args[0].lower() == "train":
        try:
            print("\n===== Start =====")
            print('\nLearn a tree model of rules from %s and %s ' % (args[1], args[2]))         
            rdrTree = SCRDRTreeLearner(THRESHOLD[0], THRESHOLD[1])
            print('threshold')
            rdrTree.learnRDRTree(args[2], args[1])
            print("Step 2")
            print("\nWrite the learned tree model to file ", args[2] + ".RDR")
            
            rdrTree.writeToFile(args[2] + ".RDR")        

            print('\nDone!')
        except Exception as e:
            print("\nERROR ==> ", e)
            printHelp()      
    else:
        printHelp()
if __name__ == "__main__":
    #print(sys.argv)
    rdrTree = SCRDRTreeLearner(THRESHOLD[0], THRESHOLD[1])
    rdrTree.learnRDRTree(r'D:\src\rdr\train\Train_gold.txt.BI', r'D:\src\rdr\train\Train_gold.txt.RAW.Init' )
    #run()