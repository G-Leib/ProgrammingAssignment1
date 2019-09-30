#===========================================================
# Authors:
# Robert Kupfner
# Gil Leibovich
#===========================================================

import sys
from enum import Enum

class CharClass(Enum):
    EOF        = 1
    LETTER     = 2
    DIGIT      = 3
    OPERATOR   = 4
    PUNCTUATOR = 5
    BLANK      = 6
    OTHER      = 7

def getChar(input):
    if len(input) == 0:
        return (None, CharClass.EOF)
    c = input[0].lower()
    if c.isalpha():
        return (c, CharClass.LETTER)
    if c.isdigit():
        return (c, CharClass.DIGIT)
    if c in ['+', '-', '*', '/', '>', '=', '<', '<=', '>=', ':=']:
        return (c, CharClass.OPERATOR)
    if c in ['.', ':', ';']:
        return (c, CharClass.PUNCTUATOR)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    return (c, CharClass.OTHER)

def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

class Token(Enum):
    ADDITION = 1
    ASSIGNMENT = 2
    BEGIN = 3
    BOOLEAN_TYPE = 4
    COLON = 5
    DO = 6
    ELSE = 7
    END = 8
    EQUAL = 9
    FALSE = 10
    GREATER = 11
    GREATER_EQUAL = 12
    IDENTIFIER = 13
    IF = 14
    INTEGER_LITERAL = 15
    INTEGER_TYPE = 16
    LESS = 17
    LESS_EQUAL = 18
    MULTIPLICATION = 19
    PERIOD = 20
    PROGRAM = 21
    READ = 22
    SEMICOLON = 23
    SUBTRACTION = 24
    THEN = 25
    TRUE = 26
    VAR = 27
    WHILE = 28
    WRITE = 29
    DIVISION = 30
    EOF = 31

lookupToken = {
    "$"         : Token.EOF,
    "+"         : Token.ADDITION,
    "-"         : Token.SUBTRACTION,
    "*"         : Token.MULTIPLICATION,
    "/"         : Token.DIVISION,
    ">"         : Token.GREATER,
    ">="        : Token.GREATER_EQUAL,
    "<"         : Token.LESS,
    "<="        : Token.LESS_EQUAL,
    "begin"     : Token.BEGIN,
    "do"        : Token.DO,
    "else"      : Token.ELSE,
    "end"       : Token.END,
    "false"     : Token.FALSE,
    "if"        : Token.IF,
    "."         : Token.PERIOD,
    ":="        : Token.ASSIGNMENT,
    "="         : Token.EQUAL,
    "boolean"   : Token.BOOLEAN_TYPE,
    "integer"   : Token.INTEGER_TYPE,
    "program"   : Token.PROGRAM,
    "read"      : Token.READ,
    ";"         : Token.SEMICOLON,
    ":"         : Token.COLON,
    "then"      : Token.THEN,
    "true"      : Token.TRUE,
    "var"       : Token.VAR,
    "while"     : Token.WHILE,
    "write"     : Token.WRITE
}

class Tree:

    TAB = "   "

    def __init__(self):
        self.data     = None
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab = ""):
        if self.data != None:
            print(tab + self.data)
            tab += self.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)

def errorMessage(code):
    msg = "Error " + str(code).zfill(2) + ": "
    if code == 1:
        return msg + "source file missing"
    if code == 2:
        return msg + "couldn't open source file"
    if code == 3:
        return msg + "lexical error"
    if code == 4:
        return msg + "couldn't open grammar file"
    if code == 5:
        return msg + "couldn't open SLR table file"
    if code == 6:
        return msg + "EOF expected"
    if code == 7:
        return msg + "identifier expected"
    if code == 8:
        return msg + "special word missing"
    if code == 9:
        return msg + "symbol missing"
    if code == 10:
        return msg + "data type expected"
    if code == 11:
        return msg + "identifier or literal value expected"
    return msg + "syntax error"

def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    if charClass == CharClass.EOF:

        return (input, None, None)

    if charClass == CharClass.LETTER:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass != CharClass.DIGIT and charClass != CharClass.LETTER:
                break
        if lexeme.lower() in lookupToken.keys():
            return (input, lexeme, lookupToken[lexeme.lower()])
        else:
            return (input, lexeme, Token.IDENTIFIER)

    if charClass == CharClass.DIGIT:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass != CharClass.DIGIT:
                break
        return (input, lexeme, Token.INTEGER_LITERAL)

    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        c, charClass = getChar(input)
        if c == '=':
            input, lexeme = addChar(input, lexeme)
        if lexeme in lookupToken.keys():
            return (input, lexeme, lookupToken[lexeme])

    if charClass == CharClass.PUNCTUATOR:
        input, lexeme = addChar(input, lexeme)
        c, charClass = getChar(input)
        if lexeme == ':' and c == '=':
            input, lexeme = addChar(input, lexeme)
            return (input, lexeme, lookupToken[lexeme])
        return (input, lexeme, lookupToken[lexeme])

    raise Exception("{} on symbol {}".format(errorMessage(3), lexeme))

