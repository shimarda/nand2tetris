import os
import sys

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
        line = self.cur_line.strip()
        if not line or line.startswith('//'):
            return None
        
        if '//' in line:
            line = line[:line.index('//')]
        
        line = line.strip()
        if not line:
            return None
        
        parts = line.split()
        if not parts:
            return None

        cmd = parts[0]

        if cmd in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            self.cmd_type = C_ARITHMETIC
        elif cmd == "push":
            self.cmd_type = C_PUSH
        elif cmd == "pop":
            self.cmd_type = C_POP
        elif cmd == "label":
            self.cmd_type = C_LABEL
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
        line = self.cur_line.strip()
        if '//' in line:
            line = line[:line.index('//')]
        
        line = line.strip()
        parts = line.split()

        if self.cmd_type != C_ARITHMETIC:
            return parts[1]
        else:
            return parts[0]
    
    # 現在のコマンドの第二引数を返す
    def arg2(self) -> str:
        line = self.cur_line.strip()

        if '//' in line:
            line = line[:line.index('//')]

        line = line.strip()
        parts = line.split()

        if self.cmd_type in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            return parts[2]
        else:
            return None

class CodeWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = ""
        self.fp = open(file_path, "w")
        self.cur_line = ""
        self.label_counter = 0
        asm_code = """
            @256
            D=A
            @SP
            M=D
            """
        self.fp.write(asm_code)
        self.writeCall("Sys.init", 0)

    def close(self):
        self.fp.close()

    # 新しいvmファイルの変換が開始されたことを知らせる
    def setFileName(self, file_path):
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]
        print(f"{self.file_name}の変換開始")

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
                A=M
                M=-M
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
                A=M
                D=M
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
                A=M
                D=M
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
                A=M
                D=M
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
                A=M
                D=M
                @SP
                M=M-1
                A=M
                M=D&M
                @SP
                M=M+1
                """   
        elif cmd == "or":
            asm_code = """
                @SP
                M=M-1
                A=M
                D=M
                @SP
                M=M-1
                A=M
                M=D|M
                @SP
                M=M+1
                """   
        elif cmd == "not":
            asm_code = """
                @SP
                M=M-1
                A=M
                M=!M
                @SP
                M=M+1
                """   
        self.fp.write(asm_code)

    # push, popのcommandに対応するアセンブリコードを出力ファイルに書き込む
    def WritePushPop(self, cmd: int, segment, index):
        index = int(index)

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

    # ラベルコマンドの実装
    def writeLabel(self, label: str):
        asm_code = f"""
            ({label})
            """
        self.fp.write(asm_code)

    # gotoコマンドの実装
    def writeGoto(self, label: str):
        asm_code = f"""
            @{label}
            0;JMP
            """
        self.fp.write(asm_code)

    # if-gotoの実装
    def writeIf(self, label: str):
        asm_code = f"""
            @SP
            M=M-1
            A=M
            D=M
            @{label}
            D;JNE
            """
        self.fp.write(asm_code)

    # functionコマンドの実装
    def writeFunction(self, functionName: str, nVars: int):
        asm_code = f"""
            ({functionName})
            """
        for i in range(nVars):
            asm_code +=  """
                @SP
                A=M
                M=0
                @SP
                M=M+1
                """
        self.fp.write(asm_code)

    # callコマンドの実装
    def writeCall(self, functionName: str, nArgs: int):
        asm_code = f"""
            @{functionName}$ret.{self.label_counter}
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            @LCL
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            @ARG
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            @THIS
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            @THAT
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            @SP
            D=M
            @5
            D=D-A
            @{nArgs}
            D=D-A
            @ARG
            M=D
            @SP
            D=M
            @LCL
            M=D
            @{functionName}
            0;JMP
            ({functionName}$ret.{self.label_counter})
            """
        self.label_counter += 1
        self.fp.write(asm_code)

    # return コマンドの実装
    def writeReturn(self):
        asm_code = f"""
            @LCL
            D=M
            @13
            M=D
            @5
            A=D-A
            D=M
            @14
            M=D
            @SP
            M=M-1
            A=M
            D=M
            @ARG
            A=M
            M=D
            D=A
            @SP
            M=D+1
            @13
            D=M
            @1
            A=D-A
            D=M
            @THAT
            M=D
            @13
            D=M
            @2
            A=D-A
            D=M
            @THIS
            M=D
            @13
            D=M
            @3
            A=D-A
            D=M
            @ARG
            M=D 
            @13
            D=M
            @4
            A=D-A
            D=M
            @LCL
            M=D
            @14
            A=M
            0;JMP
            """
        self.fp.write(asm_code)

class VMTranslator:
    def __init__(self, input_path):
        self.input_path = input_path
        
        # 出力ファイル名を決定
        dir_name = os.path.basename(os.path.normpath(input_path))
        self.output_file = os.path.join(input_path, f"{dir_name}.asm")
        
        # .vmファイルのリストを取得
        self.vm_files = [f for f in os.listdir(input_path) if f.endswith('.vm')]
        print(f"見つかったファイル: {self.vm_files}")

    def translate(self):
        # 1つのCodeWriterインスタンスを作成(ブートストラップコード込み)
        code_writer = CodeWriter(self.output_file)
        
        try:
            # 各.vmファイルを順番に処理
            for vm_file in self.vm_files:
                full_input_path = os.path.join(self.input_path, vm_file)
                parser = Parser(full_input_path)
                code_writer.setFileName(full_input_path)
                
                try:
                    while parser.hasMoreLines():
                        parser.advance()
                        cmd_type = parser.commandType()

                        if cmd_type is None:
                            continue

                        if cmd_type == C_ARITHMETIC:
                            cmd = parser.arg1()
                            code_writer.WriteArithmetic(cmd)
                        elif cmd_type in [C_POP, C_PUSH]:
                            seg = parser.arg1()
                            index = parser.arg2()
                            code_writer.WritePushPop(cmd_type, seg, index)
                        elif cmd_type == C_LABEL:
                            label = parser.arg1()
                            code_writer.writeLabel(label)
                        elif cmd_type == C_GOTO:
                            label = parser.arg1()
                            code_writer.writeGoto(label)
                        elif cmd_type == C_IF:
                            label = parser.arg1()
                            code_writer.writeIf(label)
                        elif cmd_type == C_CALL:
                            function_name = parser.arg1()
                            args_num = parser.arg2()
                            code_writer.writeCall(function_name, int(args_num))
                        elif cmd_type == C_FUNCTION:
                            function_name = parser.arg1()
                            args_num = parser.arg2()
                            code_writer.writeFunction(function_name, int(args_num))
                        elif cmd_type == C_RETURN:
                            code_writer.writeReturn()
                finally:
                    parser.close()
        finally:
            code_writer.close()

    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    input_path = sys.argv[1]
    
    translator = VMTranslator(input_path)
    translator.translate()

    print("変換終了")