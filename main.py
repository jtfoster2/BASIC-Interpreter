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

# The interpreter uses grammar from a subset of BASIC which is defined as:

'''
<Program> -> <Code> end
<Code> -> <Line><Code> | <Line>
<Line> -> <INT_LIT> <Statement>
<Statement> -> <For_Statement> | <Print_Statement> | <Next_Statement> | <Input_Statement>

<For_Statement> -> for <Boolean_Expression> to <id> <Print_Statements> <Next_Statement>
<Print_Statements> -> <Print_Statement> | <Print_Statement> <Print_Statements>
<Print_Statement> -> print <id> | print <id>, <id> * <id> | print <String_Literal>
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

import Scanner
import Parser
import Interpreter

def main():  # The main program definition where we create the Scanner object and use Scanner.scan() method to parse the file 'table-of-squares.bas'

    my_scanner = Scanner.Scanner()
    #my_scanner.scan('table-of-squares.bas')  # Run the test file 'table-of-squares.bas' in the Scanner object.
    my_scanner.scan('test.bas')  # Run the test file 'table-of-squares.bas' in the Scanner object.

main()  # Here we start the main function running the program