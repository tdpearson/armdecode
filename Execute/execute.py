from functools import lru_cache
from Execute.branching import Branching


class Execute(object):
    def __init__(self, registers, process_mode, memory):
        self.registers = registers
        self.process_mode = process_mode
        self.memory = memory
        self.branch = Branching(registers, process_mode, memory)

    def __call__(self, args):
        @lru_cache()
        def lookup(instr):
            if instr in ['B', 'BL']: return self.branch[instr]
            return print
        lookup(args['instr'])(args)