__author__ = 'tdp'

from Decode.utils import signed_int, sign_extend


class Branching:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def B(self, args):
        """ Branch causes a branch to a target address """
        def handle(imm, shift):
            self.registers.PC += signed_int(args[imm] << shift)
        if args['encoding'] == 'A1':
            handle('imm24', 2)
        if args['encoding'] == 'T1':
            handle('imm8', 1)
        if args['encoding'] == 'T2':
            handle('imm11', 1)
        if args['encoding'] == 'T3':
            delta = signed_int((args['S'] << 19 | args['J2'] << 18 | args['J1'] << 17 | args['imm6'] << 11 | args['imm11']) << 1)
            self.registers.PC += delta
        if args['encoding'] == 'T4':
            I1 = 1 ^ (args['J1'] ^ args['S'])
            I2 = 1 ^ (args['J2'] ^ args['S'])
            delta = signed_int((args['S'] << 23 | I1 << 22 | I2 << 21 | args['imm10'] << 11 | args['imm11']) << 1)
            self.registers.PC += delta

    def CBZ(self, args):
        """ Compare and Branch on Zero """
        if args['Rn'] == 0:
            delta = signed_int((args['i'] << 5 | args['imm5']) << 1)
            self.registers.PC += delta

    def CBNZ(self, args):
        """ Compare and Branch on Nonzero """
        if args['Rn'] != 0:
            delta = signed_int((args['i'] << 5 | args['imm5']) << 1)
            self.registers.PC += delta

    def BL(self, args):
        """ Branch with Link / Branch with Link and Exchange Instructions Sets"""
        if args['encoding'] == 'A1-I':
            self.registers.LR = self.registers.PC - 4
            self.registers.PC += signed_int(args['imm24'] << 2)
        if args['encoding'] == 'A2-I':  # BLX
            self.registers.LR = self.registers.PC - 4
            self.registers.PC += signed_int((args['imm24'] << 1 | args['H']) << 1)
            self.process_mode.CPSR.thumb_bit = 1
        if args['encoding'] == 'T1-I':
            self.registers.LR = self.registers.PC - 2
            I1 = 1 ^ (args['J1'] ^ args['S'])
            I2 = 1 ^ (args['J2'] ^ args['S'])
            delta = signed_int((args['S'] << 23 | I1 << 22 | I2 << 21 | args['imm10'] << 11 | args['imm11']) << 1)
            self.registers.PC += delta
        if args['encoding'] == 'T2-I':  # BLX
            self.registers.LR = self.registers.PC - 2  # TODO: Confirm
            I1 = 1 ^ (args['J1'] ^ args['S'])
            I2 = 1 ^ (args['J2'] ^ args['S'])
            delta = signed_int((args['S'] << 22 | I1 << 21 | I2 << 20 | args['imm10H'] << 10 | args['imm10L']) << 2)
            self.registers.PC += delta
            self.process_mode.CPSR.thumb_bit = 0

    def BX(self, args):
        """ Branch and Exchange """
        raise NotImplementedError

    def BXJ(self, args):
        """ Branch and Exchange Jazelle """
        raise NotImplementedError

    def TBB(self, args):
        """ Table Branch Byte """
        raise NotImplementedError

    def TBH(self, args):
        """Table Branch Halfword """
        raise NotImplementedError
