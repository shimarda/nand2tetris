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

op_lst = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

class JackTokenizer:
    def __init__(self, file_path: str) -> None:
        self.file = file_path
        self.fp = open(file_path, "r")
        self.cur_line = ""
        self.cur_position = 0
        self.cur_token = ""
        self.token_lst = list()
        self.cur_token_type = None

    def hasMoreTokens(self) -> bool:
        length = len(self.token_lst)
        if int(length) - 1 == self.cur_position:
            return False
        else :
            return True
    
    def tokenizeLines(self):
        for line in self.fp:
            if line.startswith("//") or line.startswith('/*'):
                continue
            self.cur_line = line
            self.tokenizeLine()

    # 1行をトークンへ
    def tokenizeLine(self):
        line = self.cur_line
        token = ""
        # インデックス i を使って文字列を走査
        i = 0
        while i < len(line):
            char = line[i]

            if char == '\n':
                if token:
                    self.token_lst.append(token)
                i = len(line)

            elif char in symbol_lst:
                if token:
                    self.token_lst.append(token)
                self.token_lst.append(char)
                token = ""
                i += 1

            elif char == ' ':
                if token:
                    self.token_lst.append(token)
                    token = ""
                i += 1
                
            elif char == '"':
                if token:
                    self.token_lst.append(token)
                
                self.token_lst.append('"')
                
                try:
                    next_quote_index = line.index('"', i + 1)
                    
                    string_content = line[i + 1 : next_quote_index]
                    self.token_lst.append(string_content)
                    
                    self.token_lst.append('"')
                    
                    i = next_quote_index + 1
                    
                except ValueError:
                    string_content = line[i + 1:]
                    self.token_lst.append(string_content)
                    i = len(line) # ループを終了
                
                token = "" # トークンをリセット

            else :
                token += char
                i += 1
        
        # 行の終わりに残っているトークンを処理
        if token:
            self.token_lst.append(token)
    
    

    # 次のトークンを取得
    def advance(self):
        self.cur_position += 1
        self.cur_token = self.token_lst[self.cur_position]

    def tokenType(self):
        token = self.cur_token

        if token in keyword_lst:
            self.cur_token_type = KEYWORD
        elif token in symbol_lst:
            self.cur_token_type = SYMBOL
        elif 0 <= int(token) <= 32767:
            self.cur_token_type = INT_CONST
        elif '"' not in token and '\n' not in token:
            self.cur_token_type = STRING_CONST
        else:
            self.cur_token_type = IDENTIFIER
        
        return self.cur_token_type
    
    def KeyWord(self):
        if self.cur_token == "class":
            return CLASS
        elif self.cur_token == "method":
            return METHOD
        elif self.cur_token == "function":
            return FUNCTION
        elif self.cur_token == "constructor":
            return CONSTRUCTOR
        elif self.cur_token == "int":
            return INT
        elif self.cur_token == "boolean":
            return BOOLEAN
        elif self.cur_token == "char":
            return CHAR
        elif self.cur_token == "void":
            return VOID
        elif self.cur_token == "var":
            return VAR
        elif self.cur_token == "static":
            return STATIC
        elif self.cur_token == "field":
            return FIELD
        elif self.cur_token == "let":
            return LET
        elif self.cur_token == "do":
            return DO
        elif self.cur_token == "if":
            return IF
        elif self.cur_token == "else":
            return ELSE
        elif self.cur_token == "while":
            return WHILE
        elif self.cur_token == "return":
            return RETURN
        elif self.cur_token == "true":
            return TRUE
        elif self.cur_token == "false":
            return FALSE
        elif self.cur_token == "null":
            return NULL
        elif self.cur_token == "this":
            return THIS

    def symbol(self) -> str:
        return self.cur_token
    
    def identifier(self) -> str:
        return self.cur_token
    
    def intVal(self) -> int:
        return int(self.cur_token)
    
    def stringVal(self) -> str:
        return self.cur_token

