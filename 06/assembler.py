import re

class Parser():
    def init():
        return None

    # 入力にまだ行があるのか
    def hasMoreLines():
        return None

    # 空白、コメントをスキップ
    def advance():
        return None

    # 命令のタイプを示す
    def instructionType():
        return None

    # 命令が(〇〇)の場合シンボル〇〇を返す
    def symbol():
        return None

    # 現在のC命令のdest部分を返す
    def dest():
        return None

    # 現在のC命令のcomp部分を返す
    def comp():
        return None

    # 現在のC命令のjump部分を返す
    def jump():
        return None

class Code():
    # destニーモニックのバイナリコード
    def dest():
        return None
    
    # compニーモニックのバイナリコード
    def comp():
        return None

    # jumpニーモニックのバイナリコード
    def jump():
        return None


class SymbolTable():
    # 新しい空のシンボルテーブルを作成
    def init():
        return None

    # <symbot, address>をテーブルに追加
    def addEntry():
        return None

    # 指定されたsymbolがテーブルに含まれているのか
    def contains():
        return None

    # symbolに関連付けられたアドレスを返す
    def getAddress():
        return None











