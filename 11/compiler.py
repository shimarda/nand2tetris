import os
import sys
import re
import dataclasses

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
ARG = 26

keyword_lst = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'char', 
               'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 
               'while', 'return']

symbol_lst = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', 
              '*', '/', '&', '|', '<', '>', '=', '~']

op_lst = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

# kindの文字列表現マッピング
KIND_TO_STRING = {
    STATIC: 'static',
    FIELD: 'field',
    ARG: 'arg',
    VAR: 'var'
}

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
        elif token.isdigit() and 0 <= int(token) <= 32767:  # 先に数値チェック
            self.cur_token_type = INT_CONST
        elif (self.cur_position > 0 and 
            self.token_lst[self.cur_position - 1] == '"'):
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
        self.class_table = SymbolTable()
        self.subroutine_table = SymbolTable()
        self.current_class_name = ""
        self.input_file.tokenizeLines()

        if self.input_file.token_lst:
            self.input_file.cur_token = self.input_file.token_lst[0]
    
    def escapeXml(self, text: str) -> str:
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        return text
    
    def writeSymbol(self, symbol: str) -> None:
        escaped = self.escapeXml(symbol)
        self.fp_out.write(f"<symbol> {escaped} </symbol>\n")

    def writeIdentifier(self, name: str, usage: str) -> None:
        category = None
        index = None
        kind = None
        
        if self.subroutine_table.contains(name):
            kind = self.subroutine_table.kindOf(name)
            index = self.subroutine_table.indexOf(name)
            category = KIND_TO_STRING.get(kind, 'unknown')
        
        elif self.class_table.contains(name):
            kind = self.class_table.kindOf(name)
            index = self.class_table.indexOf(name)
            category = KIND_TO_STRING.get(kind, 'unknown')
        
        else:
            if usage == "defined":
                if name == self.current_class_name:
                    category = 'class'
                else:
                    category = 'subroutine'
            else:
                category = 'class_or_subroutine_call' 
        
        if index is not None:
            self.fp_out.write(f"<identifier> {name} (usage: {usage}, category: {category}, index: {index}) </identifier>\n")
        else:
            self.fp_out.write(f"<identifier> {name} (usage: {usage}, category: {category}) </identifier>\n")

    def compileClass(self) -> None:
        self.fp_out.write("<class>\n")
        self.fp_out.write("<keyword> class </keyword>\n")
        self.input_file.advance()
        
        self.current_class_name = self.input_file.cur_token
        self.writeIdentifier(self.current_class_name, "defined")
        
        self.input_file.advance()
        self.writeSymbol('{')
        self.input_file.advance()

        while (self.input_file.cur_token in ['static', 'field']):
            self.compileClassVarDec()
        
        while (self.input_file.cur_token in ['constructor', 'function', 'method']):
            self.compileSubroutine()

        self.writeSymbol('}')
        self.fp_out.write("</class>\n")

    def compileClassVarDec(self) -> None:
        self.fp_out.write("<classVarDec>\n")
        
        kind_str = self.input_file.cur_token
        if kind_str == 'static':
            kind = STATIC
        else:
            kind = FIELD
        
        self.fp_out.write(f"<keyword> {self.input_file.cur_token} </keyword>\n")
        self.input_file.advance()
        
        var_type = self.input_file.cur_token
        self.compileType()
        
        var_name = self.input_file.cur_token
        self.class_table.define(var_name, var_type, kind)
        self.writeIdentifier(var_name, "defined")
        self.input_file.advance()
        
        while self.input_file.cur_token == ',':
            self.writeSymbol(',')
            self.input_file.advance()
            
            var_name = self.input_file.cur_token
            self.class_table.define(var_name, var_type, kind)
            self.writeIdentifier(var_name, "defined")
            self.input_file.advance()
        
        self.writeSymbol(';')
        self.input_file.advance()
        self.fp_out.write("</classVarDec>\n")

    def compileSubroutine(self) -> None:
        self.subroutine_table.reset()
        
        self.fp_out.write("<subroutineDec>\n")
        
        subroutine_type = self.input_file.cur_token
        if subroutine_type == 'method':
            self.subroutine_table.define("this", self.current_class_name, ARG)

        self.fp_out.write(f"<keyword> {self.input_file.cur_token} </keyword>\n")
        self.input_file.advance()
    
        if self.input_file.cur_token == 'void':
            self.fp_out.write(f"<keyword> void </keyword>\n")
            self.input_file.advance()
        else:
            self.compileType()
        
        subroutine_name = self.input_file.cur_token
        self.writeIdentifier(subroutine_name, "defined")
        self.input_file.advance()
        
        self.writeSymbol('(')
        self.input_file.advance()
        
        self.compileParameterList()
        
        self.writeSymbol(')')
        self.input_file.advance()
        
        self.fp_out.write("<subroutineBody>\n")
        self.writeSymbol('{')
        self.input_file.advance()
        
        while self.input_file.cur_token == 'var':
            self.compileVarDec()
        
        self.compileStatements()
        
        self.writeSymbol('}')
        self.input_file.advance()
        self.fp_out.write("</subroutineBody>\n")
        
        self.fp_out.write("</subroutineDec>\n")

    def compileParameterList(self) -> None:
        self.fp_out.write("<parameterList>\n")
        
        if self.input_file.cur_token != ')':
            param_type = self.input_file.cur_token
            self.compileType()
            
            param_name = self.input_file.cur_token
            self.subroutine_table.define(param_name, param_type, ARG)
            self.writeIdentifier(param_name, "defined")
            self.input_file.advance()
            
            while self.input_file.cur_token == ',':
                self.writeSymbol(',')
                self.input_file.advance()
                
                param_type = self.input_file.cur_token
                self.compileType()
                
                param_name = self.input_file.cur_token
                self.subroutine_table.define(param_name, param_type, ARG)
                self.writeIdentifier(param_name, "defined")
                self.input_file.advance()
        
        self.fp_out.write("</parameterList>\n")

    def compileVarDec(self) -> None:
        self.fp_out.write("<varDec>\n")
        
        self.fp_out.write(f"<keyword> var </keyword>\n")
        self.input_file.advance()
        
        var_type = self.input_file.cur_token
        self.compileType()
        
        var_name = self.input_file.cur_token
        self.subroutine_table.define(var_name, var_type, VAR)
        self.writeIdentifier(var_name, "defined")
        self.input_file.advance()
        
        while self.input_file.cur_token == ',':
            self.writeSymbol(',')
            self.input_file.advance()
            
            var_name = self.input_file.cur_token
            self.subroutine_table.define(var_name, var_type, VAR)
            self.writeIdentifier(var_name, "defined")
            self.input_file.advance()
        
        self.writeSymbol(';')
        self.input_file.advance()
        self.fp_out.write("</varDec>\n")

    def compileStatements(self) -> None:
        self.fp_out.write("<statements>\n")
        
        while self.input_file.cur_token in ['let', 'if', 'while', 'do', 'return']:
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
        
        self.fp_out.write("</statements>\n")

    def compileLet(self) -> None:
        self.fp_out.write("<letStatement>\n")
        self.fp_out.write("<keyword> let </keyword>\n")
        self.input_file.advance()
        
        var_name = self.input_file.cur_token
        self.writeIdentifier(var_name, "used")
        self.input_file.advance()
        
        if self.input_file.cur_token == '[':
            self.writeSymbol('[')
            self.input_file.advance()
            self.compileExpression()
            self.writeSymbol(']')
            self.input_file.advance()
        
        self.writeSymbol('=')
        self.input_file.advance()
        
        self.compileExpression()
        
        self.writeSymbol(';')
        self.input_file.advance()
        self.fp_out.write("</letStatement>\n")

    def compileIf(self) -> None:
        self.fp_out.write("<ifStatement>\n")
        self.fp_out.write("<keyword> if </keyword>\n")
        self.input_file.advance()
        
        self.writeSymbol('(')
        self.input_file.advance()
        
        self.compileExpression()
        
        self.writeSymbol(')')
        self.input_file.advance()
        
        self.writeSymbol('{')
        self.input_file.advance()
        
        self.compileStatements()
        
        self.writeSymbol('}')
        self.input_file.advance()
        
        if self.input_file.cur_token == 'else':
            self.fp_out.write("<keyword> else </keyword>\n")
            self.input_file.advance()
            
            self.writeSymbol('{')
            self.input_file.advance()
            
            self.compileStatements()
            
            self.writeSymbol('}')
            self.input_file.advance()
        
        self.fp_out.write("</ifStatement>\n")

    def compileWhile(self) -> None:
        self.fp_out.write("<whileStatement>\n")
        self.fp_out.write("<keyword> while </keyword>\n")
        self.input_file.advance()
        
        self.writeSymbol('(')
        self.input_file.advance()
        
        self.compileExpression()
        
        self.writeSymbol(')')
        self.input_file.advance()
        
        self.writeSymbol('{')
        self.input_file.advance()
        
        self.compileStatements()
        
        self.writeSymbol('}')
        self.input_file.advance()
        self.fp_out.write("</whileStatement>\n")

    def compileDo(self) -> None:
        self.fp_out.write("<doStatement>\n")
        self.fp_out.write("<keyword> do </keyword>\n")
        self.input_file.advance()
        
        self.compileSubroutineCall()
        
        self.writeSymbol(';')
        self.input_file.advance()
        self.fp_out.write("</doStatement>\n")

    def compileSubroutineCall(self) -> None:

        first_name = self.input_file.cur_token
        self.writeIdentifier(first_name, "used")
        self.input_file.advance()
        
        if self.input_file.cur_token == '.':
            self.writeSymbol('.')
            self.input_file.advance()
            
            subroutine_name = self.input_file.cur_token
            self.writeIdentifier(subroutine_name, "used")
            self.input_file.advance()
        
        self.writeSymbol('(')
        self.input_file.advance()
        
        self.compileExpressionList()
        
        self.writeSymbol(')')
        self.input_file.advance()

    def compileReturn(self) -> None:
        self.fp_out.write("<returnStatement>\n")
        self.fp_out.write("<keyword> return </keyword>\n")
        self.input_file.advance()
        
        if self.input_file.cur_token != ';':
            self.compileExpression()
        
        self.writeSymbol(';')
        self.input_file.advance()
        self.fp_out.write("</returnStatement>\n")

    def compileExpression(self) -> None:
        self.fp_out.write("<expression>\n")
        self.compileTerm()
        
        while self.input_file.cur_token in op_lst:
            self.writeSymbol(self.input_file.cur_token)
            self.input_file.advance()
            
            self.compileTerm()
        self.fp_out.write("</expression>\n")

    def compileTerm(self) -> None:
        self.fp_out.write("<term>\n")
        
        if self.input_file.cur_token.isdigit():
            self.fp_out.write(f"<integerConstant> {self.input_file.cur_token} </integerConstant>\n")
            self.input_file.advance()
        
        elif self.input_file.cur_position > 0 and self.input_file.token_lst[self.input_file.cur_position - 1] == '"':
            escaped_str = self.escapeXml(self.input_file.cur_token)
            self.fp_out.write(f"<stringConstant> {escaped_str} </stringConstant>\n")
            self.input_file.advance()
            self.input_file.advance()
        
        elif self.input_file.cur_token in ['true', 'false', 'null', 'this']:
            self.fp_out.write(f"<keyword> {self.input_file.cur_token} </keyword>\n")
            self.input_file.advance()
        
        elif self.input_file.cur_token in ['-', '~']:
            self.writeSymbol(self.input_file.cur_token)
            self.input_file.advance()
            self.compileTerm()
        
        elif self.input_file.cur_token == '(':
            self.writeSymbol('(')
            self.input_file.advance()
            self.compileExpression()
            self.writeSymbol(')')
            self.input_file.advance()
        
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', self.input_file.cur_token):
            next_token = self.input_file.token_lst[self.input_file.cur_position + 1]
            
            if next_token == '[':  
                var_name = self.input_file.cur_token
                self.writeIdentifier(var_name, "used")
                self.input_file.advance()
                self.writeSymbol('[')
                self.input_file.advance()
                self.compileExpression()
                self.writeSymbol(']')
                self.input_file.advance()
            
            elif next_token in ['(', '.']: 
                self.compileSubroutineCall()
            
            else:
                var_name = self.input_file.cur_token
                self.writeIdentifier(var_name, "used")
                self.input_file.advance()
                
        self.fp_out.write("</term>\n")

    def compileExpressionList(self) -> int:
        self.fp_out.write("<expressionList>\n")
        count = 0
        
        if self.input_file.cur_token != ')':
            self.compileExpression()
            count += 1
            
            while self.input_file.cur_token == ',':
                self.writeSymbol(',')
                self.input_file.advance()
                self.compileExpression()
                count += 1
        
        self.fp_out.write("</expressionList>\n")
        return count

    def compileType(self) -> None:
        if self.input_file.cur_token in ['int', 'char', 'boolean']:
            self.fp_out.write(f"<keyword> {self.input_file.cur_token} </keyword>\n")
            self.input_file.advance()
        else:
            self.writeIdentifier(self.input_file.cur_token, "used")
            self.input_file.advance()

