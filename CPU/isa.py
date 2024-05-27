from enum import Enum

class Opcodes(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    OR = 5
    AND = 6
    INC = 7
    DEC = 8
    CMP = 9
    PUSH = 10
    POP = 11
    IN = 12
    OUT = 13
    LOAD = 14 # в регистр
    SLOAD = 15
    STORE = 16 # в память
    JUMP = 17
    JUMPZ = 18
    JUMPNZ = 19
    JUMPNEG = 20
    JUMPNNEG = 21
    MOV = 22
    HALT = 23

def write_codes(file):
    instr = file.read().strip().split("\n")
    return instr + ["00000000000000000000000000000000"] * (2 ** 22 - len(instr))

'''
Опкод | тип адресации | номер регистра | операнд
00000|0|0000|0000000000000000000000 - 32 бита

Опкод: нумерация как в классе Opcodes
тип: 0 - регистр, 1 - непосредственная
операнд - номер регистра, либо операнд
'''

