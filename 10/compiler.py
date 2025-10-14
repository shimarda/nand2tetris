import os
import sys
import re

KEYWORD = 0
SYMBOL = 1
IDENTIFIER = 2
INT_CONST = 3
STRING_CONST = 4
CLASS = 5
METHOD = 6
FUNCTION = 7
CONSTRUCTOR = 8
INT = 9
BOOLEAN = 10
CHAR = 11
VOID = 12
VAR = 13
STATIC = 14
FIELD = 15
LET = 16
DO = 17
IF = 18
ELSE = 19
WHILE = 20
RETURN = 21
TRUE = 22
FALSE = 23
NULL = 24
THIS = 25

keyword_lst = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'char', 
               'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 
               'while', 'return']

symbol_lst = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', 
              '*', '/', '&', '|', '<', '>', '=', '~']

class JackTokenizer:
    def __init__(self, file_path: str) -> None:
        self.file = file_path
        self.fp = open(file_path, "r")
        self.cur_token = ""
        self.cur_line = ""
        self.token_type = None

    def hasMoreTokens(self) -> bool:
        before, separator, after = self.cur_line.partition(self.cur_token)
        if after is "":
            return False
        else:
            return True
            
    def advance(self):
        self.cur_line = self.fp.readline()
        line_lst = self.cur_line.strip()
        try:
            cur_num = line_lst.index(self.cur_token)
            self.cur_token = line_lst[cur_num+1]
        except ValueError:
            self.cur_token = line_lst[0]

    def tokenType(self):
        token = self.cur_token

        if token in keyword_lst:
            self.token_type = KEYWORD
        elif token in symbol_lst:
            self.token_type = SYMBOL
        elif 0 <= int(token) <= 32767:
            self.token_type = INT_CONST
        elif '"' not in token and '\n' not in token:
            self.token_type = STRING_CONST
        else:
            self.token_type = IDENTIFIER
        
        return self.token_type
    
    def KeyWord(self):
        if self.cur_token is "class":
            return CLASS
        elif self.cur_token is "method":
            return METHOD
        elif self.cur_token is "function":
            return FUNCTION
        elif self.cur_token is "constructor":
            return CONSTRUCTOR
        elif self.cur_token is "int":
            return INT
        elif self.cur_token is "boolean":
            return BOOLEAN
        elif self.cur_token is "char":
            return CHAR
        elif self.cur_token is "void":
            return VOID
        elif self.cur_token is "var":
            return VAR
        elif self.cur_token is "static":
            return STATIC
        elif self.cur_token is "field":
            return FIELD
        elif self.cur_token is "let":
            return LET
        elif self.cur_token is "do":
            return DO
        elif self.cur_token is "if":
            return IF
        elif self.cur_token is "else":
            return ELSE
        elif self.cur_token is "while":
            return WHILE
        elif self.cur_token is "return":
            return RETURN
        elif self.cur_token is "true":
            return TRUE
        elif self.cur_token is "false":
            return FALSE
        elif self.cur_token is "null":
            return NULL
        elif self.cur_token is "this":
            return THIS

    def symbol(self):
        return self.cur_token


class CompilationEngine:
    def __init__(self):
        self.file = ""

class JackAnalyzer:
    def __init__(self):
        self.file = ""