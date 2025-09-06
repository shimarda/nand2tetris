import os

C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GOTO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8


class Parser:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.fp = open(file_path, "r")
        self.cur_line = ""
        self.cmd_type = None
        
    def close(self):
        self.fp.close()

    # 入力にさらに行があるか
    def hasMoreLines(self) -> bool:
        cur_line = self.fp.tell()
        line = self.fp.readline()
        self.fp.seek(cur_line)
        return line != ''
    
    # 次の入力をよみ現在のコマンドにする
    def advance(self):
        self.cur_line = self.fp.readline()

    # 現在のコマンドの種類の定数を返す
    def commandType(self):
        cmd = self.cur_line.strip().split()[0]

        if cmd in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            self.cmd_type = C_ARITHMETIC
        elif cmd == "push":
            self.cmd_type = C_PUSH
        elif cmd == "pop":
            self.cmd_type = C_POP
        elif cmd == "if-goto":
            self.cmd_type = C_IF
        elif cmd == "goto":
            self.cmd_type = C_GOTO
        elif cmd == "function":
            self.cmd_type = C_FUNCTION
        elif cmd == "return":
            self.cmd_type = C_RETURN
        elif cmd == "call":
            self.cmd_type = C_CALL
        
        return self.cmd_type
    
    # 現在のコマンドの第一引数を返す
    def arg1(self) -> str:
        if self.cmd_type != C_ARITHMETIC:
            line = self.cur_line
            return str(line.strip().split()[1])
        else:
            return self.cur_line.strip().split()[0]
    
    # 現在のコマンドの第二引数を返す
    def arg2(self) -> str:
        if self.cmd_type in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            line = self.cur_line
            return str(line.strip().split()[2])

class CodeWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.fp = open(file_path, "w")
        self.cur_line = ""
        self.label_counter = 0

    def close(self):
        self.fp.close()

    # 算術論理コマンドのcmdに対応するアセンブリコードを出力ファイルに書き込む
    def WriteArithmetic(self, cmd: str):

        if cmd == "add":
            asm_code = """
                @SP
                M=M-1
                A=M
                D=M
                @SP
                M=M-1
                A=M
                M=D+M
                @SP
                M=M+1
                """
        elif cmd == "sub":
            asm_code = """
                @SP
                M=M-1
                A=M
                D=M
                @SP
                M=M-1
                A=M
                M=M-D
                @SP
                M=M+1"""
        elif cmd == "neg":
            asm_code = """
                @SP
                M=M-1
                D=M
                M=-D
                @SP
                M=M+1
                """
        elif cmd == "eq":
            jump_label = f"Jmp_{self.label_counter}"
            end_label = f"end_{self.label_counter}"
            self.label_counter += 1
            asm_code = f"""
                @SP
                M=M-1
                D=M
                A=M
                @SP
                M=M-1
                A=M
                D=M-D
                @{jump_label}
                D;JEQ
                @SP
                A=M
                M=0
                @{end_label}
                0;JMP
                ({jump_label})
                @SP
                A=M
                M=-1
                ({end_label})
                @SP
                M=M+1
                """
        elif cmd == "gt":
            jump_label = f"Jmp_{self.label_counter}"
            end_label = f"end_{self.label_counter}"
            self.label_counter += 1
            asm_code = f"""
                @SP
                M=M-1
                D=M
                A=M
                @SP
                M=M-1
                A=M
                D=M-D
                @{jump_label}
                D;JGT
                @SP
                A=M
                M=0
                @{end_label}
                0;JMP
                ({jump_label})
                @SP
                A=M
                M=-1
                ({end_label})
                @SP
                M=M+1
                """
        elif cmd == "lt":
            jump_label = f"Jmp_{self.label_counter}"
            end_label = f"end_{self.label_counter}"
            self.label_counter += 1
            asm_code = f"""
                @SP
                M=M-1
                D=M
                A=M
                @SP
                M=M-1
                A=M
                D=M-D
                @{jump_label}
                D;JLT
                @SP
                A=M
                M=0
                @{end_label}
                0;JMP
                ({jump_label})
                @SP
                A=M
                M=-1
                ({end_label})
                @SP
                M=M+1
                """
        elif cmd == "and":
            asm_code = """
                @SP
                M=M-1
                D=M
                A=M
                @SP
                M=M-1
                A=M
                M=M&D
                @SP
                M=M+1
                """   
        elif cmd == "or":
            asm_code = """
                @SP
                M=M-1
                D=M
                A=M
                @SP
                M=M-1
                A=M
                M=M|D
                @SP
                M=M+1
                """   
        elif cmd == "not":
            asm_code = """
                @SP
                M=M-1
                D=M
                M=!D
                @SP
                M=M+1
                """   
        self.fp.write(asm_code)

    # push, popのcommandに対応するアセンブリコードを出力ファイルに書き込む
    def WritePushPop(self, cmd: int, segment, index):
        if cmd == C_PUSH:

            if segment == "constant":
                asm_code = f"""
                    @{index}
                    D=A
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """
                
            elif segment in ["local", "argument", "this", "that"]:
                seg_map = {
                    "local": "LCL",
                    "argument": "ARG",
                    "this": "THIS",
                    "that": "THAT"
                }
                seg = seg_map[segment]
                asm_code = f"""
                    @{seg}
                    D=M
                    @{index}
                    A=D+A
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """ 
            elif segment == "temp":
                addr = index + 5
                asm_code = f"""
                    @{addr}
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """
            elif segment == "static":
                asm_code = f"""
                    @{self.file_name}.{index}
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """
            elif segment == "pointer":
                addr = "THIS" if index == 0 else "THAT"
                asm_code = f"""
                    @{addr}
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """
        elif cmd == C_POP:
            if segment in ["local", "argument", "this", "that"]:
                seg_map = {
                    "local": "LCL",
                    "argument": "ARG",
                    "this": "THIS",
                    "that": "THAT"
                }
                seg = seg_map[segment]
                asm_code = f"""
                    @{seg}
                    D=M
                    @{index}
                    D=D+A
                    @R13
                    M=D
                    @SP
                    M=M-1
                    A=M
                    D=M
                    @R13
                    A=M
                    M=D
                    """
            elif segment == "temp":
                addr = index + 5
                asm_code = f"""
                    @SP
                    M=M-1
                    A=M
                    D=M
                    @{addr}
                    M=D
                    """
            elif segment == "static":
                asm_code = f"""
                    @SP
                    M=M-1
                    A=M
                    D=M
                    @{self.file_name}.{index}
                    M=D
                    """
            elif segment == "pointer":
                addr = "THIS" if index == 0 else "THAT"
                asm_code = f"""
                    @SP
                    M=M-1
                    A=M
                    D=M
                    @{addr}
                    M=D
                    """
        self.fp.write(asm_code)    

