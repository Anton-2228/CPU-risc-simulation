import sys

from reverse_polish_notation import reverse_polish_notation
from parser import parser
from CPU.isa import Opcodes, write_codes_mnem, write_codes
from ast_check import AST_syntax_check


class Translator:
    def __init__(self):
        self.regs = [0 for _ in range(8)]
        self.vars = {}
        self.instructions = []
        self.tokens = None
        self.tmp_var_counter = 0
        self.tmp_vars = {}
        self.strings = {}
        self.string_count = 0

    def trans_expr(self, expr):
        polish = reverse_polish_notation(expr)
        deep = 0
        for i in polish:
            match i[0]:
                case "PLUS":
                    if deep < 7:
                        self.instructions.append([Opcodes.ADD, 0, deep-1, deep])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.ADD, 0, 6, 7])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.ADD, 0, 7, 8])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "MINUS":
                    if deep < 7:
                        self.instructions.append([Opcodes.SUB, 0, deep - 1, deep])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.SUB, 0, 6, 7])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.SUB, 0, 7, 8])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "MUL":
                    if deep < 7:
                        self.instructions.append([Opcodes.MUL, 0, deep - 1, deep])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.MUL, 0, 6, 7])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.MUL, 0, 7, 8])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "DIV":
                    if deep < 7:
                        self.instructions.append([Opcodes.DIV, 0, deep - 1, deep])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.DIV, 0, 6, 7])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.DIV, 0, 7, 8])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "MOD":
                    if deep < 7:
                        self.instructions.append([Opcodes.MOD, 0, deep - 1, deep])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.MOD, 0, 6, 7])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.MOD, 0, 7, 8])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "OR":
                    if deep < 7:
                        self.instructions.append([Opcodes.OR, 0, deep - 1, deep])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.OR, 0, 6, 7])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.OR, 0, 7, 8])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "AND":
                    if deep < 7:
                        self.instructions.append([Opcodes.AND, 0, deep - 1, deep])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.AND, 0, 6, 7])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.AND, 0, 7, 8])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "NEQ":
                    if deep < 7:
                        self.instructions.append([Opcodes.CMP, 0, deep - 1, deep])
                        self.instructions.append([Opcodes.JUMPZ, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, deep - 1, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, deep - 1, 0])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.CMP, 0, 6, 7])
                        self.instructions.append([Opcodes.JUMPZ, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, 6, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, 6, 0])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.CMP, 0, 7, 8])
                        self.instructions.append([Opcodes.JUMPZ, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, 7, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, 7, 0])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "EQ":
                    if deep < 7:
                        self.instructions.append([Opcodes.CMP, 0, deep - 1, deep])
                        self.instructions.append([Opcodes.JUMPNZ, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, deep - 1, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, deep - 1, 0])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.CMP, 0, 6, 7])
                        self.instructions.append([Opcodes.JUMPNZ, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, 6, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, 6, 0])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.CMP, 0, 7, 8])
                        self.instructions.append([Opcodes.JUMPNZ, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, 7, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, 7, 0])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "GT":
                    if deep < 7:
                        self.instructions.append([Opcodes.CMP, 0, deep - 1, deep])
                        self.instructions.append([Opcodes.JUMPNNEG, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, deep - 1, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, deep - 1, 0])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.CMP, 0, 6, 7])
                        self.instructions.append([Opcodes.JUMPNNEG, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, 6, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, 6, 0])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.CMP, 0, 7, 8])
                        self.instructions.append([Opcodes.JUMPNNEG, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, 7, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, 7, 0])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "LT":
                    if deep < 7:
                        self.instructions.append([Opcodes.CMP, 0, deep - 1, deep])
                        self.instructions.append([Opcodes.JUMPNEG, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, deep - 1, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, deep - 1, 0])
                    elif deep == 7:
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.CMP, 0, 6, 7])
                        self.instructions.append([Opcodes.JUMPNEG, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, 6, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, 6, 0])
                    else:
                        self.instructions.append([Opcodes.POP, 0, 0, 8])
                        self.instructions.append([Opcodes.POP, 0, 0, 7])
                        self.instructions.append([Opcodes.CMP, 0, 7, 8])
                        self.instructions.append([Opcodes.JUMPNEG, 1, 0, len(self.instructions) + 3])
                        self.instructions.append([Opcodes.MOV, 1, 7, 1])
                        self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
                        self.instructions.append([Opcodes.MOV, 1, 7, 0])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                    deep -= 1
                case "NAME":
                    deep += 1
                    if deep < 7:
                        self.instructions.append([Opcodes.LOAD, 1, deep, (i[1], 0)])
                    else:
                        self.instructions.append([Opcodes.LOAD, 1, 7, (i[1], 0)])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                case "NUMBER":
                    deep += 1
                    if deep < 7:
                        self.instructions.append([Opcodes.MOV, 1, deep, int(i[1])])
                    else:
                        self.instructions.append([Opcodes.MOV, 1, 7, int(i[1])])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])
                case "INPUT_INT":
                    deep += 1
                    if deep < 7:
                        self.instructions.append([Opcodes.IN, 0, deep, 2])
                    else:
                        self.instructions.append([Opcodes.IN, 0, 7, 2])
                        self.instructions.append([Opcodes.PUSH, 0, 0, 7])

    def trans_let(self, index):
        index_end = index
        while tokens[index_end][0] != "SEMICOLON":
            index_end += 1
        var = tokens[index+1][1]
        self.vars[var] = None
        match self.tokens[index+3][0]:
            case "STRING":
                self.trans_str(tokens[index+3][1])
            case "INPUT_STR":
                self.input_str()
            case _:
                expr = tokens[index+3:index_end]
                self.trans_expr(expr)
        self.instructions.append([Opcodes.STORE, 1, 1, (var, 0)])
        return index_end

    def trans_var(self, index):
        index_end = index
        while tokens[index_end][0] != "SEMICOLON":
            index_end += 1
        var = tokens[index][1]
        match self.tokens[index + 2][0]:
            case "STRING":
                self.trans_str(tokens[index + 2][1])
            case "INPUT_STR":
                self.input_str()
            case _:
                expr = tokens[index + 2:index_end]
                self.trans_expr(expr)
        self.instructions.append([Opcodes.STORE, 1, 1, (var, 0)])
        return index_end

    def trans_while(self, index):
        st_expr = index + 2
        end_expr = st_expr
        count_bracket = 0
        while True:
            if tokens[end_expr][0] == "RPAREN" and count_bracket == 0:
                break
            if tokens[end_expr][0] == "LPAREN":
                count_bracket += 1
            elif tokens[end_expr][0] == "RPAREN":
                count_bracket -= 1
            end_expr += 1
        expr = tokens[st_expr:end_expr]
        start_while = len(self.instructions)
        self.trans_expr(expr)
        self.instructions.append([Opcodes.CMP, 1, 1, 0])
        tmp_var = str(self.tmp_var_counter)
        self.tmp_var_counter += 1
        self.tmp_vars[tmp_var] = None
        self.instructions.append([Opcodes.JUMPNZ, 1, 0, (tmp_var, 1)])
        end_while = self.translate(end_expr+2)
        self.instructions.append([Opcodes.JUMP, 1, 0, start_while])
        self.tmp_vars[tmp_var] = len(self.instructions)
        return end_while

    def trans_if(self, index):
        st_expr = index + 2
        end_expr = st_expr
        count_bracket = 0
        while True:
            if tokens[end_expr][0] == "RPAREN" and count_bracket == 0:
                break
            if tokens[end_expr][0] == "LPAREN":
                count_bracket += 1
            elif tokens[end_expr][0] == "RPAREN":
                count_bracket -= 1
            end_expr += 1
        expr = tokens[st_expr:end_expr]
        self.trans_expr(expr)
        self.instructions.append([Opcodes.CMP, 1, 1, 0])
        tmp_var = str(self.tmp_var_counter)
        self.tmp_var_counter += 1
        self.tmp_vars[tmp_var] = None
        self.instructions.append([Opcodes.JUMPZ, 1, 0, (tmp_var, 1)])
        end_if = self.translate(end_expr + 2)
        self.tmp_vars[tmp_var] = len(self.instructions)
        return end_if

    def trans_print_int(self, index):
        st_expr = index + 2
        end_expr = st_expr
        count_bracket = 0
        while True:
            if tokens[end_expr][0] == "RPAREN" and count_bracket == 0:
                break
            if tokens[end_expr][0] == "LPAREN":
                count_bracket += 1
            elif tokens[end_expr][0] == "RPAREN":
                count_bracket -= 1
            end_expr += 1
        expr = tokens[st_expr:end_expr]
        self.trans_expr(expr)
        self.instructions.append([Opcodes.OUT, 0, 1, 2])
        return end_expr

    def trans_print_str(self, index):
        self.instructions.append([Opcodes.LOAD, 1, 1, (self.tokens[index+2][1], 0)])
        self.instructions.append([Opcodes.LOAD, 0, 2, 1])
        # self.instructions.append([Opcodes.OUT, 0, 2, 1])
        start_print = len(self.instructions)
        self.instructions.append([Opcodes.CMP, 1, 2, 0])
        self.instructions.append([Opcodes.JUMPZ, 1, 0, start_print+7])
        self.instructions.append([Opcodes.SUB, 1, 2, 1])
        self.instructions.append([Opcodes.ADD, 1, 1, 1])
        self.instructions.append([Opcodes.LOAD, 0, 3, 1])
        self.instructions.append([Opcodes.OUT, 0, 3, 1])
        self.instructions.append([Opcodes.JUMP, 1,0, start_print])
        return index+4

    def trans_str(self, line):
        line = line[1:-1]
        num_line = str(self.string_count)
        self.strings[str(self.string_count)] = None
        self.instructions.append([Opcodes.MOV, 1, 1, len(line)])
        self.instructions.append([Opcodes.STORE, 1, 1, (num_line, 3, 1)])
        for i in line:
            self.instructions.append([Opcodes.MOV, 1, 1, ord(i)])
            self.instructions.append([Opcodes.STORE, 1, 1, (num_line, 3, 1)])
        self.instructions.append([Opcodes.MOV, 1, 1, (num_line, 3, 0)])


    def input_str(self):
        line = str(self.string_count)
        self.strings[line] = None
        self.instructions.append([Opcodes.IN, 0, 1, 1])

        self.instructions.append([Opcodes.CMP, 1, 1, 20])
        self.instructions.append([Opcodes.JUMPNEG, 1, 0, len(self.instructions) + 2])
        self.instructions.append([Opcodes.MOV, 1, 1, 20])

        self.instructions.append([Opcodes.STORE, 1, 1, (line, 2)])
        self.instructions.append([Opcodes.MOV, 1, 3, (line, 2)])
        index_start = len(self.instructions)
        self.instructions.append([Opcodes.SUB, 1, 1, 1])
        self.instructions.append([Opcodes.ADD, 1, 3, 1])
        self.instructions.append([Opcodes.IN, 0, 2, 1])
        self.instructions.append([Opcodes.STORE, 0, 2, 3])
        self.instructions.append([Opcodes.CMP, 1, 1, 0])
        self.instructions.append([Opcodes.JUMPNZ, 1, 0, index_start])
        self.instructions.append([Opcodes.MOV, 1, 1, (line, 2)])
        self.string_count += 1

    def translate(self, index):
        while index < len(tokens):
            match tokens[index][0]:
                case "LET":
                    index = self.trans_let(index)
                case "NAME":
                    index = self.trans_var(index)
                case "WHILE":
                    index = self.trans_while(index)
                case "IF":
                    index = self.trans_if(index)
                case "PRINT_INT":
                    index = self.trans_print_int(index)
                case "PRINT_STR":
                    index = self.trans_print_str(index)
                case "RBRACE":
                    return index
            index += 1

    def insert_vars(self):
        for x, i in enumerate(self.instructions):
            for y, z in enumerate(self.instructions[x]):
                if isinstance(self.instructions[x][y], tuple):
                    if self.instructions[x][y][0] in self.tmp_vars and self.instructions[x][y][1] == 1:
                        self.instructions[x][y] = self.tmp_vars[self.instructions[x][y][0]]

        index = len(self.instructions) + 1
        for x, i in enumerate(self.instructions):
            for y, z in enumerate(self.instructions[x]):
                if isinstance(self.instructions[x][y], tuple):
                    if self.instructions[x][y][0] in self.vars and self.instructions[x][y][1] == 0:
                        if self.vars[self.instructions[x][y][0]] is None:
                            self.vars[self.instructions[x][y][0]] = index
                            index += 1
                        self.instructions[x][y] = self.vars[self.instructions[x][y][0]]

        for x, i in enumerate(self.instructions):
            for y, z in enumerate(self.instructions[x]):
                if isinstance(self.instructions[x][y], tuple):
                    if self.instructions[x][y][0] in self.strings and self.instructions[x][y][1] == 2:
                        if self.strings[self.instructions[x][y][0]] is None:
                            self.strings[self.instructions[x][y][0]] = index
                            index += 20
                        self.instructions[x][y] = self.strings[self.instructions[x][y][0]]

        for x, i in enumerate(self.instructions):
            for y, z in enumerate(self.instructions[x]):
                if isinstance(self.instructions[x][y], tuple):
                    if self.instructions[x][y][0] in self.strings and self.instructions[x][y][1] == 3:
                        if not isinstance(self.strings[self.instructions[x][y][0]], list):
                            self.strings[self.instructions[x][y][0]] = [index, index]
                        self.strings[self.instructions[x][y][0]][1] = index
                        if self.instructions[x][y][2] == 1:
                            self.instructions[x][y] = self.strings[self.instructions[x][y][0]][1]
                        elif self.instructions[x][y][2] == 0:
                            self.instructions[x][y] = self.strings[self.instructions[x][y][0]][0]
                        index += 1

