import os
import time
import json
import random
import platform
import re
import sys
from zipfile import ZipFile


isLinux = False

def main():
    # var
    global isLinux
    #init
    
    os.chdir(sys.argv[1])
    if platform.system() == 'Linux':
       isLinux = True
    random.seed(time.time())
    
    solutionFile = os.listdir('solution')
    
    if os.path.isdir('testcase'):
        file = os.listdir('testcase')
        os.chdir('testcase')
        for name in file:
            os.remove(name)
        os.chdir('..')
    else:   
        os.mkdir('testcase')
    #compilation
    if isLinux:
        os.system("g++ generator.cpp -o testcase/generator.exe")
    else:
        os.system("g++ generator.cpp -o testcase\\generator.exe")
    print("Generator compiled")
    if isLinux:
        os.system("g++ validator.cpp -o testcase/validator.exe")
    else:
        os.system("g++ validator.cpp -o testcase\\validator.exe")
    print("Validator compiled")
    for solution in solutionFile:
	    if solution.endswith('.c') or solution.endswith('.cpp'):
       		 if isLinux:
            		cmdLine = 'g++ solution/' + solution + ' -o testcase/' + solution[:-4] + '.exe'
       		 else:
            		cmdLine = 'g++ solution\\' + solution + ' -o testcase\\' + solution[:-4] + '.exe'
       		 os.system(cmdLine)
    print("Compilation End")
    #load json file
    
    with open('data.json') as f:
        jsonFile = json.load(f)
    
    testcasePatternFile = list(jsonFile['subtasks'])

    #Generate testcase
    os.chdir('testcase')
    subtask = 1
    for timeOfRun in jsonFile['no_subtasks']:
        cmdLine = "generator.exe " + str(subtask) + ' ' + str(timeOfRun) +' ' + str(random.randint(0 , 25565)) 
        if isLinux:
            cmdLine = './' + cmdLine
        os.system(cmdLine)
        subtask += 1
    print("Generation Done")
    
    #Validate testcase
    subtask -= 1
    TCfile = []
    TCfile = os.listdir(os.getcwd())
    
    inputFile = []
    
    for i in range(subtask):
        fileList = []
        Patteren = testcasePatternFile[i][1]
        testcasePattern = re.compile(Patteren)
        for fileName in TCfile:
            if testcasePattern.match(fileName) and fileName.endswith(".in"):
                fileList.append(fileName)
                inputFileName = fileName
                cmdLine = "validator.exe " + str(i + 1) + " <" + inputFileName
                if isLinux:
                    cmdLine = "./" + cmdLine
                
                print('current file %s' % inputFileName)
                os.system(cmdLine)  
        inputFile.append(fileList)
    print("Validation Done")
    
    #Generate answer
    for fileName in TCfile:
        if fileName.endswith(".in"):
            print('creating answer for %s' % fileName)
            ansFile = fileName[:-3] + ".ans"
            inputFileName = fileName
            cmdLine = "main_solution.exe <" + inputFileName + " >" + ansFile
            if isLinux:
                cmdLine = "./" + cmdLine
            os.system(cmdLine)
    print("Answer Done")   

    print('-----------------------------')
    #Run Subtask
    for solutionName in solutionFile: #different solution
        subtask = 1
        print("%s:"  % (solutionName))
        
        
        
        for subtaskFile in inputFile: #subtask X
            subtaskPass = 0
            totalsubtask = 0
            allpass = True
            print('---subtask %d:' % subtask , end = ' ')
            for inputFileName in subtaskFile: #File in subtask X
                cmdLine = solutionName[:-4] + '.exe <' + inputFileName + ' >output.out'
                if isLinux:
                    cmdLine = './' + cmdLine
                os.system(cmdLine)
                
                original = open(inputFileName[:-3] + '.ans' , 'r')
                subAnswer = open('output.out' , 'r')

                subAnswerList = []
                originalList = []

                for line in original:
                    if line != "\n":
                        line = line.rstrip()
                        originalList.append(line)

                for line in subAnswer:
                    if line != "\n":
                        line = line.rstrip()
                        subAnswerList.append(line)
                
                subAnswer.close()
                original.close()

                if subAnswerList == originalList:
                    difference = False
                else:
                    difference = True

                if difference:
                    allpass = False
                else:
                    subtaskPass += 1
                totalsubtask += 1
            
            if allpass:
                print('Pass' , end = ' ')
            else:
                print('Fail' , end = ' ')
            print('%d / %d testcase(s) pass' % (subtaskPass , totalsubtask))
            subtask += 1
      

    #remove useless file
    os.remove('output.out')
    for solutionName in solutionFile:
        Name = solutionName[:-4] + '.exe'
        os.remove(Name)
    os.remove('generator.exe')
    os.remove('validator.exe')
    
    #zip file
    zipobj = ZipFile('testcase.zip' , 'w')
    for Name in TCfile:
        if Name.endswith('in'):
            zipobj.write(Name)
            zipobj.write(Name[:-3] + '.ans')
    zipobj.close()

    #information
    print('Author: %s' % jsonFile['author'])
    print('Timelimit: %.1f second(s)' % jsonFile['time'])
    print('ALL DONE')
    
            
if __name__ == "__main__":
    main()
#watch?v=dQw4w9WgXcQ

