# ruff: noqa: F403, F405

# from middleware import *
# from control_unit import ControlUnit
from CPU import *


class ALU:
    def __init__(self):
        self.datapath:Datapath = None
        self.left_input:RegisterBaseCell = RegisterBaseCell("0")
        self.right_input:RegisterBaseCell = RegisterBaseCell("0")
        self.result:RegisterBaseCell = RegisterBaseCell("0")
        self.current_port = None

    def add(self):
        self.result.decimal = self.left_input.decimal + self.right_input.decimal
        self.set_flags()

    def sub(self):
        self.result.decimal = self.left_input.decimal - self.right_input.decimal
        self.set_flags()

    def mul(self):
        self.result.decimal = self.left_input.decimal * self.right_input.decimal
        self.set_flags()

    def div(self):
        self.result.decimal = self.left_input.decimal // self.right_input.decimal
        self.set_flags()

    def mod(self):
        self.result.decimal = self.left_input.decimal % self.right_input.decimal
        self.set_flags()

    def or_(self):
        self.result.decimal = self.left_input.decimal | self.right_input.decimal
        self.set_flags()

    def and_(self):
        self.result.decimal = self.left_input.decimal & self.right_input.decimal
        self.set_flags()

    def inc(self):
        self.result.decimal = self.left_input.decimal + 1
        self.set_flags()

    def dec(self):
        self.result.decimal = self.left_input.decimal - 1
        self.set_flags()

    def nop_l(self):
        self.result.decimal = self.left_input.decimal
        self.set_flags()

    def nop_r(self):
        self.result.decimal = self.right_input.decimal
        self.set_flags()

    def set_flags(self):
        self.overflow_check()
        self.zero_check()
        self.negative_check()

    def zero_check(self):
        if self.result.decimal == 0:
            self.datapath.zf = 1
        else:
            self.datapath.zf = 0

    def overflow_check(self):
        if self.result.decimal < -2**31:
            self.datapath.of = 1
            self.result.decimal = 2**32 - (-2**31 - self.result.decimal)
        elif self.result.decimal >= 2**31:
            self.datapath.of = 1
            self.result.decimal = -2**31 + (self.result.decimal - 2**31)
        else:
            self.datapath.of = 0

    def negative_check(self):
        if self.result.decimal < 0:
            self.datapath.ng = 1
        else:
            self.datapath.ng = 0

