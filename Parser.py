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

# The Parser is called at the end of Scanner.scan function and passes the Lexeme and Token lists to this function
# Here we check the grammar and functionality of the scanned program for errors so that we can pass this into the
# interpreter. Once the grammar has passed, we pass the Lexeme and Token lists into the interpreter
'''
<Program> -> <Code> end
<Code> -> <Line><Code> | <Line>
<Line> -> <INT_LIT> <Statement>
<Statement> -> <For_Statement> | <Print_Statement> | <Next_Statement> | <Input_Statement>

<For_Statement> -> for <Boolean_Expression> to <id> <Code> <Next_Statement>
<Print_Statements> -> <Print_Statement> | <Print_Statement> <Print_Statements>
<Print_Statement> -> print <id> | print <id> , <id> * <id> | print <String_Literal>
<Next_Statement> -> next <id>
<Input_statement> -> input <id>

<Boolean_Expression> -> <id> = <Number>
<String_Literal> -> " <id> "
<id> -> Letter | Digit | <id><id>
<INT_LIT> -> <Number>
<Number> -> Digit | <Number>Digit

Lexical Analyzer
Letter -> [a-zA-Z]
Digit -> [0-9]
'''
import sys
import Scanner
import Interpreter

def parser(wList, tList):

    # <Line> -> <INT_LIT> <Statement>
    # <Statement> -> <For_Statement> | <Print_Statement> | <Next_Statement> | <Input_Statement>
    tokenCount = len(wList)
    lineCount = 0
    sysExitNum = False
    forCount = 0
    nextCount = 0

    #for x in range(tokenCount):
    #    print(x,": ",wList[x])

    for x in range(tokenCount):

        if wList[x] == "for":
            forCount += 1
        if wList[x] == "next":
            nextCount += 1

        # We first check to make sure the file is Ended properly
        if wList[tokenCount-1] != "end":
            print("Error at end of File: ** The file must end with the Reserved Word 'end' **")
            print("File: Parser.py, Line: 45")
            sysExitNum = True
            sys.exit('')
        # Check to make sure the Reserved Word 'end' is the last word
        if wList[x] == "end" and x != tokenCount-1:
            print("Error on line: " + str(lineCount) + " ** The Reserved Word 'end' denotes the end of file **")
            print("File: Parser.py, Line: 51")
            sysExitNum = True
        if tList[x] == "INT_LIT": # PARSER: Keep a line count for Error Handling
                lineCount = lineCount + 1
        # Here we check for "For", "Print", "Next" or "Input" statements following INT_LIT token
        # The Token and Lexemes have been stored in tokenList and wordList
        if tList[x] == "INT_LIT" and tList[x+1] != "Reserved Word":
            print("Error on line: " + str(lineCount) +  " ** Reserved Words [Print, Input, For, Next, End] Should Follow INT_LIT **")
            print("File: Parser.py, Line: 60")
            sysExitNum = True

        # <Input_statement> -> input <id>
        # Input Statements follow INT_LIT
        # Input Statements must have the Resevered Word 'input' be followed by an identifier
        if wList[x] == "input" and tList[x-1] != "INT_LIT":
            print("Error on line: " + str(lineCount) + " ** The Reserved Word 'input' can only follow INT_LIT **")
            print("File: Parser.py, Line: 68")
            sysExitNum = True
        if wList[x] == "input" and tList[x+1] != "Identifier":
            print("Error on line: " + str(lineCount) + " ** An Identifier must follow the Reserved Word'input' **")
            print("File: Parser.py, Line: 72")
            sysExitNum = True

        # <Next_Statement> -> next <id>
        # Next Statements follow INT_LIT
        # Next Statements must have the Reserved Word 'next' be followed by an identifier
        if wList[x] == "next" and tList[x-1] != "INT_LIT":
            print("Error on line: " + str(lineCount) + " ** The Reserved Word 'next' can only follow INT_LIT **")
            print("File: Parser.py, Line: 80")
            sysExitNum = True
        if wList[x] == "next" and tList[x+1] != "Identifier":
            print("Error on line: " + str(lineCount) + " ** An Identifier must follow the Reserved Word 'next' **")
            print("File: Parser.py, Line: 84")
            sysExitNum = True

        # <For_Statement> -> for <Boolean_Expression> to <id> <Code> <Next_Statement>
        # <Boolean_Expression> -> <id> Operation <Number>
        # For Statements follow INT_LIT
        # For Statements must have the Reserved Word 'for' be followed by a Boolean Expression
        # For Statements must have the Reserved Word 'to' follow the Boolean Expression
        # For Statements must have the Reserved Word 'to' be followed by an identifier
            # Check that 'for' only follows 'INT_LIT'
        if wList[x] == "for" and tList[x - 1] != "INT_LIT":
            print("Error on line: " + str(lineCount) + " ** The Reserved Word 'for' can only follow INT_LIT **")
            sysExitNum = True

            # Boolean Expressions
        if wList[x] == "for" and tList[x + 1] != "Identifier":
            print("Error on line: " + str(lineCount) + " ** An Identifier must follow the Reserved Word 'for' **")
            print("File: Parser.py, Line: 101")
            sysExitNum = True
        if wList[x] == "for" and tList[x + 2] != "Operation":
            print("Error on line: " + str(lineCount) + " ** An '=' Operation must follow the Identifier **")
            print("File: Parser.py, Line: 105")
            sysExitNum = True
        if wList[x] == "for" and tList[x + 3] != "Digit":
            print("Error on line: " + str(lineCount) + " ** A Digit must follow the '=' Operation **")
            print("File: Parser.py, Line: 109")
            sysExitNum = True

            # Check that 'to' follows the Boolean Expression
        if wList[x] == "for" and wList[x + 4] != "to":
            print("Error on line: " + str(lineCount) + " ** The Reserved Word 'to' must follow the Boolean Expression **")
            print("File: Parser.py, Line: 115")
            sysExitNum = True

            # Check that an Identifier or Digit follows the Reserved Word 'to'
        if wList[x] == "for" and tList[x + 5] != "Identifier":
            if tList[x+5] != "Digit":
                print("Error on line: " + str(lineCount) + " ** An Identifier must follow the Reserved Word 'to' **")
                print("File: Parser.py, Line: 122")
                sysExitNum = True

            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # PARSER: FOR Statements in Grammar
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            # Check that the Reserved Word 'next' exists before end of file to iterate through For Statement
            # Check for nested for loops
            # Check that the number of 'next' statements match the number of 'for' statements

        # <Print_Statement> -> print <id> | print <id> , <id>Operation<id> | print <String Literal>
        # Print Statements follow INT_LIT
        # Print Statements must be followed by an Identifier or String Literal
        if wList[x] == "print" and tList[x - 1] != "INT_LIT":
            print("Error on line: " + str(lineCount) + " ** The Reserved Word 'print' can only follow INT_LIT **")
            print("File: Parser.py, Line: 137")
            sysExitNum = True
        if wList[x] == "print" and tList[x + 1] != "String Literal":
            if tList[x + 1] != "Identifier":
                if tList[x+1] != "Digit":
                    print("Error on line: " + str(lineCount) + " ** The Reserved Word 'print' can only be followed by a String Literal, Identifier or Digit **")
                    print("File: Parser.py, Line: 143")
                    sysExitNum = True

        # <Boolean_Expression> -> <id>Operation<Number>
        # Boolean Expressions must follow the Reserved Word 'for'
        # Boolean Expressions contain and follow the flow of: Identifier -> Operation '=' -> Digit
        if wList[x] == "=":
            if tList[x-1] != "Identifier" and tList[x+1] != "Digit":
                print("Error on line: " + str(lineCount) + " ** Boolean Expressions must follow: Identifier -> Operation '=' -> Digit **")
                print("File: Parser.py, Line: 152")
                sysExitNum = True
    if sysExitNum == True or forCount != nextCount:
        sys.exit('')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # PARSER: Print Statements For Grammar
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # This portion of the PARSER is not needed with the complete interpreter. We leave this here
    # For error handling the Grammar portion of the PARSER
    '''testTokenCount = len(wList)
    testLineCount = 0
    for x in range(testTokenCount):

        print("Next Token is: " + tList[x] + "; Next Lexeme is: " + wList[x])

        # <Line> -> <INT_LIT> <Statement>
        # <Statement> -> <For_Statement> | <Print_Statement> | <Next_Statement> | <Input_Statement>
        if tList[x] == "INT_LIT":
            print("Enter Reserved Word")
        # <Print_Statement> -> print <id> | print <id> , <id>Operation<id> | print <String_Literal>
        if wList[x] == "print":
            print("Enter <id>")
            print("Enter <id>, <id>Operation<id>")
            print("Enter <String_Literal>")
        # <Input_statement> -> input <id>
        if wList[x] == "input":
            print("Enter <id>")
        # <Next_Statement> -> next <id>
        if wList[x] == "next":
            print("Enter <id>")
        # <id> -> Letter | Digit | <id><id> | <Operation>
        if tList[x] == "Identifier":
            print("Enter <id>")
            print("Enter <Operation>")
            print("Enter <INT_LIT>")
        # <String_Literal> -> " <id> "
        if tList[x] == "String Literal":
            print("Enter <INT_LIT>")
        # <For_Statement> -> for <Boolean_Expression> to <id> <Code> <Statement> <Next_Statement>
        if wList[x] == "for":
            print("Enter <Boolean_Expression>")
        if wList[x] == "to":
            print("Enter <id>")
        if tList[x] == "Operation":
            print("Enter Digit")
        if tList[x] == "Digit":
            print("Enter Reserved Word")
        if wList[x] == "end":
            print("Exit")'''

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Start Interpreter
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # We have made it passed all of the error handling so we can start the python interpretation of the file
    # Here we call on the interpreter and pass both the word and token list to start the interpretation
    Interpreter.Interpret(wList, tList)