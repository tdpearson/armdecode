__author__ = 'tdp'

from Execute.utils import memory_access_read, memory_access_write


class LoadStore:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def LDR(self, args):
        """ Load Register """
        raise NotImplementedError

    def LDRB(self, args):
        """ Load RegisterByte """
        raise NotImplementedError

    def LDRBT(self, args):
        """ Load Register Byte Unprivileged """
        raise NotImplementedError

    def LDRD(self, args):
        """ Load Register Dual """
        raise NotImplementedError

    def LDREX(self, args):
        """ Load Register Exclusive """
        raise NotImplementedError

    def LDREXB(self, args):
        """ Load Register Exclusive Byte """
        raise NotImplementedError

    def LDREXD(self, args):
        """ Load Register Exclusive Doubleword """
        raise NotImplementedError

    def LDREXH(self, args):
        """ Load Register Exclusive Halfword """
        raise NotImplementedError

    def LDRH(self, args):
        """ Load Register Halfword """
        raise NotImplementedError

    def LDRHT(self, args):
        """ Load Register Halfword Unprivileged """
        raise NotImplementedError

    def LDRSB(self, args):
        """ Load Register Signed Byte """
        raise NotImplementedError

    def LDRSBT(self, args):
        """ Load Register Signed Byte Unprivileged """
        raise NotImplementedError

    def LDRSH(self, args):
        """ Load Register Signed Halfword """
        raise NotImplementedError

    def LDRSHT(self, args):
        """ Load Register Signed Halfword Unprivileged """
        raise NotImplementedError

    def LDRT(self, args):
        """ Load Register Unprivileged """
        raise NotImplementedError

    def STR(self, args):
        """ Store Register """
        if args['encoding'] == 'A1-I':
            if args['U']:  # Add
                offset_address = self.registers[args['Rn']] + args['imm12']
            else:  # Subtract
                offset_address = self.registers[args['Rn']] - args['imm12']
            if args['P']:  # Index
                memory_access_write(self.memory, bytes(self.registers[args['Rt']]), offset_address, 32)
            else:
                memory_access_write(self.memory, bytes(self.registers[args['Rt']]), args['imm12'], 32)
            if args['P'] == 0 | args['W'] == 1:  # write back
                self.registers[args['Rn']] = offset_address
        if args['encoding'] == 'A1-R':
            raise NotImplementedError
        if args['encoding'] == 'T1-I':
            raise NotImplementedError
        if args['encoding'] == 'T2-I':
            raise NotImplementedError
        if args['encoding'] == 'T3-I':
            raise NotImplementedError
        if args['encoding'] == 'T4-I':
            raise NotImplementedError
        if args['encoding'] == 'T1-R':
            raise NotImplementedError
        if args['encoding'] == 'T2-R':
            raise NotImplementedError

    def STRB(self, args):
        """ Store Register Byte """
        raise NotImplementedError

    def STRBT(self, args):
        """ Store Register Byte Unprivileged """
        raise NotImplementedError

    def STRD(self, args):
        """ Store Register Dual """
        raise NotImplementedError

    def STREX(self, args):
        """ Store Register Exclusive """
        raise NotImplementedError

    def STREXB(self, args):
        """ Store Register Exclusive Byte """
        raise NotImplementedError

    def STREXD(self, args):
        """ Store Register Exclusive Doubleword """
        raise NotImplementedError

    def STREXH(self, args):
        """ Store Register Exclusive Halfword """
        raise NotImplementedError

    def STRH(self, args):
        """ Store Register Halfword """
        raise NotImplementedError

    def STRHT(self, args):
        """ Store Register Halfword Unprivileged """
        raise NotImplementedError

    def STRT(self, args):
        """ Store Register Unprivileged """
        raise NotImplementedError


class LoadStoreMultiple:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def LDM(self, args):
        """ Load Multiple / Increment After / Full Descending """
        raise NotImplementedError

    def LDMDA(self, args):
        """ Load Multiple Decrement After / Full Ascending """
        raise NotImplementedError

    def LDMDB(self, args):
        """ Load Multiple Decrement Before / Empty Ascending """
        raise NotImplementedError

    def LDMIB(self, args):
        """ Load Multiple Increment Before / Empty Descending """
        raise NotImplementedError

    def POP(self, args):
        """ Pop Multiple Registers """
        raise NotImplementedError

    def PUSH(self, args):
        """ Push Multiple Registers """
        raise NotImplementedError

    def STM(self, args):
        """ Store Multiple / Increment After / Empty Ascending """
        raise NotImplementedError

    def STMDA(self, args):
        """ Store Multiple Decrement After / Empty Descending """
        raise NotImplementedError

    def STMDB(self, args):
        """ Store Multiple Decrement Before / Full Descending """
        raise NotImplementedError

    def STMIB(self, args):
        """ Store Multiple Increment Before / Full Ascending """
        raise NotImplementedError
