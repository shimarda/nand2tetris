import re
import sys


A_INSTRUCTION: str = "A_INSTRUCTION"
C_INSTRUCTION: str = "C_INSTRUCTION"
L_INSTRUCTION: str = "L_INSTRUCTION"

class Parser:

    # 入力ファイル/データストリームを開き解析の準備をする
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.fp = open(file_path, "r")
        

    # 入力にまだ行があるのか
    def hasMoreLines(self) -> bool:
        cur_line = self.fp.tell()
        line = self.fp.readline()
        self.fp.seek(cur_line)
        return line != ''

    # 空白、コメントをスキップ
    def advance(self):
        while True:
            line = self.fp.readline()
            stripped = line.strip()
            if stripped == '' or stripped.startswith('//'):
                continue
            return line

    # 命令のタイプを示す
    def instructionType(self):
        line = self.fp.readline()
        if line.startswith('@'):
            self.instructionType = A_INSTRUCTION
            return A_INSTRUCTION
        elif re.fullmatch(r'\(*\)', line):
            self.instructionType = L_INSTRUCTION
            return L_INSTRUCTION
        else:
            self.instructionType = C_INSTRUCTION
            return C_INSTRUCTION

    # 命令が(〇〇)の場合シンボル〇〇を返す
    def symbol(self):
        line = self.fp.readline()
        if self.instructionType == L_INSTRUCTION:
            m = re.search(r'\((*)\)', line)
            return m.group(1)
        elif self.instructionType == A_INSTRUCTION:
            m = re.search(r'@(*)', line)
            return m.group(1)
    # 現在のC命令のdest部分を返す
    def dest(self):
        line = self.fp.readline()
        return re.search(r'(*)=*', line).group(1)

    # 現在のC命令のcomp部分を返す
    def comp(self):
        line = self.fp.readline()
        return re.search(r'*=();*', line).group(1)

    # 現在のC命令のjump部分を返す
    def jump(self):
        line = self.fp.readline()
        return re.search(r'*=*;(*)', line).group(1)

class Code:
    # destニーモニックのバイナリコード
    def dest(self):
        
        return None
    
    # compニーモニックのバイナリコード
    def comp(self):
        return None

    # jumpニーモニックのバイナリコード
    def jump(selg):
        return None


class SymbolTable:
    # 新しい空のシンボルテーブルを作成
    def init(self):
        return None

    # <symbot, address>をテーブルに追加
    def addEntry(self):
        return None

    # 指定されたsymbolがテーブルに含まれているのか
    def contains(self):
        return None

    # symbolに関連付けられたアドレスを返す
    def getAddress(self):
        return None





if __name__ == "__main__":
    
    args = sys.argv
    if 1 != len(args):
        print("Argument is invalid")
    else:
        parser = Parser(args[0])

        if parser.hasMoreLines():
            # 次に行あり
            parser.advance()
            
            instr_type = parser.instructionType()
            if instr_type == A_INSTRUCTION or instr_type == L_INSTRUCTION:
                symbol = parser.symbol()
            else:
                dest = parser.dest()
                comp = parser.comp()
                jump = parser.jump()
        else:
            parser.fp.close()

    




