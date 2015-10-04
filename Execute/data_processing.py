__author__ = 'tdp'
from Decode.utils import isZeroBit
from Execute.utils import *

CPSR_Mask = 0b11111000111111110000001111011111
APSR_Mask = 0b11111000000111100000000000000000

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
            try:
                result = self.registers[args['Rn']] & decode_immediate_shift(args, self.process_mode.CPSR, self.registers)
                carry = getbit(self.registers[args['Rn']], args('imm5'))
            except NotShifted:
                result = self.registers[args['Rn']] & self.registers[args['Rm']]
                carry = 0
            if args['S']:
                self.process_mode.CPSR.negative_flag = getbit(result, 31)
                self.process_mode.CPSR.zero_flag = isZeroBit(result)
                self.process_mode.CPSR.carry_flag = carry
            self.registers[args['Rd']] = result
            sticky = ""
            if args['S']: sticky = " and update flags"
            print("and R%s to R%s store in R%s%s" % (args['Rn'], args['Rm'], args['Rd'], sticky))
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
        if args['encoding'] == 'A1-I':
            # Rn, imm12
            imm32, carry = arm_expand_immediate(args['imm12'], self.process_mode.CPSR.carry_flag)
            result = args['Rn'] & imm32
            self.process_mode.CPSR.negative_flag = getbit(result, 31)
            self.process_mode.CPSR.zero_flag = isZeroBit(result)
            self.process_mode.CPSR.carry_flag = carry
            print("test R%s against %s" % (args['Rn'], imm32))
        if args['encoding'] == 'T1-I':
            raise NotImplementedError
        if args['encoding'] == 'A1-R':
            raise NotImplementedError
        if args['encoding'] == 'T1-R':
            raise NotImplementedError
        if args['encoding'] == 'T2-R':
            raise NotImplementedError
        if args['encoding'] == 'A1-RSR':
            raise NotImplementedError

class MiscInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory
        self.privilege_level = process_mode.current_mode.privilege_level

    def __getitem__(self, item):
        return getattr(self, item)

    def MRS(self, args):
        if args['encoding'] == 'A1':
            if self.privilege_level > 0:  # Execute as system level
                if args['R'] == 1:  # read SPSR
                    self.registers[args['Rd']] = int(self.process_mode.current_mode.SPSR)
                    print("copied SPSR to R%s" % args['Rd'])
                if args['R'] == 0:
                    # CPSR is read with execution state bits other than E masked out.
                    self.registers[args['Rd']] = int(self.process_mode.CPSR) & CPSR_Mask
                    print("copied CPSR to R%s" % args['Rd'])
            else:  # Execute as application level
                self.registers[args['Rd']] = int(self.process_mode.CPSR) & APSR_Mask
                print("copied APSR to R%s" % args['Rd'])
        if args['encoding'] == 'A1-BR':
            raise NotImplementedError
        if args['encoding'] == 'T1':
            raise NotImplementedError
        if args['encoding'] == 'T1-BR':
            raise NotImplementedError