class CompilationEngine:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = JackTokenizer(input_file)
        self.output_file = output_file
        self.fp_out = open(output_file, "w")
        
        self.input_file.tokenizeLines()

        if self.input_file.token_lst:
            self.input_file.cur_token = self.input_file.token_lst[0]

    def compileClass(self) -> None:
        classname = self.input_file.cur_token
        self.fp_out.write(f"<class>")
        self.fp_out.write(f"<keyword> class </keyword>")
        self.input_file.advance()
        self.fp_out.write(f"<identifier> {classname} </identifier>")
        self.input_file.advance()
        self.fp_out.write("<symbol> { </symbol>")
        self.input_file.advance()

        while (self.input_file.cur_token in ['static', 'field']):
            self.compileClassVarDec()
        
        while (self.input_file.cur_token in ['constructor', 'function', 'method']):
            self.compileSubroutine()

        self.fp_out.write("<symbol> } </symbol>")
        self.fp_out.write("</class>")
        self.input_file.advance()


    def compileClassVarDec(self) -> None:
        self.fp_out.write("<classVarDec>\n")
        
        self.fp_out.write(f"<keyword> {self.input_file.cur_token} </keyword>\n")
        self.input_file.advance()
        
        
        self.compileType()
        
        self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>\n")
        self.input_file.advance()
        
        while self.input_file.cur_token == ',':
            self.fp_out.write("<symbol> , </symbol>\n")
            self.input_file.advance()
            self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>\n")
            self.input_file.advance()
        
        self.fp_out.write("<symbol> ; </symbol>\n")
        self.input_file.advance()
        self.fp_out.write("</classVarDec>\n")

    def compileSubroutine(self) -> None:
        if (self.input_file.cur_token_type == METHOD):
            self.fp_out.write(f"<keyword> {self.input_file.cur_token} </keyword>")
        elif (self.input_file.cur_token_type == FUNCTION):
            self.fp_out.write(f"<function> {self.input_file.cur_token} </function>")
        elif (self.input_file.cur_token_type == CONSTRUCTOR):
            self.fp_out.write(f"<constructor> {self.input_file.cur_token} </constructor>")

        self.input_file.advance()   

        if (self.input_file.cur_token == 'void'):
            label = 'keyword'
        else:
            label = 'identifier'
        self.fp_out.write(f"<{label}> {self.input_file.cur_token} </{label}>")
        self.input_file.advance() 

        self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>")
        self.input_file.advance()

        self.fp_out.write('<symbol> ( </symbol>')
        self.input_file.advance()

        self.compileParameterList()

        self.fp_out.write("<symbol> ) </symbol>")
        self.input_file.advance()

        self.compileSubroutineBody()

    
    def compileParameterList(self) -> None:
        self.fp_out.write("<parameterList>\n")
        
        if self.input_file.cur_token != ')':

            self.compileType()
            
            self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>\n")
            self.input_file.advance()

            while self.input_file.cur_token == ',':
                self.fp_out.write("<symbol> , </symbol>\n")
                self.input_file.advance()
                self.compileType()
                self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>\n")
                self.input_file.advance()
        
        self.fp_out.write("</parameterList>\n")

    def compileSubroutineBody(self) -> None:
        self.fp_out.write("<symbol> { </symbol>")
        self.input_file.advance()

        while (self.input_file.cur_token == 'var'):
            self.compileVarDec()

        self.compileStatements()

        self.fp_out.write("<symbol> } </symbol>")
        self.input_file.advance()

    def compileVarDec(self) -> None:
        self.fp_out.write("<keyword> var </keyword>")
        self.input_file.advance()

        self.compileType()

        self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>")
        self.input_file.advance()

        while (self.input_file.cur_token == ','):
            self.fp_out.write("<symbol> , </symbol>")
            self.input_file.advance()
            self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>")
            self.input_file.advance()
        
        self.fp_out.write("<symbol> ; </symbol>")
        self.input_file.advance()

    def compileStatements(self) -> None:
        while (self.input_file.cur_token in ['let', 'if', 'while', 'do', 'return']):
            if self.input_file.cur_token == 'let':
                self.compileLet()
            elif self.input_file.cur_token == 'if':
                self.compileIf()
            elif self.input_file.cur_token == 'while':
                self.compileWhile()
            elif self.input_file.cur_token == 'do':
                self.compileDo()
            elif self.input_file.cur_token == 'return':
                self.compileReturn()

    def compileLet(self) -> None:
        self.fp_out.write("<keyword> let </keyword>")
        self.input_file.advance()

        self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>")
        self.input_file.advance()

        if self.input_file.cur_token == '[':
            self.fp_out.write("<symbol> [ </symbol>")
            self.input_file.advance()
            self.compileExpression()
            self.fp_out.write("<symbol> ] </symbol>")
            self.input_file.advance()
        
        self.fp_out.write("<symbol> = </symbol>")
        self.input_file.advance()

        self.compileExpression()

        self.fp_out.write("<symbol> ; </symbol>")
        self.input_file.advance()

    def compileIf(self) -> None:
        self.fp_out.write("<keyword> if </keyword>")
        self.input_file.advance()

        self.fp_out.write("<symbol> ( </symbol>")
        self.input_file.advance()

        self.compileExpression()

        self.fp_out.write("<symbol> ) </symbol>")
        self.input_file.advance()
        self.fp_out.write("<symbol> { </symbol>")
        self.input_file.advance()

        self.compileStatements()

        self.fp_out.write("<symbol> } </symbol>")
        self.input_file.advance()

        if self.input_file.cur_token == 'else':
            self.fp_out.write("<keyword> else </keyword>")
            self.input_file.advance()
            self.fp_out.write("<symbol> { </symbol>")
            self.input_file.advance()

            self.compileStatements()

            self.fp_out.write("<symbol> } </symbol>")
            self.input_file.advance()


    def compileWhile(self) -> None:
        self.fp_out.write("<keyword> while </keyword>")
        self.input_file.advance()

        self.fp_out.write("<symbol> ( </symbol>")
        self.input_file.advance()

        self.compileExpression()

        self.fp_out.write("<symbol> ) </symbol>")
        self.input_file.advance()

        self.fp_out.write("<symbol> { </symbol>")
        self.input_file.advance()

        self.compileStatements()

        self.fp_out.write("<symbol> } </symbol>")
        self.input_file.advance()

    def compileDo(self) -> None:
        self.fp_out.write("<keyword> do </keyword>")
        self.input_file.advance()

        self.compileSubroutineCall()

        self.fp_out.write("<symbol> ; </symbol>")
        self.input_file.advance()

    def compileReturn(self) -> None:
        self.fp_out.write("<keyword> return </keyword>")
        self.input_file.advance()

        if self.input_file.cur_token != ";":
            self.compileExpression()
        
        self.fp_out.write("<symbol> ; </symbol>")
        self.input_file.advance()


    def compileExpression(self) -> None:
        self.compileTerm()

        while self.input_file.cur_token in op_lst:
            self.fp_out.write(f"<symbol> {self.input_file.cur_token} </symbol>")
            self.input_file.advance()
            
            self.compileTerm()

    def compileTerm(self) -> None:

        if self.input_file.cur_token.isdigit():
            self.fp_out.write(f"<integerConstant> {self.input_file.cur_token} </integerConstant>\n")
            self.input_file.advance()
        
        elif self.input_file.cur_position > 0 and self.input_file.token_lst[self.input_file.cur_position - 1] == '"':
            self.fp_out.write(f"<stringConstant> {self.input_file.cur_token} </stringConstant>\n")
            self.input_file.advance()
            self.input_file.advance()
        
        elif self.input_file.cur_token in ['true', 'false', 'null', 'this']:
            self.fp_out.write(f"<keyword> {self.input_file.cur_token} </keyword>\n")
            self.input_file.advance()
        
        elif self.input_file.cur_token in ['-', '~']:
            self.fp_out.write(f"<symbol> {self.input_file.cur_token} </symbol>\n")
            self.input_file.advance()
            self.compileTerm()
        
        elif self.input_file.cur_token == '(':
            self.fp_out.write("<symbol> ( </symbol>\n")
            self.input_file.advance()
            self.compileExpression()
            self.fp_out.write("<symbol> ) </symbol>\n")
            self.input_file.advance()
        
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', self.input_file.cur_token):

            next_token = self.input_file.token_lst[self.input_file.cur_position + 1]
            
            if next_token == '[':  
                self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>\n")
                self.input_file.advance()
                self.fp_out.write("<symbol> [ </symbol>\n")
                self.input_file.advance()
                self.compileExpression()
                self.fp_out.write("<symbol> ] </symbol>\n")
                self.input_file.advance()
            
            elif next_token in ['(', '.']: 
                self.compileSubroutineCall()
            
            else:
                self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>\n")
                self.input_file.advance()

    def compileExpressionList(self) -> int:
        print("hello")

    def compileType(self) -> None:
        if self.input_file.cur_token in ['int', 'char', 'boolean']:
            self.fp_out.write(f"<keyword> {self.input_file.cur_token} </keyword>")
            self.input_file.advance()
        else:
            self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>")
            self.input_file.advance()

    def compileSubroutineCall(self) -> None:

        if self.input_file.token_lst[self.input_file.cur_position+1] != '.':
            self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>")
            self.input_file.advance()

            self.fp_out.write("<symbol> ( </symbol>")
            self.input_file.advance()

            self.compileExpressionList()

            self.fp_out.write("<symbol> ) </symbol>")
            self.input_file.advance()
        
        else:
            self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>")
            self.input_file.advance()

            self.fp_out.write("<symbol> . </symbol>")
            self.input_file.advance()

            self.fp_out.write(f"<identifier> {self.input_file.cur_token} </identifier>")
            self.input_file.advance()

            self.fp_out.write("<symbol> ( </symbol>")
            self.input_file.advance()

            self.compileExpressionList()

            self.fp_out.write("<symbol> ) </symbol>")
            self.input_file.advance()




class JackAnalyzer:
    def __init__(self):
        self.file = ""