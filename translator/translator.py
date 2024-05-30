import sys

from reverse_polish_notation import reverse_polish_notation
from parser import parser
from CPU.isa import Opcodes, write_codes_mnem, write_codes
from ast_check import AST_syntax_check


class Translator:
    def __init__(self):
        self.vars = {}
        self.instructions = []
        self.tokens = None
        self.tmp_var_counter = 0
        self.tmp_vars = {}
        self.strings = {}
        self.string_count = 0
        self.static_string = {}
        self.data = {}

    def arifm_op(self, token, deep):
        match token:
            case "PLUS":
                opcode = Opcodes.ADD
            case "MINUS":
                opcode = Opcodes.SUB
            case "MUL":
                opcode = Opcodes.MUL
            case "DIV":
                opcode = Opcodes.DIV
            case "MOD":
                opcode = Opcodes.MOD
            case "OR":
                opcode = Opcodes.OR
            case "AND":
                opcode = Opcodes.AND

        if deep < 7:
            self.instructions.append([opcode, 0, deep - 1, deep])
        elif deep == 7:
            self.instructions.append([Opcodes.POP, 0, 0, 7])
            self.instructions.append([opcode, 0, 6, 7])
        else:
            self.instructions.append([Opcodes.POP, 0, 0, 8])
            self.instructions.append([Opcodes.POP, 0, 0, 7])
            self.instructions.append([opcode, 0, 7, 8])
            self.instructions.append([Opcodes.PUSH, 0, 0, 7])

    def logic_op(self, token, deep):
        match token:
            case "EQ":
                jump_type = Opcodes.JUMPNZ
            case "NEQ":
                jump_type = Opcodes.JUMPZ
            case "GT":
                jump_type = Opcodes.JUMPNNEG
            case "LT":
                jump_type = Opcodes.JUMPNEG

        if deep < 7:
            self.instructions.append([Opcodes.CMP, 0, deep - 1, deep])
            self.instructions.append([jump_type, 1, 0, len(self.instructions) + 3])
            self.instructions.append([Opcodes.MOV, 1, deep - 1, 1])
            self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
            self.instructions.append([Opcodes.MOV, 1, deep - 1, 0])
        elif deep == 7:
            self.instructions.append([Opcodes.POP, 0, 0, 7])
            self.instructions.append([Opcodes.CMP, 0, 6, 7])
            self.instructions.append([jump_type, 1, 0, len(self.instructions) + 3])
            self.instructions.append([Opcodes.MOV, 1, 6, 1])
            self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
            self.instructions.append([Opcodes.MOV, 1, 6, 0])
        else:
            self.instructions.append([Opcodes.POP, 0, 0, 8])
            self.instructions.append([Opcodes.POP, 0, 0, 7])
            self.instructions.append([Opcodes.CMP, 0, 7, 8])
            self.instructions.append([jump_type, 1, 0, len(self.instructions) + 3])
            self.instructions.append([Opcodes.MOV, 1, 7, 1])
            self.instructions.append([Opcodes.JUMP, 1, 0, len(self.instructions) + 2])
            self.instructions.append([Opcodes.MOV, 1, 7, 0])
            self.instructions.append([Opcodes.PUSH, 0, 0, 7])

    def trans_expr(self, expr):
        polish = reverse_polish_notation(expr)
        deep = 0
        for i in polish:
            match i[0]:
                case "PLUS":
                    self.arifm_op("PLUS", deep)
                    deep -= 1
                case "MINUS":
                    self.arifm_op("MINUS", deep)
                    deep -= 1
                case "MUL":
                    self.arifm_op("MUL", deep)
                    deep -= 1
                case "DIV":
                    self.arifm_op("DIV", deep)
                    deep -= 1
                case "MOD":
                    self.arifm_op("MOD", deep)
                    deep -= 1
                case "OR":
                    self.arifm_op("OR", deep)
                    deep -= 1
                case "AND":
                    self.arifm_op("AND", deep)
                    deep -= 1
                case "NEQ":
                    self.logic_op("NEQ", deep)
                    deep -= 1
                case "EQ":
                    self.logic_op("EQ", deep)
                    deep -= 1
                case "GT":
                    self.logic_op("GT", deep)
                    deep -= 1
                case "LT":
                    self.logic_op("LT", deep)
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
                self.static_string[var] = tokens[index + 3][1][1:-1]
            case "INPUT_STR":
                self.input_str()
                self.instructions.append([Opcodes.STORE, 1, 1, (var, 0)])
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
                self.static_string[var] = tokens[index + 2][1][1:-1]
            case "INPUT_STR":
                self.input_str()
                self.instructions.append([Opcodes.STORE, 1, 1, (var, 0)])
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
        if self.tokens[index+2][0] == "NAME":
            self.instructions.append([Opcodes.LOAD, 1, 1, (self.tokens[index+2][1], 0)])
        elif self.tokens[index+2][0] == "STRING":
            self.static_string[self.string_count] = tokens[index + 2][1][1:-1]
            self.instructions.append([Opcodes.MOV, 1, 1, (self.string_count, 3)])
            self.string_count += 1
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

        static_string_addr = {}
        for i in self.static_string:
            if isinstance(i, str):
                self.data[self.vars[i]] = index
            static_string_addr[i] = index
            self.data[index] = len(self.static_string[i])
            index += 1
            for z in self.static_string[i]:
                self.data[index] = ord(z)
                index += 1

        for x, i in enumerate(self.instructions):
            for y, z in enumerate(self.instructions[x]):
                if isinstance(self.instructions[x][y], tuple):
                    if self.instructions[x][y][0] in self.static_string and self.instructions[x][y][1] == 3:
                        self.instructions[x][y] = static_string_addr[self.instructions[x][y][0]]

def add_mnem(raw_instr, machine_instr, res_file):
    instructions = []
    for x in range(len(raw_instr)):
        i = raw_instr[x]
        z = machine_instr[x]
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

def generate_machine_instruction(translator, res_file):
    raw_instr = translator.instructions
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
    add_mnem(raw_instr, instructions, res_file)

    for i in translator.data:
        while len(instructions) <= i:
            instructions.append("00000000000000000000000000000000")
        instructions[i] = format(translator.data[i], "032b")

    write_codes(instructions, res_file)

if __name__ == "__main__":
    a = 2
    args = sys.argv
    input_file = open(args[1], "r", encoding="utf-8")
    target_file = args[2]

    tokens = parser(input_file.read())

    res = AST_syntax_check(tokens)
    assert res, "Ошибка в абстрактном синтаксическом дереве"

    translator = Translator()
    translator.tokens = tokens

    translator.translate(0)
    translator.insert_vars()

    generate_machine_instruction(translator, target_file)