def add_mnem(raw_instr, machine_instr, res_file):
    instructions = []
    for x in range(len(raw_instr)):
        i = raw_instr[x]
        z = machine_instr[x]
        # print(i)
        temp = f"{z} - {x}\t{hex(int(z, 2))}\t{i[0].name}"
        if i[0] in [Opcodes.INC, Opcodes.DEC]:
            instructions.append(f"{temp}\t#{i[2]}")
        elif i[0] in [Opcodes.PUSH, Opcodes.POP, Opcodes.JUMP, Opcodes.JUMPZ, Opcodes.JUMPNZ, Opcodes.JUMPNEG, Opcodes.JUMPNNEG]:
            if i[1] == 0:
                instructions.append(f"{temp}\t#{i[3]}")
            elif i[1] == 1:
                instructions.append(f"{temp}\t${i[3]}")
        elif i[0] in [Opcodes.IN, Opcodes.OUT]:
            instructions.append(f"{temp}\t#{i[2]}\t${i[3]}")
        elif i[0] in [Opcodes.HALT]:
            instructions.append(f"{temp}")
        else:
            if i[1] == 0:
                instructions.append(f"{temp}\t#{i[2]}\t#{i[3]}")
            elif i[1] == 1:
                instructions.append(f"{temp}\t#{i[2]}\t${i[3]}")
    write_codes_mnem(instructions, res_file)

def generate_machine_instruction(raw_instr, res_file):
    instructions = []
    raw_instr.append([Opcodes.HALT, 0,0,0])
    for i in raw_instr:
        instr = ""

        command = bin(i[0].value)[2:]
        instr += "0"*(5 - len(command)) + command

        type = bin(i[1])[2:]
        instr += type

        first = bin(i[2])[2:]
        instr += "0"*(4-len(first)) + first

        second = bin(i[3])[2:]
        instr += "0"*(22-len(second)) + second

        instructions.append(instr)
        # instr += "\n"
        # res_file.writelines(instr)
    add_mnem(raw_instr, instructions, res_file)
    write_codes(instructions, res_file)
    # res_file.writelines("10111000000000000000000000000000")

if __name__ == "__main__":
    a = 2
    args = sys.argv
    input_file = open(args[1], "r", encoding="utf-8")
    target_file = args[2]

    tokens = parser(input_file.read())

    # print(tokens)
    res = AST_syntax_check(tokens)
    assert res, "Ошибка в абстрактном синтаксическом дереве"

    translator = Translator()
    translator.tokens = tokens

    translator.translate(0)
    translator.insert_vars()
    # print(translator.instructions)

    generate_machine_instruction(translator.instructions, target_file)