def loadGrammar(input):
    grammar = []
    for line in input:
        grammar.append(line.strip())
    return grammar

def getLHS(production):
    return production.split("->")[0].strip()

def getRHS(production):
    return production.split("->")[1].strip().split(" ")

def printGrammar(grammar):
    i = 0
    for production in grammar:
        print(str(i) + ". " + getLHS(production), end = " -> ")
        print(getRHS(production))
        i += 1

def loadTable(input):
    actions = {}
    gotos = {}
    header = [h.lower() for h in input.readline().strip().split(",")]
    end = header.index("$")
    tokens = []
    for field in header[1:end + 1]:
        tokens.append(field)
    variables = header[end + 1:]
    for line in input:
        row = line.strip().split(",")
        state = int(row[0])
        # print("state: " + str(state))
        for i in range(len(tokens)):
            token = tokens[i]
            key = (state, token)
            value = row[i + 1]
            if len(value) == 0:
                value = None
            actions[key] = value
        for i in range(len(variables)):
            variable = variables[i]
            #print("variable: " + variable)
            key = (state, variable)
            value = row[i + len(tokens) + 1]
            if len(value) == 0:
                value = None
            gotos[key] = value

    return (actions, gotos)

def printActions(actions):
    for key in actions:
        print(key, end = " -> ")
        print(actions[key])

def printGotos(gotos):
    for key in gotos:
        print(key, end = " -> ")
        print(gotos[key])


# TODO: fill complete conditions for remaining syntax errors: 8, 9,
def handle_syntax_error(stack, state, input):
    if stack[-2] == '.' and input[0] != '$':
        raise Exception(errorMessage(6))
    elif stack[-2] == 'program' and input[0] != 'i':
        raise Exception(errorMessage(7))
    elif stack[-2] == ';' and input[0] != "read":
        raise Exception(errorMessage(8))
    elif state == 25 and input[0] not in lookupToken.keys():
        raise Exception(errorMessage(9))
    elif state == 46 and input[0] != CharClass.OPERATOR:
        raise Exception(errorMessage(9))
    elif 'var' in stack and input[0] not in {'integer', 'boolean'}:
        raise Exception(errorMessage(10))
    elif stack[-2] == ':=' and input[0] not in {'i', 'int_l', 'true', 'false'}:
        raise Exception(errorMessage(11))
    else:
        raise Exception(errorMessage(99))

def parse(input, grammar, actions, gotos):

    trees = []

    stack = []
    stack.append(0)
    while True:
        print("stack: ", end = "")
        print(stack, end = " ")
        print("input: ", end = "")
        print(input, end = " ")
        state = stack[-1]
        # print("state: " + str(state))
        token = input[0]
        # print("token: " + token)
        action = actions[(state, token)]
        print("action: ", end = "")
        print(action)

        if action is None:
            handle_syntax_error(stack, state, input)


        if action[0] == 's':
            input.pop(0)
            stack.append(token)
            state = int(action[1:])
            stack.append(state)

            tree = Tree()
            tree.data = token
            trees.append(tree)

        elif action[0] == 'r':
            production = grammar[int(action[1:])]
            lhs = getLHS(production)
            rhs = getRHS(production)
            for i in range(len(rhs) * 2):
                stack.pop()
            state = stack[-1]
            stack.append(lhs)
            stack.append(int(gotos[(state, lhs)]))

            newTree = Tree()
            newTree.data = lhs

            for tree in trees[-len(rhs):]:
                newTree.add(tree)

            trees = trees[:-len(rhs)]

            trees.append(newTree)

        else:
            production = grammar[0]
            lhs = getLHS(production)
            rhs = getRHS(production)

            root = Tree()
            root.data = lhs
            for tree in trees:
                print(tree.data)
                root.add(tree)

            return root


if __name__ == "__main__":

    
    if len(sys.argv) != 2:
        raise Exception(errorMessage(1))
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError(errorMessage(2))
    
    input = source.read()
    source.close()
    tokens = []
    tape = []
    output = []
    inputToken = []

    while True:
        input, lexeme, token = lex(input)
        if lexeme == None:
            tape.append("$")
            break

        
        if token == Token.IDENTIFIER:
            tape.append('i')
        elif token == Token.INTEGER_LITERAL:
            tape.append('int_l')
        else:
            tape.append(lexeme)
        
        tokens.append(token)
        output.append([lexeme, token, tape[-1]])

    for (lexeme, token, t)in output:
        print(lexeme, '\t', t, '\t', token)

    try:
        input = open("grammar.txt", "rt")
    except Exception:
        raise IOError(errorMessage(4))
    grammar = loadGrammar(input)
    # printGrammar(grammar)
    input.close()

    try:
        input = open("slr_table.txt", "rt")
    except Exception:
        raise IOError(errorMessage(5))
    actions, gotos = loadTable(input)
    # printActions(actions)
    # printGotos(gotos)
    input.close()

    print(tape)

    parse_tree = parse(tape, grammar, actions, gotos)

    if parse_tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        parse_tree.print()
    else:
        print("Code has syntax errors!")

    print([(getLHS(g), getRHS(g)) for g in grammar])