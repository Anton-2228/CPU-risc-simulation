# ruff: noqa: F403, F405

from __future__ import annotations

from CPU import *

class Logger:
    file = None
    @staticmethod
    def init(file):
        Logger.file = open(file, "w")
    line = ""
    logs:dict[str, list[RegisterBaseCell]] = {"pc":[],
            "ar":[],
            "dr":[],
            "r1":[],
            "r2":[],
            "r3":[],
            "r4":[],
            "r5":[],
            "r6":[],
            "r7":[],
            "r8":[],
            "sp":[],
            "zf":[],
            "of":[],
            "ng":[]}

    @staticmethod
    def update(datapath:Datapath, control_unit:ControlUnit, middleware:Middleware):
        Logger.logs["pc"].append(control_unit.pc.decimal)
        Logger.logs["ar"].append(middleware.ar.decimal)
        Logger.logs["dr"].append(middleware.dr.decimal)
        Logger.logs["r1"].append(datapath.gen_regs[0].decimal)
        Logger.logs["r2"].append(datapath.gen_regs[1].decimal)
        Logger.logs["r3"].append(datapath.gen_regs[2].decimal)
        Logger.logs["r4"].append(datapath.gen_regs[3].decimal)
        Logger.logs["r5"].append(datapath.gen_regs[4].decimal)
        Logger.logs["r6"].append(datapath.gen_regs[5].decimal)
        Logger.logs["r7"].append(datapath.gen_regs[6].decimal)
        Logger.logs["r8"].append(datapath.gen_regs[7].decimal)
        Logger.logs["sp"].append(datapath.sp.decimal)
        Logger.logs["zf"].append(datapath.zf)
        Logger.logs["of"].append(datapath.of)
        Logger.logs["ng"].append(datapath.ng)
    @staticmethod
    def log(datapath:Datapath, control_unit:ControlUnit, middleware:Middleware):
        Logger.line += f"pc: {str(Logger.logs['pc'][-1]) + ' -> ' if Logger.logs['pc'][-1] != control_unit.pc else ''}{control_unit.pc.decimal} | "
        Logger.line += f"ar: {str(Logger.logs['ar'][-1]) + ' -> ' if Logger.logs['ar'][-1] != middleware.ar else ''}{middleware.ar.decimal} | "
        Logger.line += f"dr: {middleware.dr} | "
        # line += f"dr: {str(Logger.logs["dr"][-1]) + " -> " if Logger.logs["dr"][-1] != middleware.dr else ""}{middleware.dr}(bin) | "
        Logger.line += f"r1: {str(Logger.logs['r1'][-1]) + ' -> ' if Logger.logs['r1'][-1] != datapath.gen_regs[0] else ''}{datapath.gen_regs[0].decimal} | "
        Logger.line += f"r2: {str(Logger.logs['r2'][-1]) + ' -> ' if Logger.logs['r2'][-1] != datapath.gen_regs[1] else ''}{datapath.gen_regs[1].decimal} | "
        Logger.line += f"r3: {str(Logger.logs['r3'][-1]) + ' -> ' if Logger.logs['r3'][-1] != datapath.gen_regs[2] else ''}{datapath.gen_regs[2].decimal} | "
        Logger.line += f"r4: {str(Logger.logs['r4'][-1]) + ' -> ' if Logger.logs['r4'][-1] != datapath.gen_regs[3] else ''}{datapath.gen_regs[3].decimal} | "
        Logger.line += f"r5: {str(Logger.logs['r5'][-1]) + ' -> ' if Logger.logs['r5'][-1] != datapath.gen_regs[4] else ''}{datapath.gen_regs[4].decimal} | "
        Logger.line += f"r6: {str(Logger.logs['r6'][-1]) + ' -> ' if Logger.logs['r6'][-1] != datapath.gen_regs[5] else ''}{datapath.gen_regs[5].decimal} | "
        Logger.line += f"r7: {str(Logger.logs['r7'][-1]) + ' -> ' if Logger.logs['r7'][-1] != datapath.gen_regs[6] else ''}{datapath.gen_regs[6].decimal} | "
        Logger.line += f"r8: {str(Logger.logs['r8'][-1]) + ' -> ' if Logger.logs['r8'][-1] != datapath.gen_regs[7] else ''}{datapath.gen_regs[7].decimal} | "
        Logger.line += f"sp: {str(Logger.logs['sp'][-1]) + ' -> ' if Logger.logs['sp'][-1] != datapath.sp else ''}{datapath.sp.decimal} | "
        Logger.line += f"zf: {str(Logger.logs['zf'][-1]) + ' -> ' if Logger.logs['zf'][-1] != datapath.zf else ''}{datapath.zf} | "
        Logger.line += f"of: {str(Logger.logs['of'][-1]) + ' -> ' if Logger.logs['of'][-1] != datapath.of else ''}{datapath.of} | "
        Logger.line += f"ng: {str(Logger.logs['ng'][-1]) + ' -> ' if Logger.logs['ng'][-1] != datapath.ng else ''}{datapath.ng} | "
        Logger.line += "\n"

        Logger.file.writelines(Logger.line)
        Logger.update(datapath, control_unit, middleware)
        Logger.line = ""
