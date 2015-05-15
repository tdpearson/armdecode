__author__ = 'tdp'
from Decode.utils import isZeroBit

class DataProcessing():
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def MOV(self, args):
        if args['encoding'] == 'A1-I':
            '''S, Rd, imm12'''
            pass
        if args['encoding'] == 'A1-R':
            Rm = self.registers[args['Rm']]
            self.registers[args['Rd']] = Rm
            self.process_mode.CPSR.negative_flag = Rm >> 31
            self.process_mode.CPSR.zero_flag = isZeroBit(Rm)
            print("moved %s to R%s from R%s" % (Rm, args['Rd'], args['Rm']))