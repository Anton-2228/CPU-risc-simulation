from enum import Enum

class Opcodes(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    OR = 5
    AND = 6
    INC = 7#
    DEC = 8#
    CMP = 9
    PUSH = 10#
    POP = 11#
    IN = 12#
    OUT = 13#
    LOAD = 14 # в регистр
    SLOAD = 15
    STORE = 16 # в память
    JUMP = 17#
    JUMPZ = 18#
    JUMPNZ = 19#
    JUMPNEG = 20#
    JUMPNNEG = 21#
    MOV = 22
    HALT = 23


def read_codes(file):
    instruction = []
    with open(file, mode="rb") as f:
        while True:
            instr = f.read(4)
            if instr == b'':
                break
            num = int.from_bytes(instr)
            # print(format(num, "032b"))
            instruction.append(format(num, "032b"))
    return instruction + ["00000000000000000000000000000000"] * (2 ** 22 - len(instr))

def write_codes(instructions, file):
    instructions = ''.join(instructions)
    with open(file, mode="wb") as f:
        for i in range(0, len(instructions), 8):
            # print(instructions[i:i+8])
            f.write(int(instructions[i:i+8], 2).to_bytes(1, "big"))

def write_codes_mnem(instructions, file):
    source, file = file.rsplit('/', 1)
    file = f"{source}/mnem_{file}.txt"
    with open(file, mode="w", encoding="utf-8") as f:
        for i in range(len(instructions)):
            instr = instructions[i]
            if i+1 != len(instructions):
                instr += "\n"
            f.writelines(instr)

'''
Опкод | тип адресации | номер регистра | операнд
00000|0|0000|0000000000000000000000 - 32 бита

Опкод: нумерация как в классе Opcodes
тип: 0 - регистр, 1 - непосредственная
операнд - номер регистра, либо операнд
'''

