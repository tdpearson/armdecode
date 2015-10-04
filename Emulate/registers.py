class PSR(object):
    def __init__(self):
        self.negative_flag = 0
        self.zero_flag = 0
        self.carry_flag = 0
        self.overflow_flag = 0
        self.cumulative_saturation = 0
        self.if_then_state_bits = 0
        self.jazelle_bit = 0
        self.greater_than_or_equal_flags = 0
        self.endianness = 0
        self.asynchronous_abort_mask = 0
        self.irq_mask = 0
        self.fiq_mask = 0
        self.thumb_bit = 0
        self.mode = 0

    def __index__(self):
        return self._get_val()

    def __int__(self):
        return self._get_val()

    def __add__(self, other):
        return self._get_val() + other

    def __iadd__(self, other):
        return self._set_val(self._get_val() + other)

    def __repr__(self):
        return str(self.__dict__)

    def _get_val(self):
        val = self.negative_flag << 32 | \
              self.zero_flag << 31 | \
              self.carry_flag << 30 | \
              self.overflow_flag << 29 | \
              self.cumulative_saturation << 28 | \
              (self.if_then_state_bits & 3) << 26 | \
              self.jazelle_bit << 25 | \
              self.greater_than_or_equal_flags << 17 | \
              (self.if_then_state_bits >> 2) << 11 | \
              self.endianness << 10 | \
              self.asynchronous_abort_mask << 9 | \
              self.irq_mask << 8 | \
              self.fiq_mask << 7 | \
              self.thumb_bit << 6 | \
              self.mode
        return val

    def _set_val(self, val):
        self.negative_flag = val >> 32
        self.zero_flag = (val >> 31) & 1
        self.carry_flag = (val >> 30) & 1
        self.overflow_flag = (val >> 29) & 1
        self.cumulative_saturation = (val >> 28) & 1
        self.if_then_state_bits = ((val >> 11) & 0b111111) << 2 | (val >> 26) & 0b11
        self.jazelle_bit = (val >> 25) & 1
        self.greater_than_or_equal_flags = (val >> 17) & 0b1111
        self.endianness = (val >> 10) & 1
        self.asynchronous_abort_mask = (val >> 9) & 1
        self.irq_mask = (val >> 8) & 1
        self.fiq_mask = (val >> 7) & 1
        self.thumb_bit = (val >> 6) & 1
        self.mode = val & 0b11111
        return self


class Register(list):
    def __init__(self, *args, **kwds):
        super(self.__class__, self).__init__(*args, **kwds)
        self.extend( [0] * 16 )

    def __getattr__(self, key):
        if key.upper() in ["R0","R1","R2","R3","R4","R5","R6","R7","R8",
                           "R9", "R10","R11","R12","R13","R14","R15"]:
            return self[int(key[1:])]
        if key.upper() == "SP": return self[13]
        if key.upper() == "LR": return self[14]
        if key.upper() == "PC": return self[15]

    def __setattr__(self, key, value):
        if key.upper() in ["R0","R1","R2","R3","R4","R5","R6","R7","R8",
                           "R9", "R10","R11","R12","R13","R14","R15"]:
            self[int(key[1:])] = value
        if key.upper() == "SP": self[13] = value
        if key.upper() == "LR": self[14] = value
        if key.upper() == "PC": self[15] = value