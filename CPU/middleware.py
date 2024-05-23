from enum import Enum

import numba
from numba.experimental import jitclass
from bitstring import BitArray

# from datapath import Datapath
# from control_unit import ControlUnit
from CPU import *
from functools import lru_cache

class Signal_ip(Enum):
    SIGNAL_IP_INC = "signal_ip_inc"
    SIGNAL_IP_ALU = "signal_ip_alu"
    SIGNAL_IP_INSTR = "signal_ip_instr"

class Signal_ar(Enum):
    SIGNAL_AR_IP = "signal_ar_ip"
    SIGNAL_AR_ALU = "signal_ar_alu"

class Signal_gen_reg(Enum):
    SIGNAL_GEN_REG_1_MEM = "signal_gen_reg_1_mem"
    SIGNAL_GEN_REG_2_MEM = "signal_gen_reg_2_mem"
    SIGNAL_GEN_REG_3_MEM = "signal_gen_reg_3_mem"
    SIGNAL_GEN_REG_4_MEM = "signal_gen_reg_4_mem"
    SIGNAL_GEN_REG_5_MEM = "signal_gen_reg_5_mem"
    SIGNAL_GEN_REG_6_MEM = "signal_gen_reg_6_mem"
    SIGNAL_GEN_REG_7_MEM = "signal_gen_reg_7_mem"
    SIGNAL_GEN_REG_8_MEM = "signal_gen_reg_8_mem"

    SIGNAL_GEN_REG_1_ALU = "signal_gen_reg_1_alu"
    SIGNAL_GEN_REG_2_ALU = "signal_gen_reg_2_alu"
    SIGNAL_GEN_REG_3_ALU = "signal_gen_reg_3_alu"
    SIGNAL_GEN_REG_4_ALU = "signal_gen_reg_4_alu"
    SIGNAL_GEN_REG_5_ALU = "signal_gen_reg_5_alu"
    SIGNAL_GEN_REG_6_ALU = "signal_gen_reg_6_alu"
    SIGNAL_GEN_REG_7_ALU = "signal_gen_reg_7_alu"
    SIGNAL_GEN_REG_8_ALU = "signal_gen_reg_8_alu"

    SIGNAL_GEN_REG_1_IO = "signal_gen_reg_1_io"
    SIGNAL_GEN_REG_2_IO = "signal_gen_reg_2_io"
    SIGNAL_GEN_REG_3_IO = "signal_gen_reg_3_io"
    SIGNAL_GEN_REG_4_IO = "signal_gen_reg_4_io"
    SIGNAL_GEN_REG_5_IO = "signal_gen_reg_5_io"
    SIGNAL_GEN_REG_6_IO = "signal_gen_reg_6_io"
    SIGNAL_GEN_REG_7_IO = "signal_gen_reg_7_io"
    SIGNAL_GEN_REG_8_IO = "signal_gen_reg_8_io"

class Signal_instr(Enum):
    SIGNAL_ALL_CELL = "signal_all_cell"
    SIGNAL_BITMASK = "signal_bitmask"

class Signal_sp(Enum):
    SIGNAL_SP_INC = "signal_sp_inc"
    SIGNAL_SP_DEC = "signal_sp_dec"

class Signal_left_alu(Enum):
    SIGNAL_LEFT_ALU_SP = "signal_left_alu_sp"
    SIGNAL_LEFT_ALU_GEN_REG_1 = "signal_left_alu_gen_reg_1"
    SIGNAL_LEFT_ALU_GEN_REG_2 = "signal_left_alu_gen_reg_2"
    SIGNAL_LEFT_ALU_GEN_REG_3 = "signal_left_alu_gen_reg_3"
    SIGNAL_LEFT_ALU_GEN_REG_4 = "signal_left_alu_gen_reg_4"
    SIGNAL_LEFT_ALU_GEN_REG_5 = "signal_left_alu_gen_reg_5"
    SIGNAL_LEFT_ALU_GEN_REG_6 = "signal_left_alu_gen_reg_6"
    SIGNAL_LEFT_ALU_GEN_REG_7 = "signal_left_alu_gen_reg_7"
    SIGNAL_LEFT_ALU_GEN_REG_8 = "signal_left_alu_gen_reg_8"

class Signal_right_alu(Enum):
    SIGNAL_RIGHT_ALU_GEN_REG_1 = "signal_right_alu_gen_reg_1"
    SIGNAL_RIGHT_ALU_GEN_REG_2 = "signal_right_alu_gen_reg_2"
    SIGNAL_RIGHT_ALU_GEN_REG_3 = "signal_right_alu_gen_reg_3"
    SIGNAL_RIGHT_ALU_GEN_REG_4 = "signal_right_alu_gen_reg_4"
    SIGNAL_RIGHT_ALU_GEN_REG_5 = "signal_right_alu_gen_reg_5"
    SIGNAL_RIGHT_ALU_GEN_REG_6 = "signal_right_alu_gen_reg_6"
    SIGNAL_RIGHT_ALU_GEN_REG_7 = "signal_right_alu_gen_reg_7"
    SIGNAL_RIGHT_ALU_GEN_REG_8 = "signal_right_alu_gen_reg_8"
    SIGNAL_RIGHT_ALU_DATA_REG = "signal_right_alu_data_reg"

