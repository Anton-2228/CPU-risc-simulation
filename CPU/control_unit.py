# ruff: noqa: F403, F405

# from isa import *
# from middleware import *
# from datapath import Datapath
# from CPU import *
import sys

from CPU import *


class ControlUnit:
    def __init__(self):
        self.pc:RegisterBaseCell = RegisterBaseCell("0")
        self.datapath:Datapath = None
        self.middleware:Middleware = None
        self.iocontroller:IOController = None

    def latch_ip(self, signal):
        match signal:
            case Signal_ip.SIGNAL_IP_INC:
                self.pc.decimal += 1
            case Signal_ip.SIGNAL_IP_ALU:
                self.pc.decimal = self.datapath.alu.result.decimal
            case Signal_ip.SIGNAL_IP_INSTR:
                self.pc.decimal = self.middleware.dr.short

    def decoder(self):
        memory_data = self.middleware.dr.binary
        command = int(memory_data[:5], 2)
        addr_type = int(memory_data[5], 2)
        first_operand = int(memory_data[6:10], 2)
        second_operand = int(memory_data[10:], 2)

        Logger.line += f"command: {hex(command)} - {Opcodes(command).name} | "

        match command:
            case Opcodes.ADD.value:
                self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{first_operand}"))
                if addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                elif addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                self.datapath.alu.add()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_alu"), 0)
            case Opcodes.SUB.value:
                self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{first_operand}"))
                if addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                elif addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                self.datapath.alu.sub()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_alu"), 0)
            case Opcodes.MUL.value:
                self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{first_operand}"))
                if addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                elif addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                self.datapath.alu.mul()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_alu"), 0)
            case Opcodes.DIV.value:
                self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{first_operand}"))
                if addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                elif addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                self.datapath.alu.div()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_alu"), 0)
            case Opcodes.MOD.value:
                self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{first_operand}"))
                if addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                elif addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                self.datapath.alu.mod()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_alu"), 0)
            case Opcodes.OR.value:
                self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{first_operand}"))
                if addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                elif addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                self.datapath.alu.or_()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_alu"), 0)
            case Opcodes.INC.value:
                self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{first_operand}"))
                if addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                elif addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                self.datapath.alu.inc()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_alu"), 0)
            case Opcodes.DEC.value:
                self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{first_operand}"))
                if addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                elif addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                self.datapath.alu.dec()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_alu"), 0)
            case Opcodes.CMP.value:
                self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{first_operand}"))
                if addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                elif addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                self.datapath.alu.sub()
            case Opcodes.PUSH.value:
                self.datapath.latch_sp(Signal_sp.SIGNAL_SP_DEC)
                self.datapath.latch_left_alu(Signal_left_alu.SIGNAL_LEFT_ALU_SP)
                self.datapath.alu.nop_l()
                self.middleware.latch_ar(Signal_ar.SIGNAL_AR_ALU)
                if addr_type == 1:
                    self.middleware.write_to_mem(Signal_reg_write.SIGNAL_DATA_REG_WRITE)
                elif addr_type == 0:
                    self.middleware.write_to_mem(Signal_reg_write(f"signal_gen_reg_{second_operand}_write"))
            case Opcodes.POP.value:
                self.datapath.latch_left_alu(Signal_left_alu.SIGNAL_LEFT_ALU_SP)
                self.datapath.latch_sp(Signal_sp.SIGNAL_SP_INC)
                self.datapath.alu.nop_l()
                self.middleware.latch_ar(Signal_ar.SIGNAL_AR_ALU)
                self.middleware.read_from_mem()
                self.middleware.latch_dr()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{second_operand}_mem"), Signal_instr.SIGNAL_ALL_CELL)
            case Opcodes.IN.value:
                self.datapath.latch_port(Signal_port(f"signal_{second_operand}_port"))
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_io"), 0)
            case Opcodes.OUT.value:
                self.iocontroller.latch_port(Signal_port(f"signal_{second_operand}_port"))
                self.iocontroller.latch_data(Signal_reg_write_io(f"signal_reg_{first_operand}_write_io"))
            case Opcodes.LOAD.value:
                if addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                elif addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                self.datapath.alu.nop_r()
                self.middleware.latch_ar(Signal_ar.SIGNAL_AR_ALU)
                self.middleware.read_from_mem()
                self.middleware.latch_dr()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_mem"), Signal_instr.SIGNAL_ALL_CELL)
            case Opcodes.SLOAD.value:
                self.datapath.latch_left_alu(Signal_left_alu.SIGNAL_LEFT_ALU_SP)
                if addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                elif addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                self.datapath.alu.add()
                self.middleware.latch_ar(Signal_ar.SIGNAL_AR_ALU)
                self.middleware.read_from_mem()
                self.middleware.latch_dr()
                self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_mem"), Signal_instr.SIGNAL_ALL_CELL)
            case Opcodes.STORE.value:
                if addr_type == 1:
                    self.datapath.latch_right_alu(Signal_right_alu.SIGNAL_RIGHT_ALU_DATA_REG)
                elif addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                self.datapath.alu.nop_r()
                self.middleware.latch_ar(Signal_ar.SIGNAL_AR_ALU)
                self.middleware.write_to_mem(Signal_reg_write(f"signal_gen_reg_{first_operand}_write"))
            case Opcodes.JUMP.value:
                if addr_type == 1:
                    self.latch_ip(Signal_ip.SIGNAL_IP_INSTR)
                elif addr_type == 0:
                    self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                    self.datapath.alu.nop_r()
                    self.latch_ip(Signal_ip.SIGNAL_IP_ALU)
            case Opcodes.JUMPZ.value:
                if self.datapath.zf == 1:
                    if addr_type == 1:
                        self.latch_ip(Signal_ip.SIGNAL_IP_INSTR)
                    elif addr_type == 0:
                        self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                        self.datapath.alu.nop_r()
                        self.latch_ip(Signal_ip.SIGNAL_IP_ALU)
            case Opcodes.JUMPNZ.value:
                if self.datapath.zf == 0:
                    if addr_type == 1:
                        self.latch_ip(Signal_ip.SIGNAL_IP_INSTR)
                    elif addr_type == 0:
                        self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                        self.datapath.alu.nop_r()
                        self.latch_ip(Signal_ip.SIGNAL_IP_ALU)
            case Opcodes.JUMPNEG.value:
                if self.datapath.ng == 1:
                    if addr_type == 1:
                        self.latch_ip(Signal_ip.SIGNAL_IP_INSTR)
                    elif addr_type == 0:
                        self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                        self.datapath.alu.nop_r()
                        self.latch_ip(Signal_ip.SIGNAL_IP_ALU)
            case Opcodes.JUMPNNEG.value:
                if self.datapath.ng == 0:
                    if addr_type == 1:
                        self.latch_ip(Signal_ip.SIGNAL_IP_INSTR)
                    elif addr_type == 0:
                        self.datapath.latch_right_alu(Signal_right_alu(f"signal_right_alu_gen_reg_{second_operand}"))
                        self.datapath.alu.nop_r()
                        self.latch_ip(Signal_ip.SIGNAL_IP_ALU)
            case Opcodes.MOV.value:
                if addr_type == 1:
                    self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_mem"), Signal_instr.SIGNAL_BITMASK)
                elif addr_type == 0:
                    self.datapath.latch_left_alu(Signal_left_alu(f"signal_left_alu_gen_reg_{second_operand}"))
                    self.datapath.alu.nop_l()
                    self.datapath.latch_general_regs(Signal_gen_reg(f"signal_gen_reg_{first_operand}_alu"), 0)
            case Opcodes.HALT.value:
                # print([x.decimal for x in self.middleware.memory.memory_cells[:50]])
                return 1
        return 0
        # print([x.decimal for x in self.middleware.memory.memory_cells[:50]])

    def start(self):
        Logger.update(self.datapath, self, self.middleware)
        while True:
            Logger.log(self.datapath, self, self.middleware)
            self.middleware.latch_ar(Signal_ar.SIGNAL_AR_IP)
            self.latch_ip(Signal_ip.SIGNAL_IP_INC)
            self.middleware.read_from_mem()
            self.middleware.latch_dr()
            ret = self.decoder()
            if ret == 1:
                return