class Datapath:
    def __init__(self):
        self.alu = ALU()
        self.alu.datapath = self
        self.gen_regs:list[RegisterBaseCell] = [RegisterBaseCell("0") for _ in range(8)]
        self.sp:RegisterBaseCell = RegisterBaseCell(bin(2**22))
        self.zf = 0
        self.of = 0
        self.ng = 0
        self.middleware:Middleware = None
        self.control_unit:ControlUnit = None
        self.iocontroller:IOController = None

    def latch_port(self, signal):
        match signal:
            case Signal_port.SIGNAL_1_PORT:
                self.current_port = 1
            case Signal_port.SIGNAL_2_PORT:
                self.current_port = 2

    def latch_general_regs(self, signal, signal_instr):
        match signal_instr:
            case Signal_instr.SIGNAL_ALL_CELL:
                value_from_mem = self.middleware.dr.decimal
            case Signal_instr.SIGNAL_BITMASK:
                value_from_mem = self.middleware.dr.short

        match signal:
            case Signal_gen_reg.SIGNAL_GEN_REG_1_MEM:
                self.gen_regs[0].decimal = value_from_mem
            case Signal_gen_reg.SIGNAL_GEN_REG_2_MEM:
                self.gen_regs[1].decimal = value_from_mem
            case Signal_gen_reg.SIGNAL_GEN_REG_3_MEM:
                self.gen_regs[2].decimal = value_from_mem
            case Signal_gen_reg.SIGNAL_GEN_REG_4_MEM:
                self.gen_regs[3].decimal = value_from_mem
            case Signal_gen_reg.SIGNAL_GEN_REG_5_MEM:
                self.gen_regs[4].decimal = value_from_mem
            case Signal_gen_reg.SIGNAL_GEN_REG_6_MEM:
                self.gen_regs[5].decimal = value_from_mem
            case Signal_gen_reg.SIGNAL_GEN_REG_7_MEM:
                self.gen_regs[6].decimal = value_from_mem
            case Signal_gen_reg.SIGNAL_GEN_REG_8_MEM:
                self.gen_regs[7].decimal = value_from_mem

            case Signal_gen_reg.SIGNAL_GEN_REG_1_ALU:
                self.gen_regs[0].decimal = self.alu.result.decimal
            case Signal_gen_reg.SIGNAL_GEN_REG_2_ALU:
                self.gen_regs[1].decimal = self.alu.result.decimal
            case Signal_gen_reg.SIGNAL_GEN_REG_3_ALU:
                self.gen_regs[2].decimal = self.alu.result.decimal
            case Signal_gen_reg.SIGNAL_GEN_REG_4_ALU:
                self.gen_regs[3].decimal = self.alu.result.decimal
            case Signal_gen_reg.SIGNAL_GEN_REG_5_ALU:
                self.gen_regs[4].decimal = self.alu.result.decimal
            case Signal_gen_reg.SIGNAL_GEN_REG_6_ALU:
                self.gen_regs[5].decimal = self.alu.result.decimal
            case Signal_gen_reg.SIGNAL_GEN_REG_7_ALU:
                self.gen_regs[6].decimal = self.alu.result.decimal
            case Signal_gen_reg.SIGNAL_GEN_REG_8_ALU:
                self.gen_regs[7].decimal = self.alu.result.decimal

            case Signal_gen_reg.SIGNAL_GEN_REG_1_IO:
                self.gen_regs[0].decimal = self.iocontroller.get_top_buffer(self.current_port)
            case Signal_gen_reg.SIGNAL_GEN_REG_2_IO:
                self.gen_regs[1].decimal = self.iocontroller.get_top_buffer(self.current_port)
            case Signal_gen_reg.SIGNAL_GEN_REG_3_IO:
                self.gen_regs[2].decimal = self.iocontroller.get_top_buffer(self.current_port)
            case Signal_gen_reg.SIGNAL_GEN_REG_4_IO:
                self.gen_regs[3].decimal = self.iocontroller.get_top_buffer(self.current_port)
            case Signal_gen_reg.SIGNAL_GEN_REG_5_IO:
                self.gen_regs[4].decimal = self.iocontroller.get_top_buffer(self.current_port)
            case Signal_gen_reg.SIGNAL_GEN_REG_6_IO:
                self.gen_regs[5].decimal = self.iocontroller.get_top_buffer(self.current_port)
            case Signal_gen_reg.SIGNAL_GEN_REG_7_IO:
                self.gen_regs[6].decimal = self.iocontroller.get_top_buffer(self.current_port)
            case Signal_gen_reg.SIGNAL_GEN_REG_8_IO:
                self.gen_regs[7].decimal = self.iocontroller.get_top_buffer(self.current_port)

    def latch_sp(self, signal):
        match signal:
            case Signal_sp.SIGNAL_SP_INC:
                self.sp.decimal += 1
            case Signal_sp.SIGNAL_SP_DEC:
                self.sp.decimal -= 1

    def latch_left_alu(self, signal):
        match signal:
            case Signal_left_alu.SIGNAL_LEFT_ALU_GEN_REG_1:
                self.alu.left_input.decimal = self.gen_regs[0].decimal
            case Signal_left_alu.SIGNAL_LEFT_ALU_GEN_REG_2:
                self.alu.left_input.decimal = self.gen_regs[1].decimal
            case Signal_left_alu.SIGNAL_LEFT_ALU_GEN_REG_3:
                self.alu.left_input.decimal = self.gen_regs[2].decimal
            case Signal_left_alu.SIGNAL_LEFT_ALU_GEN_REG_4:
                self.alu.left_input.decimal = self.gen_regs[3].decimal
            case Signal_left_alu.SIGNAL_LEFT_ALU_GEN_REG_5:
                self.alu.left_input.decimal = self.gen_regs[4].decimal
            case Signal_left_alu.SIGNAL_LEFT_ALU_GEN_REG_6:
                self.alu.left_input.decimal = self.gen_regs[5].decimal
            case Signal_left_alu.SIGNAL_LEFT_ALU_GEN_REG_7:
                self.alu.left_input.decimal = self.gen_regs[6].decimal
            case Signal_left_alu.SIGNAL_LEFT_ALU_GEN_REG_8:
                self.alu.left_input.decimal = self.gen_regs[7].decimal
            case Signal_left_alu.SIGNAL_LEFT_ALU_SP:
                self.alu.left_input.decimal = self.sp.decimal

    def latch_right_alu(self, signal):
        match signal:
            case Signal_right_alu.SIGNAL_RIGHT_ALU_GEN_REG_1:
                self.alu.right_input.decimal = self.gen_regs[0].decimal
            case Signal_right_alu.SIGNAL_RIGHT_ALU_GEN_REG_2:
                self.alu.right_input.decimal = self.gen_regs[1].decimal
            case Signal_right_alu.SIGNAL_RIGHT_ALU_GEN_REG_3:
                self.alu.right_input.decimal = self.gen_regs[2].decimal
            case Signal_right_alu.SIGNAL_RIGHT_ALU_GEN_REG_4:
                self.alu.right_input.decimal = self.gen_regs[3].decimal
            case Signal_right_alu.SIGNAL_RIGHT_ALU_GEN_REG_5:
                self.alu.right_input.decimal = self.gen_regs[4].decimal
            case Signal_right_alu.SIGNAL_RIGHT_ALU_GEN_REG_6:
                self.alu.right_input.decimal = self.gen_regs[5].decimal
            case Signal_right_alu.SIGNAL_RIGHT_ALU_GEN_REG_7:
                self.alu.right_input.decimal = self.gen_regs[6].decimal
            case Signal_right_alu.SIGNAL_RIGHT_ALU_GEN_REG_8:
                self.alu.right_input.decimal = self.gen_regs[7].decimal
            case Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG:
                self.alu.right_input.decimal = self.middleware.dr.short