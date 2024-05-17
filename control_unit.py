from isa import *
from datapath import ALU

class Register:
    def __init__(self, value):
        self.value = value

class Signal(Enum):
    SIGNAL_IP_INC = "signal_ip_inc"
    SIGNAL_IP_ALU = "signal_ip_alu"

    SIGNAL_AR_IP = "signal_ar_ip"
    SIGNAL_AR_ALU = "signal_ar_alu"

    # ПОМЕНЯТЬ НА ОТДЕЛЬНЫЕ СИГНАЛЫ ПОХУЙ НА ИХ КОЛИЧЕСТВО
    SIGNAL_GEN_REG_MEM = lambda x: f"{x}_mem"
    SIGNAL_GEN_REG_ALU = lambda x: f"{x}_alu"
    SIGNAL_SP_INC = "signal_sp_inc"
    SIGNAL_SP_DEC = "signal_sp_dec"

    # ПОМЕНЯТЬ НА ОТДЕЛЬНЫЕ СИГНАЛЫ ПОХУЙ НА ИХ КОЛИЧЕСТВО
    SIGNAL_LEFT_ALU_GEN_REG = lambda x: f"signal_left_alu_gen_reg{x}"
    SIGNAL_LEFT_ALU_SP = "signal_left_alu_sp"

    # ПОМЕНЯТЬ НА ОТДЕЛЬНЫЕ СИГНАЛЫ ПОХУЙ НА ИХ КОЛИЧЕСТВО
    SIGNAL_RIGHT_ALU_GEN_REG = lambda x: f"signal_right_alu_gen_reg{x}"

class ControlUnit:
    def __init__(self, DP):
        self.pc = Register(1)
        self.ar = Register(0)
        self.DP = DP

    def latch_ip(self, signal):
        match signal:
            case Signal.SIGNAL_IP_INC:
                self.pc.value += 1
            case Signal.SIGNAL_IP_ALU:
                self.pc.value = self.DP.alu.result

    def latch_addr(self, signal):
        match signal:
            case Signal.SIGNAL_AR_IP:
                self.ar = self.pc.value
            case Signal.SIGNAL_AR_ALU:
                self.ar = self.DP.alu.result

    def decoder(self, memory_data):
        command = int(memory_data[:5], 2)
        addr_type = int(memory_data[5:6], 2)
        first_operand = int(memory_data[6:10], 2)
        second_operand = int(memory_data[10:], 2)

        match command:
            case Opcodes.ADD.value:
                pass
            case Opcodes.SUB.value:
                pass
            case Opcodes.MUL.value:
                pass
            case Opcodes.DIV.value:
                pass
            case Opcodes.MOD.value:
                pass
            case Opcodes.INC.value:
                pass
            case Opcodes.DEC.value:
                pass
            case Opcodes.PUSH.value:
                pass
            case Opcodes.POP.value:
                pass
            case Opcodes.IN.value:
                pass
            case Opcodes.OUT.value:
                pass
            case Opcodes.LOAD.value:
                pass
            case Opcodes.STORE.value:
                pass
            case Opcodes.JUMP.value:
                pass
            case Opcodes.JUMPZ.value:
                pass
            case Opcodes.JUMPNZ.value:
                pass
            case Opcodes.HALT.value:
                pass
