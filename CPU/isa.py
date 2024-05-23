from enum import Enum

class Opcodes(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    OR = 5
    INC = 6
    DEC = 7
    CMP = 8
    PUSH = 9
    POP = 10
    IN = 11
    OUT = 12
    LOAD = 13 # в регистр
    SLOAD = 14
    STORE = 15 # в память
    JUMP = 16
    JUMPZ = 17
    JUMPNZ = 18
    JUMPNEG = 19
    JUMPNNEG = 20
    MOV = 21
    HALT = 22

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

