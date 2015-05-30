__author__ = 'tdp'
from Decode.utils import isZeroBit, hexprint
from Execute.utils import shift_c

class DataProcessing:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def ADC(self, args):
        raise NotImplementedError

    def ADD(self, args):
        raise NotImplementedError

    def ADR(self, args):
        raise NotImplementedError

    def AND(self, args):
        if args['encoding'] == 'A1-R':
            '''S, Rn, Rd, imm5, type, Rm'''
            raise NotImplementedError
        if args['encoding'] == 'A1-RSR':
            raise NotImplementedError
        if args['encoding'] == 'A1-I':
            raise NotImplementedError
        if args['encoding'] == 'T1-R':
            raise NotImplementedError
        if args['encoding'] == 'T2-R':
            raise NotImplementedError
        if args['encoding'] == 'T1-I':
            raise NotImplementedError

    def ASR(self, args):
        raise NotImplementedError

    def BIC(self, args):
        raise NotImplementedError

    def CMN(self, args):
        raise NotImplementedError

    def CMP(self, args):
        raise NotImplementedError

    def EOR(self, args):
        raise NotImplementedError

    def LSL(self, args):
        raise NotImplementedError

    def LSR(self, args):
        raise NotImplementedError

    def MOV(self, args):
        if args['encoding'] == 'A1-I':
            '''S, Rd, imm12'''
            raise NotImplementedError
        if args['encoding'] == 'A1-R':
            Rm = self.registers[args['Rm']]
            self.registers[args['Rd']] = Rm
            self.process_mode.CPSR.negative_flag = Rm >> 31
            self.process_mode.CPSR.zero_flag = isZeroBit(Rm)
            print("moved %s to R%s from R%s" % (Rm, args['Rd'], args['Rm']))

    def MVN(self, args):
        raise NotImplementedError

    def ORR(self, args):
        raise NotImplementedError

    def RSB(self, args):
        raise NotImplementedError

    def RSC(self, args):
        raise NotImplementedError

    def RRX(self, args):
        raise NotImplementedError

    def SBC(self, args):
        raise NotImplementedError

    def SUB(self, args):
        raise NotImplementedError

    def TEQ(self, args):
        raise NotImplementedError

    def TST(self, args):
        raise NotImplementedError


class MiscInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def MRS(self, args):
        if args['encoding'] == 'A1':
            raise NotImplementedError
        if args['encoding'] == 'A1-BR':
            raise NotImplementedError
        if args['encoding'] == 'T1':
            raise NotImplementedError
        if args['encoding'] == 'T1-BR':
            raise NotImplementedError