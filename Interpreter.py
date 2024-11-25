# University Name: Kennesaw State University
# College: College of Computing and Software Engineering
# Department: Department of Computer Science
# Course: CS 4308
# Course Title: Concepts of Programming Languages
# Section: W01
# Term: Spring 2020
# Instructor: Dr. Jose Garrido
# Student Name: John Foster, Kindra Hensley, Zander Bandoly
# Student Email: jfost103@students.kennesaw.edu, khensle1@students.kennesaw.edu, abandol1@students.kennesaw.edu
# Assignment: Module 5 - 3rd Project Deliverable
# Date: 03/16/2020

# The interpreter takes in the Lexeme and Token lists passed from Parser.py and interprets these lists into a usable python program.

import sys
import copy
import Scanner
import Parser

# This is an implementation of the interpreter that will be called upon in the Scanner.Scan method after the Parser has
# completed it checks and the Scanner has successfully created the Lexeme and Token lists.

def Interpret(wList, tList):

    # Keep track of identifiers and Values
    globalVarsPosition = []
    globalVarsIdentity = []
    globalVarsNumber = []

    # Treat these lists as stacks for 'for' loops
    forAssignmentStart = []
    toAssignmentEnd = []

    printWordList = wList.copy()
    flagList = wList.copy()

    # Set Flags
    for i in range(len(wList)):
        if tList[i] == "INT_LIT" or tList[i] == "Operation" or tList[i] == "Digit" or tList[i] == "Reserved Word" or tList[i] == "String Literal":
            flagList[i] = True
        else:
            flagList[i] = False

    ######################################################################
    # Start Main Loop to run through wList[i]
    ######################################################################
    i = 0
    while i < len(wList):

        if wList[i] == "for":
            # Needs to handle Inputs, Prints, Next and nested For Loops
            i = handleFor(i, wList, tList, flagList, globalVarsIdentity, globalVarsNumber, globalVarsPosition, forAssignmentStart, toAssignmentEnd, printWordList)
        elif wList[i] == "print":
            handlePrint(i, wList, tList, flagList, globalVarsIdentity, globalVarsNumber, globalVarsPosition, printWordList)
        elif wList[i] == "input":
            handleInput(i, wList, flagList, globalVarsIdentity, globalVarsNumber, globalVarsPosition, printWordList)

        i+=1

    ######################################################################
    # End Main Loop to run through wList[i]
    ######################################################################

    ######################################################################
    # Testing
    ######################################################################
    '''print(globalVarsIdentity)
    print(globalVarsNumber)
    print(globalVarsPosition)
    print("Start For:",forAssignmentStart)
    print("End For:",toAssignmentEnd)
    for i in range(len(wList)):
        print(i,": ", flagList[i], wList[i], printWordList[i],  tList[i])'''
    ######################################################################
    # Testing
    ######################################################################

######################################################################
# Handles For loops
# Needs i = position of 'for'
######################################################################
def handleFor(i, wList, tList, flagList, globalVarsIdentity, globalVarsNumber, globalVarsPosition, forAssignmentStart, toAssignmentEnd, printWordList):

    # Sets globalVars
    tempPos = i+2
    handleEqual(tempPos, wList, tList, flagList, globalVarsIdentity, globalVarsNumber, globalVarsPosition, forAssignmentStart, toAssignmentEnd, printWordList)

    currentForPosition = i+6
    currentNextPosistion = i+6

    # get the Next Position
    while currentNextPosistion < len(wList):
        if wList[currentNextPosistion] == "next":
            break
        currentNextPosistion += 1

    finalNextPosition = currentNextPosistion

    # Loop for id to id
    for assign in range(int(forAssignmentStart[-1]), int(toAssignmentEnd[-1])+1):
        # Loop for -- next
        for w in range(currentForPosition, currentNextPosistion):
            if wList[w] == "print":
                handlePrint(w, wList, tList, flagList, globalVarsIdentity, globalVarsNumber, globalVarsPosition, printWordList)

        # Update all next 'id' from For start to end
        theForStartsAt = i + 6
        while theForStartsAt < len(wList):
            if wList[theForStartsAt] == wList[i+1]:
                printWordList[theForStartsAt] = int(printWordList[theForStartsAt])+1
            theForStartsAt += 1

    forAssignmentStart.pop()
    toAssignmentEnd.pop()

    return (finalNextPosition+2)