class JackAnalyzer:
    def __init__(self):
        self.input_path = ""
        self.jack_files = []
    
    def analyze(self, path: str) -> None:
        self.input_path = path
        
        if os.path.isdir(path):
            self._getJackFiles(path)
        elif os.path.isfile(path) and path.endswith('.jack'):
            self.jack_files.append(path)
        else:
            print(f"エラー: {path} は有効な.jackファイルまたはディレクトリではありません")
            return
        
        for jack_file in self.jack_files:
            self._compileFile(jack_file)
    
    def _getJackFiles(self, directory: str) -> None:
        for filename in os.listdir(directory):
            if filename.endswith('.jack'):
                file_path = os.path.join(directory, filename)
                self.jack_files.append(file_path)
        
        if not self.jack_files:
            print(f"警告: {directory} に.jackファイルが見つかりません")
    
    def _compileFile(self, jack_file: str) -> None:
        output_file = jack_file.replace('.jack', '.xml')
        
        print(f"コンパイル中: {jack_file} → {output_file}")
        
        try:
            engine = CompilationEngine(jack_file, output_file)
            
            engine.compileClass()
            
            engine.fp_out.close()
            
            print(f"完了: {output_file}")
            
        except Exception as e:
            print(f"エラー: {jack_file} のコンパイル中にエラーが発生しました")
            print(f"詳細: {e}")

