from copy import copy

from Emulate.registers import PSR, Register
from Emulate.memory import Memory
from Execute.execute import Execute
from Decode.arm_template import arm

#from Decode.t16_template import t16
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
        #TODO: Add condition flag to decode
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
                decode = arm(0)
        if (self.process_mode.CPSR.thumb_bit == 0) & (self.process_mode.CPSR.jazelle_bit == 1):
            raise NotImplementedError('Jazelle')
        if (self.process_mode.CPSR.thumb_bit == 1) & (self.process_mode.CPSR.jazelle_bit == 1):
            instruction = unpack16(self.memory.read_blob(2, self.registers.PC))
            self.registers.PC += 2
            raise NotImplementedError('Thumb EE')
        try:
            action(decode)
        except TypeError:
            pass

    def step(self, count=1, action=None):
        if not action:
            raise Exception('Must supply an action')
        for _ in range(count):
            self._decode(action)

    def loop(self, action=None):
        if not action:
            raise Exception('Must supply an action')
        while True:
            self._decode(action)

    def reset(self):
        self.__init__()


process_modes = {'USR': {'mode_bits': 0b10000,
                         'allow_change_mode': False,
                         'privilege_level': 0},
                 'FIQ': {'mode_bits': 0b10001,
                         'allow_change_mode': True,
                         'privilege_level': 1},
                 'IRQ': {'mode_bits': 0b10010,
                         'allow_change_mode': True,
                         'privilege_level': 1},
                 'SVC': {'mode_bits': 0b10011,
                         'allow_change_mode': True,
                         'privilege_level': 1},
                 'MON': {'mode_bits': 0b10110,
                         'allow_change_mode': True,
                         'privilege_level': 1},
                 'ABT': {'mode_bits': 0b10111,
                         'allow_change_mode': True,
                         'privilege_level': 1},
                 'HYP': {'mode_bits': 0b11010,
                         'allow_change_mode': True,
                         'privilege_level': 2},
                 'UND': {'mode_bits': 0b11011,
                         'allow_change_mode': True,
                         'privilege_level': 1},
                 'SYS': {'mode_bits': 0b11111,
                         'allow_change_mode': True,
                         'privilege_level': 1},
                 }


class ProcessMode(object):
    class _mode(object):
        def __init__(self):
            self.SPSR = PSR()

        def __repr__(self):
            return self.name

    def __init__(self):
        self.CPSR = PSR()

        for mode_name in process_modes.keys():
            self.__dict__[mode_name] = self._mode()
            self.__dict__[mode_name].mode_bits = process_modes[mode_name]['mode_bits']
            self.__dict__[mode_name].name = mode_name
            self.__dict__[mode_name].allow_change_mode = process_modes[mode_name]['allow_change_mode']
            self.__dict__[mode_name].privilege_level = process_modes[mode_name]['privilege_level']

        self.mode_lookup = {}
        for item in self.__dict__.values():
            if hasattr(item, 'mode_bits'):
                self.mode_lookup[item.mode_bits] = item

        #initiate into SVC mode
        self.current_mode = self.SVC
        self.CPSR.mode = self.current_mode.mode_bits
        self.CPSR.zero_flag = 1

    def change_mode(self, mode):
        if self.current_mode.allow_change_mode:
            temp_mode = copy(self.CPSR)
            self.CPSR = copy(self.current_mode.SPSR)
            self.current_mode = mode
            self.CPSR.mode = self.current_mode.mode_bits
            self.current_mode.SPSR = copy(temp_mode)
        else:
            raise ModeChangeException