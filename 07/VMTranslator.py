    

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
        self.fp = open(file_path, "rw")
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

    # 現在のコマンドの朱里の定数を返す
    def commandType(self):
        cmd = self.cur_line.strip().split()[0]

        if cmd in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            self.cmd_type = C_ARITHMETIC
        elif cmd == "push":
            self.cmd_type = C_PUSH
        elif cmd == "pop":
            self.cmd_type = C_POP
        elif cmd == "if":
            self.cmd_type = C_IF
        elif cmd == "goto":
            self.cmd_type = C_GOTO
        elif cmd == "fuction":
            self.cmd_type = C_FUNCTION
        elif cmd == "return":
            self.cmd_type = C_RETURN
        elif cmd == "call":
            self.cmd_type = C_CALL
        
        return self.cmd_type
    
    # 現在のコマンドの第一引数を返す
    def arg1(self) -> str:
        line = self.cur_line
        return str(line.strip().split()[1])
    
    # 現在のコマンドの第二引数を返す
    def arg2(self) -> str:
        if self.cmd_type in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            line = self.cur_line
            return str(line.strip().split()[2])

class CodeWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.fp = open(file_path, "r")
        self.cur_line = ""

    def close(self):
        self.fp.close()

    # 算術論理コマンドのcmdに対応するアセンブリコードを出力ファイルに書き込む
    def WriteArithmetic(self, cmd: str):
        cmd_lis = cmd.strip().split()
        if cmd_lis[0] == "add":
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
        elif cmd_lis[0] == "sub":
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
        elif cmd_lis[0] == "neg":
            asm_code = """
                @SP
                M=M-1
                D=M
                M=-D
                @SP
                M=M+1
                """
        elif cmd_lis[0] == "eq":
            jump_label = cmd_lis[1]
            asm_code = f"""
                @SP
                M=M-1
                D=M
                A=M
                @SP
                M=M-1
                A=M
                D=D-A
                @{jump_label}
                D;JEQ
                @SP
                A=M
                M=0
                @END
                0;JMP
                ({jump_label})
                @SP
                A=M
                M=-1
                (END)
                @SP
                M=M+1
                """
        elif cmd_lis[0] == "gt":
            jump_label = cmd_lis[1]
            asm_code = f"""
                @SP
                M=M-1
                D=M
                A=M
                @SP
                M=M-1
                A=M
                D=D-A
                @{jump_label}
                D;JGT
                @SP
                A=M
                M=0
                @END
                0;JMP
                ({jump_label})
                @SP
                A=M
                M=-1
                (END)
                @SP
                M=M+1
                """
        elif cmd_lis[0] == "lt":
            jump_label = cmd_lis[1]
            asm_code = f"""
                @SP
                M=M-1
                D=M
                A=M
                @SP
                M=M-1
                A=M
                D=D-A
                @{jump_label}
                D;JLT
                @SP
                A=M
                M=0
                @END
                0;JMP
                ({jump_label})
                @SP
                A=M
                M=-1
                (END)
                @SP
                M=M+1
                """
        elif cmd_lis[0] == "and":
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
        elif cmd_lis[0] == "or":
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
        elif cmd_lis[0] == "not":
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
    def WritePushPop(self, cmd, segment, index):
        return 0
    

