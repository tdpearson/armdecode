__author__ = 'tdp'
from Decode.utils import isZeroBit
from Execute.utils import *
import operator as op

CPSR_Mask = 0b11111000111111110000001111011111
APSR_Mask = 0b11111000000111100000000000000000


class StandardInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def _imediate_template(self, args, operator):
        pass

    def _register_template(self, args, operator):
        if args['encoding'] == 'A1-R':
            '''S, Rn, Rd, imm5, type, Rm'''
            try:
                result = operator(self.registers[args['Rn']], decode_immediate_shift(args, self.process_mode.CPSR, self.registers))
                carry = getbit(self.registers[args['Rn']], args('imm5'))
            except NotShifted:
                result = operator(self.registers[args['Rn']], self.registers[args['Rm']])
                carry = 0
            if args['S']:
                self.process_mode.CPSR.negative_flag = getbit(result, 31)
                self.process_mode.CPSR.zero_flag = isZeroBit(result)
                self.process_mode.CPSR.carry_flag = carry
            self.registers[args['Rd']] = result

    def _register_shifted_template(self, args, operator):
        pass

    def ADC(self, args):
        """ Add with Carry """
        raise NotImplementedError

    def ADD(self, args):
        """ Add """
        raise NotImplementedError

    def ADR(self, args):
        """Add an immediate value with PC value """
        raise NotImplementedError

    def AND(self, args):
        """ AND """
        if args['encoding'] == 'A1-R':
            '''S, Rn, Rd, imm5, type, Rm'''
            #try:
            #    result = self.registers[args['Rn']] & decode_immediate_shift(args, self.process_mode.CPSR, self.registers)
            #    carry = getbit(self.registers[args['Rn']], args('imm5'))
            #except NotShifted:
            #    result = self.registers[args['Rn']] & self.registers[args['Rm']]
            #    carry = 0
            #if args['S']:
            #    self.process_mode.CPSR.negative_flag = getbit(result, 31)
            #    self.process_mode.CPSR.zero_flag = isZeroBit(result)
            #    self.process_mode.CPSR.carry_flag = carry
            #self.registers[args['Rd']] = result
            self._register_template(args, op.and_)
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

    def BIC(self, args):
        """ Bitwise Bit Clear """
        raise NotImplementedError

    def CMN(self, args):
        """ Compare Negative """
        raise NotImplementedError

    def CMP(self, args):
        """ Compare """
        raise NotImplementedError

    def EOR(self, args):
        """ Exclusive OR """
        if args['encoding'] == 'A1-I':
            raise NotImplementedError
        if args['encoding'] == 'A1-R':
            self._register_template(args, op.xor)
        if args['encoding'] == 'A1-RSR':
            raise NotImplementedError
        if args['encoding'] == 'T1-I':
            raise NotImplementedError
        if args['encoding'] == 'T1-R':
            raise NotImplementedError
        if args['encoding'] == 'T2-R':
            raise NotImplementedError

    def MOV(self, args):
        """ Move """
        if args['encoding'] == 'A1-I':
            '''S, Rd, imm12'''
            raise NotImplementedError
        if args['encoding'] == 'A1-R':
            Rm = self.registers[args['Rm']]
            self.registers[args['Rd']] = Rm
            self.process_mode.CPSR.negative_flag = Rm >> 31
            self.process_mode.CPSR.zero_flag = isZeroBit(Rm)

    def MVN(self, args):
        """ Bitwise Not """
        raise NotImplementedError

    def ORN(self, args):
        """ Bitwise OR NOT """
        raise NotImplementedError

    def ORR(self, args):
        """ Bitwise OR """
        raise NotImplementedError

    def RSB(self, args):
        """ Reverse Subtract """
        raise NotImplementedError

    def RSC(self, args):
        """ Reverse Subtract with Carry """
        raise NotImplementedError

    def SBC(self, args):
        """ Subtract with Carry """
        raise NotImplementedError

    def SUB(self, args):
        """ Subtract """
        raise NotImplementedError

    def TEQ(self, args):
        """ Test Equivalence """
        raise NotImplementedError

    def TST(self, args):
        """ Test """
        if args['encoding'] == 'A1-I':
            # Rn, imm12
            imm32, carry = arm_expand_immediate(args['imm12'], self.process_mode.CPSR.carry_flag)
            result = args['Rn'] & imm32
            self.process_mode.CPSR.negative_flag = getbit(result, 31)
            self.process_mode.CPSR.zero_flag = isZeroBit(result)
            self.process_mode.CPSR.carry_flag = carry
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


class ShiftInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def ASR(self, args):
        """ Arithmetic Shift Right """
        raise NotImplementedError

    def LSL(self, args):
        """ Logical Shift Left """
        raise NotImplementedError

    def LSR(self, args):
        """ Logical Shift Right """
        raise NotImplementedError

    def ROR(self, args):
        """ Rotate Right """
        raise NotImplementedError

    def RRX(self, args):
        """ Rotate Right with Extend """
        raise NotImplementedError


class MultiplyInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)


class SaturatingInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)


class SaturatingAddSubInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)


class PackingUnpackingInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)


class ParallelAddSubInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)


class DivideInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)


class MiscInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)


class MiscInstructions:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory
        self.privilege_level = process_mode.current_mode.privilege_level

    def __getitem__(self, item):
        return getattr(self, item)

    def MRS(self, args):
        """ Move to Register from Special register """
        if args['encoding'] == 'A1':
            if self.privilege_level > 0:  # Execute as system level
                if args['R'] == 1:  # read SPSR
                    self.registers[args['Rd']] = int(self.process_mode.current_mode.SPSR)
                if args['R'] == 0:
                    # CPSR is read with execution state bits other than E masked out.
                    self.registers[args['Rd']] = int(self.process_mode.CPSR) & CPSR_Mask
            else:  # Execute as application level
                self.registers[args['Rd']] = int(self.process_mode.CPSR) & APSR_Mask
        if args['encoding'] == 'A1-BR':
            raise NotImplementedError
        if args['encoding'] == 'T1':
            raise NotImplementedError
        if args['encoding'] == 'T1-BR':
            raise NotImplementedError