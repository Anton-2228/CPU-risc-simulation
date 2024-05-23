# from datapath import Datapath
# from control_unit import ControlUnit
# from middleware import Middleware, Memory
import numpy as np

from CPU import *

if __name__ == "__main__":
    args = sys.argv
    machine_code_file = open(args[1], "r", encoding="utf-8")
    input_file = open(args[2], "r")

    codes = write_codes(machine_code_file)

    # for i in codes:
    #     if isinstance(i, str):
    #         assert len(i) == 32, "Длина команды не 32 бита"

    input = input_file.read()

    MEM = Memory(codes)
    middleware = Middleware(MEM)
    DP = Datapath()
    CU = ControlUnit()
    IOController = IOController(input)

    middleware.datapath = DP
    middleware.control_unit = CU
    DP.middleware = middleware
    DP.control_unit = CU
    DP.iocontroller = IOController
    CU.middleware = middleware
    CU.datapath = DP
    IOController.datapath = DP
    CU.iocontroller = IOController

    Logger.init("log.txt")
    CU.start()

