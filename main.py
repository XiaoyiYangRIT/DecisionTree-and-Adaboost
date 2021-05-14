"""
Lab2
train train.dat dt dt
predict Output/dt test.dat
train train.dat ada ada
predict Output/ada test.dat

Author: Xiaoyi Yang
"""

import sys
import time
from Functions import decisionTree as dt
from Functions import adaboost as ada
from Functions import serialization as se
from Models import features as fe

class WikipediaLanguageClassification:
    """
    Class: WikipediaLanguageClassification
    """
    # Operation Constents
    TRAIN = "train"
    PREDICT = "predict"
    EXIT = "exit"
    
    # Type of learning algorithm
    DECISION_TREE = "dt"
    ADABOOST = "ada"
    
    def main(self):
        """
        The main program
        """
        while(True):
            print("\nThis is the program for Wikipedia Language Classification:")
            print("1. train <examples> <hypothesisOut> <learning-type(dt: Decision Tree; ada: Adaboost;)>")
            print("2. predict <hypothesis> <file>")
            print("3. exit")
            task = input("What are you going to do?\n").split(" ")
            if(task[0] == self.TRAIN):
                if(len(task) == 4):
                    self.training(task[1], task[2], task[3])
                    print("Hypothesis generated and saved in 'Output/" + task[2] + "'")
                else:
                    print("Argument Number Error: 'train' should be followed by 3 arguments.\n")
            elif(task[0] == self.PREDICT):
                if(len(task) == 3):
                    self.predicting(task[1], task[2])
                else:
                    print("Argument Number Error: 'predict' should be followed by 2 arguments.")
            elif(task[0] == self.EXIT):
                print("Bye.")
                sys.exit()
            else:
                print("Error: invalid operation.\n")
    
    def training(self, trainfile, hypo, learning):
        """
        Training function, read and formalize the input text, 
        then call the learn function and serialize the hypothesis
        :param trainfile: The input training file
        :param hypo: The file name of output file for generated hypothesis
        :param learning: The learning type, dt-Decision Tree, ada-Adaboost
        """
        # Handle input
        trainData = []
        with open(trainfile, "r") as f:
            for example in f.readlines():
                temp = list(example.lstrip(' ').rstrip('\n').split("|"))
                
                # Turn the input data to the form used in learning process
                # examples is the formalized list
                examples = fe.formalize(temp[1])
                examples.append(temp[0])
                trainData.append(examples)
        
        # Learning
        if learning == self.DECISION_TREE:
            output = dt.learn(trainData)
            # mark the hypothesis as "dt", due to dt and ada will predict respectively
            output["type"] = "dt"
        elif learning == self.ADABOOST:
            while(True):
                print("\nHow many times do you want the learning process repeat?")
                times = input("Please fill a positive number: \n")
                if(times.isdigit()):
                    if(int(times) > 0):
                        break
                    else:
                        print("Error: Must type a positive number.")
                else:
                    print("Error: Must type an Interger. Not " + str(type(times)))
            output = ada.learn(trainData, int(times))
            output["type"] = "ada"
        else:
            print("Error: invalid training function.\n")
            return
        
        # Serialization
        se.pick(output, hypo)
        
        
    def predicting(self, hypo, testfile):
        """
        prediction function, take the generated hypothesis from the file
        predict the text from the input file
        :param hypo: The file name of input file for generated hypothesis
        :param testfile: The file of text to be predicted
        """
        model = se.unpick(hypo)
        if(model["type"] == "dt"):
            with open(testfile, "r") as f:
                for example in f.readlines():
                    # trim the data to be predicted
                    example = example.lstrip(' ').rstrip('\n')
                    # Formalize the data with boolean value
                    example = fe.formalize(example)
                    # predict and print out the outcome
                    dt.predict(example, model)
        elif(model["type"] == "ada"):
            with open(testfile, "r") as f:
                for example in f.readlines():
                    # trim the data to be predicted
                    example = example.lstrip(' ').rstrip('\n')
                    # Formalize the data with boolean value
                    example = fe.formalize(example)
                    # predict and print out the outcome
                    ada.predict(example, model)
        
def main():
    """The main routine."""
    # create a WLC instance and invoke the main loop
    WLC = WikipediaLanguageClassification()
    WLC.main()

if __name__ == "__main__":
    main()