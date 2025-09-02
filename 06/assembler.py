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
        self.binary = ['0'] * 16
        self.current_line = ""
        self.instruction_type = None        

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
            self.current_line = stripped
            self.instruction_type = None
            return stripped

    # 命令のタイプを示す
    def instructionType(self):
        if self.instruction_type:
            return self.instruction_type
        
        line = self.current_line
        if line.startswith('@'):
            self.instruction_type = A_INSTRUCTION
            return A_INSTRUCTION
        elif re.fullmatch(r'\(.+\)', line):
            self.instruction_type = L_INSTRUCTION
            return L_INSTRUCTION
        else:
            self.instruction_type = C_INSTRUCTION
            return C_INSTRUCTION

    # 命令が(〇〇)の場合シンボル〇〇を返す
    def symbol(self):
        line = self.current_line
        instr_type = self.instructionType()
        if instr_type == L_INSTRUCTION:
            m = re.search(r'\((.+)\)', line)
            return m.group(1)
        elif instr_type == A_INSTRUCTION:
            m = re.search(r'@(.+)', line)
            return m.group(1)
        return None

    # 現在のC命令のdest部分を返す
    def dest(self):
        line = self.current_line
        if '=' in line:
            return line.split('=')[0].strip()
        return None

    # 現在のC命令のcomp部分を返す
    def comp(self):
        line = self.current_line
        if '=' in line:
            line = line.split('=')[1]
        if ';' in line:
            line = line.split(';')[0]
        return line.strip()
    
    # 現在のC命令のjump部分を返す
    def jump(self):
        line = self.current_line
        if ';' in line:
            return line.split(';')[1].strip()
        return None
    def close(self):
        self.fp.close()

class Code:
    def __init__(self):
        pass

    # destニーモニックのバイナリコード
    def dest(self, dest):
        res = ['0', '0', '0']
        if dest:
            if "M" in dest:
                res[2] = '1'
            if "D" in dest:
                res[1] = '1'
            if "A" in dest:
                res[0] = '1'
        return ''.join(res)
    
    # compニーモニックのバイナリコード
    def comp(self, comp: str):
        comp_table = {
            # a=0 の場合
            "0":   "0101010",
            "1":   "0111111", 
            "-1":  "0111010",
            "D":   "0001100",
            "A":   "0110000",
            "!D":  "0001101",
            "!A":  "0110001", 
            "-D":  "0001111",
            "-A":  "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010", 
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            # a=1 の場合 (AをMに置換)
            "M":   "1110000",
            "!M":  "1110001",
            "-M":  "1110011", 
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111", 
            "D&M": "1000000",
            "D|M": "1010101"
        }
        return comp_table.get(comp, "0000000")

    # jumpニーモニックのバイナリコード
    def jump(self, jump: str):
        jump_table = {
            None:  "000",
            "JGT": "001",
            "JEQ": "010", 
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }
        return jump_table.get(jump, "000")
    
class SymbolTable:
    # 新しい空のシンボルテーブルを作成
    def __init__(self):
        self.table = {
            "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "SCREEN": 16384, "KBD": 24576
        }        

    # <symbot, address>をテーブルに追加
    def addEntry(self, symbol, address):
        self.table[symbol] = address

    # 指定されたsymbolがテーブルに含まれているのか
    def contains(self, symbol):
        return symbol in self.table

    # symbolに関連付けられたアドレスを返す
    def getAddress(self, symbol):
        return self.table.get(symbol)

def assemble_file(input_file, output_file):
    parser = Parser(input_file)
    code = Code()
    symbol_table = SymbolTable()

    # 第一パス
    rom_addr = 0
    while parser.hasMoreLines():
        line = parser.advance()
        if line is None:
            break

        instr_type = parser.instructionType()
        if instr_type == L_INSTRUCTION:
            symbol = parser.symbol()
            symbol_table.addEntry(symbol, rom_addr)
        else:
            rom_addr += 1

    parser.close()

    # 第二パス
    parser = Parser(input_file)
    ram_addr = 16
    machine_code = []
    
    while parser.hasMoreLines():
        line = parser.advance()
        if line is None:
            break

        instr_type = parser.instructionType()

        if instr_type == A_INSTRUCTION:
            symbol = parser.symbol()

            if symbol.isdigit():
                addr = int(symbol)
            else:
                if symbol_table.contains(symbol):
                    addr = symbol_table.getAddress(symbol)
                else:
                    symbol_table.addEntry(symbol, ram_addr)
                    addr = ram_addr
                    ram_addr += 1

            binary = format(addr, '016b')
            machine_code.append(binary)
        
        elif instr_type == C_INSTRUCTION:
            dest_str = parser.dest()
            comp_str = parser.comp()
            jump_str = parser.jump()

            dest_bits = code.dest(dest_str)
            comp_bits = code.comp(comp_str)
            jump_bits = code.jump(jump_str)

            binary = "111" + comp_bits + dest_bits + jump_bits
            machine_code.append(binary)

    parser.close()

    with open(output_file, 'w') as f:
        for code_line in machine_code:
            f.write(code_line + '\n')

if __name__ == "__main__":
    
    args = sys.argv
    if len(args) != 2:
        print("Argument is invalid")
    
    input_file = args[1]
    output_file = input_file.replace('.asm', '.hack')
    
    try:
        assemble_file(input_file, output_file)
        print("アセンブル終了")
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)