######################################################################
# Gets User inputs
# Needs i = position of 'input'
######################################################################
def handlePrint(i, wList, tList, flagList, globalVarsIdentity, globalVarsNumber, globalVarsPosition, printWordList):
    # <Print_Statement> -> print <id> | print <id> , <id> * <id> | print <String_Literal>

    ################################
    # Handle String Literals
    # <Print_Statement> -> print <String_Literal>
    ################################
    if printWordList[i] == "print" and tList[i+1] == "String Literal":
        printString = printWordList[i+1]
        print(printString[1:-1])

    ################################
    # Handle Identifiers
    # <Print_Statement> -> print <id> | print <id>, <id> * <id>
    ################################
    if printWordList[i] == "print" and tList[i+1] != "String Literal":

        ###########
        # <Print_Statement> -> print <id>
        ###########
        if flagList[i+1] == False and tList[i+2] == "INT_LIT":
            print("Error: Value ",printWordList[i+1]," not assigned")
            sys.exit('')
        if flagList[i+1] == True and tList[i+2] == "INT_LIT":
            print(printWordList[i+1])
            return

        ###########
        # <Print_Statement> -> print <id>, <id> * <id>
        ###########
        tempPrintPos = i
        while tList[tempPrintPos] != "INT_LIT":
            if tList[tempPrintPos] == "Digit" or tList[tempPrintPos] == "Identifier":
                if tList[tempPrintPos+1] == "Identifier" and tList[tempPrintPos+2] != "INT_LIT":
                    if flagList[tempPrintPos] == False:
                        print("Error: Value ", printWordList[tempPrintPos], " not assigned")
                        sys.exit('')

                #######
                # <id>, <id> * <id>
                #######
                if tList[tempPrintPos+4] == "INT_LIT":
                    if tList[tempPrintPos + 3] == "Digit" or tList[tempPrintPos + 3] == "Identifier":
                        if tList[tempPrintPos+2] == "Operation" and flagList[tempPrintPos+1] == True:
                            if tList[tempPrintPos+1] == "Digit" or tList[tempPrintPos+1] == "Identifier":
                                if flagList[tempPrintPos+3] == True:
                                    tempVal1 = int(printWordList[tempPrintPos+1])
                                    tempVal2 = int(printWordList[tempPrintPos+3])
                                    tempCalcVal = tempVal1 * tempVal2
                                    print(printWordList[tempPrintPos]," ", tempCalcVal)
                                    return

                                else:
                                    print("Error: Value ", wList[tempPrintPos + 3], " not assigned")
                                    sys.exit('')
                        else:
                            print("Error: Value ", wList[tempPrintPos+1], " not assigned")
                            sys.exit('')
                    else:
                        print("Error: Value ", wList[tempPrintPos+3], " needs to be a digit or identifier")
                        sys.exit('')

                #######
                # <id>, <id> <id>
                #######
                if tList[tempPrintPos+3] == "INT_LIT":
                    if tList[tempPrintPos+2] == "Digit" or tList[tempPrintPos+2] == "Identifier":
                        if flagList[tempPrintPos+2] == True:
                            # Need to remove * from id
                            tempVal = printWordList[tempPrintPos+1]
                            tempVal = tempVal[0:-1] # Remove '*' when <id>  like id*

                            # Run through Global Var Lists to either exit program or assign value and do calc
                            tempFlag = False
                            for g in reversed(range(len(globalVarsIdentity))):
                                if tempVal == globalVarsIdentity[g] and tempPrintPos > globalVarsPosition[g]:
                                    print(globalVarsNumber[g])
                                    print(tempVal)
                                    printWordList[tempPrintPos+1] = globalVarsNumber[g]
                                    tempFlag = True
                                    return
                            # Did not find tempVal in Global list vars so error out
                            if tempFlag == False:
                                print("Error: ", tempVal, " has not been assigned")
                                sys.exit('')

                            # Values are assigned
                            # Do Calcs
                            tempCalc1 = int(printWordList[tempPrintPos+2])
                            tempCalc2 = int(printWordList[tempPrintPos+1])
                            tempCalcVal = tempCalc1 * tempCalc2
                            print(printWordList[tempPrintPos], " ", tempCalcVal)

                        else:
                            print("Error: Value ", wList[tempPrintPos + 2], " not assigned")
                            sys.exit('')
                    else:
                        print("Error: Value ", wList[tempPrintPos+2], " needs to be a digit or identifier")
                        sys.exit('')

                #######
                # <id>, <id>
                #######
                if tList[tempPrintPos+2] == "INT_LIT":
                    if tList[tempPrintPos+1] == "Digit" or tList[tempPrintPos+1] == "Identifier":
                        # Need to break String by *
                        tempArray = printWordList[tempPrintPos+1].split('*')

                        # Loop through tempArray
                        tempFlag = False
                        for t in range(len(tempArray)):
                            # Loop through Global Array
                            for g in reversed(range(len(globalVarsIdentity))):
                                if tempArray[t] == globalVarsIdentity[g] and tempPrintPos > globalVarsPosition[g]:
                                    tempFlag = True
                                    tempArray[t] = globalVarsNumber[g]
                            if tempFlag == False:
                                print("Error: ", tempArray[t], " has not been assigned")
                                sys.exit('')

                        # Loop through array and multiply everything
                        tempPrintCal = 1
                        for t in range(len(tempArray)):
                            tempPrintCal = tempPrintCal * int(tempArray[t])

                        print(printWordList[tempPrintPos], " ", tempPrintCal)
                        return
                    else:
                        print("Error: Value ", wList[tempPrintPos+1], " needs to be a digit or identifier")
                        sys.exit('')


            tempPrintPos += 1

    return

