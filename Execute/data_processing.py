__author__ = 'tdp'


class DataProcessing():
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory

    def __getitem__(self, item):
        return getattr(self, item)

    def MOV(self, args):
        if args['encoding'] == 'A1-I':
            pass
        if args['encoding'] == 'A1-R':
            pass