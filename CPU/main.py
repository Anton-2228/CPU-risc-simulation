# ruff: noqa: F403, F405

# from datapath import Datapath
# from control_unit import ControlUnit
# from middleware import Middleware, Memory

from CPU import *
import sys

if __name__ == "__main__":
    args = sys.argv
    machine_code_file = open(args[1], "r", encoding="utf-8")
    input_str_file = open(args[2], "r")
    input_int_file = open(args[3], "r")
    output_str_file = args[4]
    output_int_file = args[5]
    log_file = open(args[6], "w")

    codes = write_codes(machine_code_file)

    for i in codes:
        if isinstance(i, str):
            assert len(i) == 32, "Длина команды не 32 бита"

    MEM = Memory(codes)
    middleware = Middleware(MEM)
    DP = Datapath()
    CU = ControlUnit()
    IOController = IOController(input_str_file, input_int_file, output_str_file, output_int_file)

    middleware.datapath = DP
    middleware.control_unit = CU
    DP.middleware = middleware
    DP.control_unit = CU
    DP.iocontroller = IOController
    CU.middleware = middleware
    CU.datapath = DP
    IOController.datapath = DP
    CU.iocontroller = IOController

    Logger.init(log_file)
    CU.start()

    # in_str = False
    # len_str = 0
    # i = 0
    # with open(IOController.output_file[1], 'r') as file:
    #     data = loads(file.read())["outputs"]
    #     while i < len(data):
    #         if in_str:
    #             for z in range(len_str):
    #                 print(chr(data[i]), end='')
    #                 i += 1
    #         else:
    #             in_str = True
    #             len_str = data[i]
    #             i += 1
    #
    # print("\n")
    #
    # i = 0
    # with open(IOController.output_file[2], 'r') as file:
    #     data = loads(file.read())["outputs"]
    #     while i < len(data):
    #         print(str(data[i]), end='')
    #         i += 1
