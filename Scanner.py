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
# Assignment: Module 5 - 2nd Project Deliverable
# Date: 03/16/2020

# The Scanner takes in a file argument from the Main.py file and creates a Lexeme and Token list for later use.
# Once the file has been scanned, we pass these lists into the Parser

import sys
import Parser
import Interpreter

class Word:
    # This is the implementation of the Word class. This class holds each lexeme and it's token group and the
    # 'row' and 'col' indexes. The Word class turns the character stream taken in by the Scanner function into
    # lexemes or special characters then displays its relevant information.

    token = ''  # Store the token as a string
    isStringLiteral = False  # bool that determines a string literal
    isComment = False  # bool that determines a comment
    isComma = False  # A flag for commas
    isComplete = False  # A flag for completed words

    # 'reservedWords' - A string array containing all possible lexemes that can fall under the token category: Reserved Word
    # 'operations' - A string array containing legal operative characters/lexemes that fall under the token category: Operation

    reservedWords = ['print', 'input', 'for', 'to', 'next', 'end']
    operations = ['*', '=']

    def __init__(self, word, rownum, colnum):

        # No default constructor
        # A Word can only be initialized if it is passed as:  word(string), rownum(int), and colnum(int)

        self.word = word  # Word defined as a string
        self.rownum = rownum  # Stores row number for error messages
        self.colnum = colnum  # Stores col number for error messages

    def set_token(self):

        # Assigns a token group to the lexemes that are passed
        # Once the lexemes are assigned to a token group they are 'complete'

        if self.word:  # Check for empty list
            if self.word[-1] == ("\"") == self.word[0]:  # String literal when contained by quotes
                self.token = 'String Literal'
            elif self.word in self.reservedWords:  # Reserved word if contained in reservedWords array
                self.token = 'Reserved Word'
            elif self.word in self.operations:  # Operation if contained in operations array
                self.token = 'Operation'
            elif self.word[0] == ("/") == self.word[1]:  # Comment if starting with '//'
                self.token = 'Comment'
            elif self.word[0].isdigit():  # INT_LIT if default isdigit works
                # Check if INT_LIT flag has been initialised so digits can be used outside of INT_LIT
                if Scanner.isINTLIT == False:
                    self.token = 'INT_LIT'
                else:
                    self.token = 'Digit'
            elif self.word != ',':  # Lastly, if the word isn't a comma it must be an identifier
                self.token = 'Identifier'
            else:
                self.isComma = True
            self.isComplete = True  # Completed when assigned token
            #self.print_word()  # Print every completed Word

    # These methods are not needed but left for error handling the Scanner functionality
    def print_word(self):  # The print_word method prints the relevant contents of the word to the user. Ignore Commas

        if not self.isComma:
            print(self.token + ", symbol: " + self.word)
            print("line: " + str(self.rownum) + " column: " + str(self.colnum))
            print("")

    def handle_string_literal(self, character_in_string_literal):
        # String Literals are considered one lexeme; alternate logic needed to handle the spaces in between the words

        if character_in_string_literal == "\"":  # Check for closing quotes for a String Literal
            self.word += character_in_string_literal  # Add the closing quotes to the string
            self.set_token()
            self.isStringLiteral = False  # Stop adding to the String Literal
        else:
            self.word += character_in_string_literal  # Appened character to String Literal

    def handle_comment(self,
                       characterInComment):  # Comments, similar to String Literals, are treated as one large lexeme
        if characterInComment == "\n":
            self.word += characterInComment
            self.set_token()
            self.isComment = False
        else:
            self.word += characterInComment

    def handle_character(self, character_being_read):
        if character_being_read == "/":  # Identify the Comment Blocks
            self.word += character_being_read
            self.isComment = True
        elif character_being_read == "\"":  # Identify String Literals
            self.isStringLiteral = True
            self.word += character_being_read
        elif character_being_read.isspace():  # Identify Spaces
            if self.word != ' ':
                self.set_token()
        elif character_being_read == ",":
            self.set_token()
        else:
            self.word += character_being_read  # Appended to the term list

        if self.word == "end": # Checks for the end of file
            self.set_token()
            Scanner.isEOF = True
        if self.word in self.reservedWords:
            self.set_token()
        if self.word in self.operations:
            self.set_token()

