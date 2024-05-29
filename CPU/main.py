# ruff: noqa: F403, F405

from CPU import *
import sys

if __name__ == "__main__":
    args = sys.argv
    machine_code_file = args[1]
    input_1_file = args[2]
    input_2_file = args[3]
    output_1_file = args[4]
    output_2_file = args[5]
    log_file = args[6]

    codes = read_codes(machine_code_file)
    for i in codes:
        if isinstance(i, str):
            assert len(i) == 32, "Длина команды не 32 бита"

    MEM = Memory(codes)
    middleware = Middleware(MEM)
    DP = Datapath()
    CU = ControlUnit()
    IOController = IOController(input_1_file, input_2_file, output_1_file, output_2_file)

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
