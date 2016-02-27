__author__ = 'tdp'


class ExceptionHandling:
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def BKPT(self, args):
        """ Breakpoint """
        raise NotImplementedError

    def ERET(self, args):
        """ Exception Return """
        raise NotImplementedError

    def HVC(self, args):
        """ Hypervisor Call """
        raise NotImplementedError

    def RFE(self, args):
        """ Return From Exception """
        raise NotImplementedError

    def SMC(self, args):
        """ Secure Monitor Call """
        raise NotImplementedError

    def SRS(self, args):
        """ Store Return State """
        raise NotImplementedError

    def SVC(self, args):
        """ Supervisor Call """
        raise NotImplementedError