class Signal_reg_write(Enum):
    SIGNAL_GEN_REG_1_WRITE = "signal_gen_reg_1_write"
    SIGNAL_GEN_REG_2_WRITE = "signal_gen_reg_2_write"
    SIGNAL_GEN_REG_3_WRITE = "signal_gen_reg_3_write"
    SIGNAL_GEN_REG_4_WRITE = "signal_gen_reg_4_write"
    SIGNAL_GEN_REG_5_WRITE = "signal_gen_reg_5_write"
    SIGNAL_GEN_REG_6_WRITE = "signal_gen_reg_6_write"
    SIGNAL_GEN_REG_7_WRITE = "signal_gen_reg_7_write"
    SIGNAL_GEN_REG_8_WRITE = "signal_gen_reg_8_write"
    SIGNAL_DATA_REG_WRITE = "signal_data_reg_write"

class Signal_port(Enum):
    SIGNAL_1_PORT = "signal_1_port"
    SIGNAL_2_PORT = "signal_2_port"

class Signal_reg_write_io(Enum):
    SIGNAL_REG_1_WRITE_IO = "signal_reg_1_write_io"
    SIGNAL_REG_2_WRITE_IO = "signal_reg_2_write_io"
    SIGNAL_REG_3_WRITE_IO = "signal_reg_3_write_io"
    SIGNAL_REG_4_WRITE_IO = "signal_reg_4_write_io"
    SIGNAL_REG_5_WRITE_IO = "signal_reg_5_write_io"
    SIGNAL_REG_6_WRITE_IO = "signal_reg_6_write_io"
    SIGNAL_REG_7_WRITE_IO = "signal_reg_7_write_io"
    SIGNAL_REG_8_WRITE_IO = "signal_reg_8_write_io"

class Middleware():
    def __init__(self, memory):
        self.memory:Memory = memory
        self.ar:RegisterBaseCell = RegisterBaseCell("0")
        self.dr:RegisterBaseCell = RegisterBaseCell("0")
        # self.dr_int = RegisterBaseCell("0")
        # self.dr_short = RegisterBaseCell("0")
        self.latch_dr()
        self.datapath:Datapath = None
        self.control_unit:ControlUnit = None

    def latch_dr(self):
        self.dr.decimal = self.memory.fetched_cell.decimal

    def read_from_mem(self):
        self.memory.fetched_cell.decimal = self.memory.memory_cells[self.ar.decimal].decimal

    def write_to_mem(self, signal):
        match signal:
            case Signal_reg_write.SIGNAL_GEN_REG_1_WRITE:
                self.memory.memory_cells[self.ar.decimal].decimal = self.datapath.gen_regs[0].decimal
            case Signal_reg_write.SIGNAL_GEN_REG_2_WRITE:
                self.memory.memory_cells[self.ar.decimal].decimal = self.datapath.gen_regs[1].decimal
            case Signal_reg_write.SIGNAL_GEN_REG_3_WRITE:
                self.memory.memory_cells[self.ar.decimal].decimal = self.datapath.gen_regs[2].decimal
            case Signal_reg_write.SIGNAL_GEN_REG_4_WRITE:
                self.memory.memory_cells[self.ar.decimal].decimal = self.datapath.gen_regs[3].decimal
            case Signal_reg_write.SIGNAL_GEN_REG_5_WRITE:
                self.memory.memory_cells[self.ar.decimal].decimal = self.datapath.gen_regs[4].decimal
            case Signal_reg_write.SIGNAL_GEN_REG_6_WRITE:
                self.memory.memory_cells[self.ar.decimal].decimal = self.datapath.gen_regs[5].decimal
            case Signal_reg_write.SIGNAL_GEN_REG_7_WRITE:
                self.memory.memory_cells[self.ar.decimal].decimal = self.datapath.gen_regs[6].decimal
            case Signal_reg_write.SIGNAL_GEN_REG_8_WRITE:
                self.memory.memory_cells[self.ar.decimal].decimal = self.datapath.gen_regs[7].decimal
            case Signal_reg_write.SIGNAL_DATA_REG_WRITE:
                self.memory.memory_cells[self.ar.decimal].decimal = self.dr.short
                # self.memory.memory_cells[self.ar] = self.dr_short

    def latch_ar(self, signal):
        match signal:
            case Signal_ar.SIGNAL_AR_IP:
                self.ar.decimal = self.control_unit.pc.decimal
            case Signal_ar.SIGNAL_AR_ALU:
                self.ar.decimal = self.datapath.alu.result.decimal

@jitclass()
class RegisterBaseCell:
    def __init__(self, binary):
        self.decimal = int(binary, 2)
        # self.decimal = BitArray(bin=binary).uint

    @property
    def binary(self):
        if bin(self.decimal)[0] == "-":
            binary = bin(self.decimal)[3:]
            return "1" + "0" * (32 - len(binary) - 1) + binary
        else:
            binary = bin(self.decimal)[2:]
            return "0"*(32 - len(binary)) + binary

    @property
    def short(self):
        return int(self.binary[10:], 2)

    def __repr__(self):
        return hex(self.decimal)

    def __ne__(self, other):
        return self.decimal != other

@jitclass()
class Memory:
    def __init__(self, memory_cells):
        self.memory_cells:list[RegisterBaseCell] = [RegisterBaseCell(x) for x in memory_cells]
        self.fetched_cell:RegisterBaseCell = RegisterBaseCell("0")
        self.fetched_cell.decimal = self.memory_cells[0].decimal
