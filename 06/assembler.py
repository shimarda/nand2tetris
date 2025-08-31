import re

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
        
        return None

    # 命令のタイプを示す
    def instructionType(self):
        return None

    # 命令が(〇〇)の場合シンボル〇〇を返す
    def symbol(self):
        return None

    # 現在のC命令のdest部分を返す
    def dest(self):
        return None

    # 現在のC命令のcomp部分を返す
    def comp(self):
        return None

    # 現在のC命令のjump部分を返す
    def jump(self):
        return None

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











