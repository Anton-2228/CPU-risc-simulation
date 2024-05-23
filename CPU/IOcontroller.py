from CPU import *

class IOController:
    def __init__(self, input):
        self.datapath:Datapath = None
        self.current_port = None
        input_obr = []
        for i in input:
            input_obr += [len(list(i))]+list(i)
        # print(input_obr)
        self.input_buffers = {1:input_obr,
                              2:[]}
        self.output_buffers = {1:[],
                               2:[]}
        self.output_file = {1:open("output1.txt", "w"),
                            2:open("output2.txt", "w")}

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
        # print(self.input_buffers[1])
        # print(self.input_buffers[port])
        if isinstance(self.input_buffers[port][0], str):
            return ord(self.input_buffers[port].pop(0))
        else:
            return self.input_buffers[port].pop(0)