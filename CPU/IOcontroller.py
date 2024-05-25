from CPU import *
from json import loads

class IOController:
    def __init__(self, input_str_file, input_int_file):
        self.datapath:Datapath = None
        self.current_port = None
        input_int = loads(input_int_file.read())
        input_str = loads(input_str_file.read())

        self.input_buffers = {1:input_str,
                              2:input_int}
        self.output_buffers = {1:[],
                               2:[]}
        self.output_file = {1:open("outputs/output_str.txt", "w"),
                            2:open("outputs/output_int.txt", "w")}

    def latch_port(self, signal):
        match signal:
            case Signal_port.SIGNAL_1_PORT:
                self.current_port = 1
            case Signal_port.SIGNAL_2_PORT:
                self.current_port = 2

    def latch_data(self, signal):
        match signal:
            case Signal_reg_write_io.SIGNAL_REG_1_WRITE_IO:
                self.output_buffers[self.current_port].append(self.datapath.gen_regs[0].decimal)
            case Signal_reg_write_io.SIGNAL_REG_2_WRITE_IO:
                self.output_buffers[self.current_port].append(self.datapath.gen_regs[1].decimal)
            case Signal_reg_write_io.SIGNAL_REG_3_WRITE_IO:
                self.output_buffers[self.current_port].append(self.datapath.gen_regs[2].decimal)
            case Signal_reg_write_io.SIGNAL_REG_4_WRITE_IO:
                self.output_buffers[self.current_port].append(self.datapath.gen_regs[3].decimal)
            case Signal_reg_write_io.SIGNAL_REG_5_WRITE_IO:
                self.output_buffers[self.current_port].append(self.datapath.gen_regs[4].decimal)
            case Signal_reg_write_io.SIGNAL_REG_6_WRITE_IO:
                self.output_buffers[self.current_port].append(self.datapath.gen_regs[5].decimal)
            case Signal_reg_write_io.SIGNAL_REG_7_WRITE_IO:
                self.output_buffers[self.current_port].append(self.datapath.gen_regs[6].decimal)
            case Signal_reg_write_io.SIGNAL_REG_8_WRITE_IO:
                self.output_buffers[self.current_port].append(self.datapath.gen_regs[7].decimal)
        if self.current_port == 1:
            self.output_file[self.current_port].writelines(chr(self.output_buffers[self.current_port][-1]))
        elif self.current_port == 2:
            self.output_file[self.current_port].writelines(str(self.output_buffers[self.current_port][-1]))
        # print(self.output_buffers[1])

    def get_top_buffer(self, port):
        if port == 1:
            if isinstance(self.input_buffers[port]["inputs"][0], str):
                return ord(self.input_buffers[port]["inputs"].pop(0))
            elif isinstance(self.input_buffers[port]["inputs"][0], int):
                return self.input_buffers[port]["inputs"].pop(0)
        elif port == 2:
            return self.input_buffers[port]["inputs"].pop(0)
