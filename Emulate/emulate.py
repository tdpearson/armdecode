from copy import copy

from .registers import PSR, Register
from .memory import Memory
from Execute.execute import Execute
from Decode.arm_template import arm
from Decode.t16_template import t16
#from Decode.t32_template import t32
from Decode.utils import is32bitThumb, unpack16, unpack32, test_arm_condition


class ModeChangeException(Exception):
    pass


class Emulate(object):
    def __init__(self):
        self.memory = Memory()
        self.registers = Register()
        self.process_mode = ProcessMode()
        self.execute = Execute(self.registers,
                               self.process_mode,
                               self.memory)

    def _decode(self, action=None):
        # TODO: Add condition flag to decode
        if (self.process_mode.CPSR.thumb_bit == 1) & (self.process_mode.CPSR.jazelle_bit == 0):
            if is32bitThumb(self.memory.read_blob(2, self.registers.PC)):
                instruction = unpack32(self.memory.read_blob(4, self.registers.PC))
                self.registers.PC += 4
                decode = t32(instruction)
            else:
                instruction = unpack16(self.memory.read_blob(2, self.registers.PC))
                self.registers.PC += 2
                decode = t16(instruction)
        if (self.process_mode.CPSR.thumb_bit == 0) & (self.process_mode.CPSR.jazelle_bit == 0):
            instruction = unpack32(self.memory.read_blob(4, self.registers.PC))
            self.registers.PC += 4
            if test_arm_condition(instruction, self.process_mode.CPSR):
                decode = arm(instruction)
            else:
                decode = None
        if (self.process_mode.CPSR.thumb_bit == 0) & (self.process_mode.CPSR.jazelle_bit == 1):
            raise NotImplementedError('Jazelle')
        if (self.process_mode.CPSR.thumb_bit == 1) & (self.process_mode.CPSR.jazelle_bit == 1):
            instruction = unpack16(self.memory.read_blob(2, self.registers.PC))
            self.registers.PC += 2
            raise NotImplementedError('Thumb EE')
        if decode:
            action(decode)

    def step(self, action, count=1):
        for _ in range(count):
            self._decode(action)

    def loop(self, action):
        while True:
            self._decode(action)

    def reset(self):
        self.__init__()


process_mode_lookup = {'USR': {'mode_bits': 0b10000,
                               'allow_change_mode': False,
                               'privilege_level': 0,
                               'banked_registers': [8, 6]},  # [starting register, count] to get R8 through LR
                       'FIQ': {'mode_bits': 0b10001,
                               'allow_change_mode': True,
                               'privilege_level': 1,
                               'banked_registers': [8, 6]},  # [starting register, count] to get R8 through LR
                       'IRQ': {'mode_bits': 0b10010,
                               'allow_change_mode': True,
                               'privilege_level': 1,
                               'banked_registers': [13, 2]},  # [starting register, count] to get SP and LR
                       'SVC': {'mode_bits': 0b10011,
                               'allow_change_mode': True,
                               'privilege_level': 1,
                               'banked_registers': [13, 2]},  # [starting register, count] to get SP and LR
                       'MON': {'mode_bits': 0b10110,
                               'allow_change_mode': True,
                               'privilege_level': 1,
                               'banked_registers': [13, 2]},  # [starting register, count] to get SP and LR
                       'ABT': {'mode_bits': 0b10111,
                               'allow_change_mode': True,
                               'privilege_level': 1,
                               'banked_registers': [13, 2]},  # [starting register, count] to get SP and LR
                       'HYP': {'mode_bits': 0b11010,
                               'allow_change_mode': True,
                               'privilege_level': 2,
                               'banked_registers': [13, 2]},  # [starting register, count] to get SP and LR - technically ELR_hyp
                       'UND': {'mode_bits': 0b11011,
                               'allow_change_mode': True,
                               'privilege_level': 1,
                               'banked_registers': [13, 2]},  # [starting register, count] to get SP and LR
                       'SYS': {'mode_bits': 0b11111,
                               'allow_change_mode': True,
                               'privilege_level': 1,
                               'banked_registers': [8, 6]},  # [starting register, count] to get R8 through LR
                       }


class ProcessMode(object):
    class _mode(object):
        def __init__(self):
            self.SPSR = PSR()

        # FIXME: Is this needed?
        def __repr__(self):
            return self.name

    def __init__(self):
        self.CPSR = PSR()
        self.registers = Register()

        for mode_name in process_mode_lookup.keys():
            self.__dict__[mode_name] = self._mode()
            self.__dict__[mode_name].mode_bits = process_mode_lookup[mode_name]['mode_bits']
            self.__dict__[mode_name].name = mode_name
            self.__dict__[mode_name].allow_change_mode = process_mode_lookup[mode_name]['allow_change_mode']
            self.__dict__[mode_name].privilege_level = process_mode_lookup[mode_name]['privilege_level']
            # FIXME: initializing banked registers as zeros - should they be initialized as 0xDEADDEAD?
            self.__dict__[mode_name].banked_registers = [0] * process_mode_lookup[mode_name]['banked_registers'][1]

        # FIXME: What is this being used for? If it is not needed, get rid of it!
        self.mode_lookup = {}
        for item in self.__dict__.values():
            try:
                self.mode_lookup[item.mode_bits] = item
            except (AttributeError, KeyError):
                pass

        # initiate into SVC mode
        self.current_mode = self.SVC
        self.CPSR.mode = self.current_mode.mode_bits
        self.CPSR.zero_flag = 1

    def change_mode(self, mode):
        if self.current_mode.allow_change_mode:
            # Save CPSR to current SPSR, and bank current registers
            self.current_mode.SPSR = copy(self.CPSR)
            reg_offset, reg_count = process_mode_lookup[self.current_mode.name]['banked_registers']
            self.current_mode.banked_registers = self.registers[reg_offset:reg_offset + reg_count]
            # Change mode and load corresponding values
            self.current_mode = mode
            self.CPSR = copy(self.current_mode.SPSR)
            self.CPSR.mode = self.current_mode.mode_bits
            reg_offset, reg_count = process_mode_lookup[self.current_mode.name]['banked_registers']
            self.registers[reg_offset:reg_offset + reg_count] = self.current_mode.banked_registers
        else:
            raise ModeChangeException

    def __repr__(self):
        return "<Current Mode: %s>" % self.current_mode.name