class Scanner:
    # This is the implementation of the Scanner class. This Scanner class will open a file specified in its argument, split the file up line by line
    # indexing each character of every line one by one and utilize these to build lexemes

    row = 0  # 'row' is an integer that holds the index of the current row
    col = 0  # 'col' is an integer that holds the index of the current character
    # We want to maintain the row and column numbers of each word as they are scanned for the output of the
    # Scanner and error handling in the Parser

    isScanning = False
    newLine = False     # Flag for INT_LIT statements in the PARSER Portion
    isEOF = False       # Flag for End of file keyword in the PARSER Portion
    isINTLIT = False    # Flag for INT_LIT statements in the PARSER Portion
    intLitCheck = 0     # Flag for INT_LIT statements in the PARSER Portion
    currWord = Word('', row, col)

    wordList = []       # Stores the file words
    tokenList = []      # Stores the corresponding tokens

    def scan(self, filename):

        # Scanner.scan($$$.scl): This method takes in a filename as its argument - For testing we use 'table-of-squares.bas'
        # 'self' allows an object to refer to itself, like "this." in other languages. In Python, methods belonging to an object
        # takes the object itself in as its first parameter. For this reason, we can ignore 'self'.

        self.row = 1  # Start at the first line of file

        with open(filename,
                  "r") as fileData:  # This line opens the file passed through the scan parameter in "read" mode
            # and uses the file input as a file object called "fileData".

            for line in fileData.readlines():  # This line reads each line in 'fileData' and each line is passed as an argument
                # into the Scanner.read_line() method where each character will be checked

                self.newLine = True
                self.read_line(line)  # Each new line is passed into the below defined Scanner.read_line() method
                self.col = 0  # Start each new line at index 0
                self.row += 1  # The 'row' is incremented so the next line can be read

        Parser.parser(Scanner.wordList, Scanner.tokenList)

    def read_line(self, scannedLine):

        # This method constructs terminal symbols for each character given in the line passed
        # Words are defined as:  (String literals, Comments, Reserved words, Identifiers, Operations, Spaces, Commas)
        # Words are identified by a single space seperating two characters
        # Spaces and Commas are ignored thus not printed

        lineLength = len(scannedLine)
        Scanner.isINTLIT = False # Flag for New Line to create INT_LIT token when necessary

        for currChar in scannedLine:

            # Check to see if the Reserved Word 'end' has been found
            # If found, there should not be anything so throw and error and exit program
            if Scanner.isEOF == True:
                print("Error: File must end with the BASIC Reserved Word 'end'")
                sys.exit('')

            self.col += 1  # For each new character checked we increment the col count by 1
            if self.isScanning:  # Check if the program is already building a word
                if self.currWord.isStringLiteral:  # Check if the word is a string literal. Defined above
                    self.currWord.handle_string_literal(currChar)
                elif self.currWord.isComment:  # Check if the word is a comment. Define above
                    self.currWord.handle_comment(currChar)
                elif self.currWord.word.isspace():  # Check if the current word is a space. Defined above
                    if currChar.isspace():  # If two spaces, program is not building a word
                        self.isScanning = False
                    else:
                        self.currWord.handle_character(currChar)  # Check if space-character, start new word
                else:
                    self.currWord.handle_character(currChar)  # Add character to end of current word
            else:
                self.currWord = Word('', self.row, self.col)  # Creates a new word
                self.isScanning = True
                self.currWord.handle_character(currChar)

            if self.currWord.isComplete:  # Check if word is completed
                self.isScanning = False  # Set scan to false

                # <Line> -> <INT_LIT> <Statement>
                # We check that each line start with an <INT_LIT> token and that the <INT_LIT> tokens are sequential
                if self.currWord.token != "INT_LIT" and self.newLine == True: # PARSER: Check to make sure new line starts with <INT_LIT>
                    print("Error on Line: " + str(self.row) + " ** Lines Need To Start WITH <INT_LIT> **") # Print Line and Error
                    sys.exit('') # Exit Code

                if self.currWord.token == "INT_LIT": # PARSER: Check to see if INT_LIT are incremental
                    Scanner.intLitCheck = Scanner.intLitCheck + 10 # PARSER: Increment INT_LIT on everyline for continuity
                    if str(self.currWord.word) != str(Scanner.intLitCheck): # PARSER: If INT_LIT is not correct value Error out of code
                        print("Error on Line: " + str(self.row) + " ** INT_LIT should be increments of 10 **") # Print Line and Error
                        sys.exit('') # Exit Code

                self.newLine = False # PARSER: Flag for <INT_LIT>
                Scanner.wordList.append(self.currWord.word) # PARSER: Create a Table/List of Words
                Scanner.tokenList.append(self.currWord.token) # PARSER: Create a Table/List of Tokens
                Scanner.isINTLIT = True # Flag for identifier to not be considerd INT_LIT