@dataclasses.dataclass
class SymbolElement:
    name: str
    type: str
    kind: int
    index: int


class SymbolTable:
    def __init__(self):
        # 空のシンボルテーブル作成
        self.table = {}
        self.counters = {}
    # シンボルテーブルを空にする
    def reset(self) -> None:
        self.table.clear()
        self.counters.clear()

    # 新しい変数を定義する
    def define(self, name: str, type: str, kind) -> None:
        if kind not in self.counters:
            self.counters[kind] = 0

        index = self.counters[kind]
        self.counters[kind] += 1

        self.table[name] = SymbolElement(name, type, kind, index)
        
    def varCount(self, kind) -> int:
        return self.counters.get(kind, 0)

    def kindOf(self, name) -> int:
        if name in self.table:
            return self.table[name].kind
        else:
            return None
        
    def typeOf(self, name) -> str:
        if name in self.table:
            return self.table[name].type
        else:
            return None
        
    def indexOf(self, name) -> int:
        if name in self.table:
            return self.table[name].index
        else:
            return None

class VMWriter:
    def __init__(self, output_path):
        self.fp = open(output_path, "w")

    def writePush(self, segment, index):
        vm_code = f"""push {segment} {index}\n"""
        self.fp.write(vm_code)

    def writePop(self, segment, index):
        vm_code = f"""pop {segment} {index}\n"""
        self.fp.write(vm_code)

    def writeArithmetic(self, command):
        vm_code = f"""{command}\n"""
        self.fp.write(vm_code)

    def writeLabel(self, label):
        vm_code = f"""label {label}\n"""
        self.fp.write(vm_code)
    
    def writeGoto(self, label):
        vm_code = f"""goto {label}\n"""
        self.fp.write(vm_code)

    def writeIf(self, label):
        vm_code = f"""if-goto {label}\n"""
        self.fp.write(vm_code)

    def writeCall(self, name, nArgs):
        vm_code = f"""call {name} {nArgs}\n"""
        self.fp.write(vm_code)

    def writeFunction(self, name, nVars):
        vm_code = f"""function {name} {nVars}\n"""
        self.fp.write(vm_code)
    
    def writeReturn(self):
        vm_code = """return\n"""
        self.fp.write(vm_code)

    def close(self):
        self.fp.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python compiler.py <input.jack または ディレクトリ>")
        print("例:")
        print("  python compiler.py Square.jack")
        print("  python compiler.py SquareGame/")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    analyzer = JackAnalyzer()
    analyzer.analyze(input_path)