######################################################################
# Gets User inputs
# Needs i = position of 'input'
######################################################################
def handleInput(i, wList, flagList, globalVarsIdentity, globalVarsNumber, globalVarsPosition, printWordList):

    # Append Variables to Start of global lists
    tempID = printWordList[i+1]
    tempPos = i+1

    # Get a number from user input
    # Make sure it is an INT
    tempVal = inputNumber()

    # Insert Inputs into Global Vars
    globalVarsPosition.append(i+1)
    globalVarsNumber.append(tempVal)
    globalVarsIdentity.append(tempID)

    # Set first identity to value
    printWordList[i+1] = tempVal
    flagList[i + 1] = True

    # Run until ID is assigned again with either '=' or 'input'
    tempFlag = False
    while tempPos < len(printWordList):
        if printWordList[tempPos] == tempID and printWordList[tempPos+1] == "=":
            break
        elif printWordList[tempPos] == tempID and printWordList[tempPos-1] == "input":
            break
        if printWordList[tempPos] == tempID:
            printWordList[tempPos] = tempVal
            flagList[tempPos] = True
        tempPos += 1

    return

######################################################################
# Handles assignment '=' operations
# Needs i = position of '='
# Sets 'to' identifier and '=' identifier
# Appends these values to forAssignmentStart and toAssignmentEnd
######################################################################
def handleEqual(i, wList, tList, flagList, globalVarsIdentity, globalVarsNumber, globalVarsPosition, forAssignmentStart, toAssignmentEnd, printWordList):

    tempID = printWordList[i-1]
    tempPos = i+1
    tempNum = printWordList[i+1]

    # Insert Inputs into Global Vars
    globalVarsPosition.append(i)
    globalVarsNumber.append(printWordList[i+1])
    globalVarsIdentity.append(tempID)
    forAssignmentStart.append(printWordList[i+1])

    # Set first Identity to value
    printWordList[i-1] = printWordList[i+1]
    flagList[i-1] = True

    # Run until ID is assigned again with either '=' or 'input'
    while tempPos < len(printWordList):
        if printWordList[tempPos] == tempID and printWordList[tempPos+1] == "=":
            break
        elif printWordList[tempPos] == tempID and printWordList[tempPos-1] == "input":
            break

        if printWordList[tempPos] == tempID:
            printWordList[tempPos] = tempNum
            flagList[tempPos] = True
        tempPos += 1

    # Handle the to assignment Op
    if flagList[i+3] == False:
        print("Error: ", printWordList[i+3], "not assigned")
        sys.exit('')
    toAssignmentEnd.append(printWordList[i+3])
    return

######################################################################
# Check that user input is an INT
######################################################################
def inputNumber():
    while True:
        try:
            userInput = int(input())
        except ValueError:
            print("Not an integer. Try again...")
            continue
        else:
            return userInput
            break
