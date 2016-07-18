import struct


def is32bitThumb(val):
    try:
        #if type(val) != int
        val = struct.unpack("H", val)[0]
    except TypeError:
        pass
    if val >> 11 in [0b11101, 0b11110, 0b11111]:
        return True
    return False


def unpack32(val):
    try:
        return struct.unpack("I", val)[0]
    except TypeError:
        return val


def unpack16(val):
    try:
        return struct.unpack("H", val)[0]
    except TypeError:
        return val


def arm_condition(val):
    cond = {0b0000: 'EQ',
            0b0001: 'NE',
            0b0010: 'CS',
            0b0011: 'CC',
            0b0100: 'MI',
            0b0101: 'PL',
            0b0110: 'VS',
            0b0111: 'VC',
            0b1000: 'HI',
            0b1001: 'LS',
            0b1010: 'GE',
            0b1011: 'LT',
            0b1100: 'GT',
            0b1101: 'LE',
            0b1110: 'AL'}
    return cond[val >> 28]


def test_arm_condition(val, cpsr):
    """
    Returns True or False depending on if the instruction should be executed
    based on instruction condition and CPSR flags.

    val = word aligned ARM instruction
    cpsr = current program status register
    """
    cond = {0b0000: cpsr.zero_flag == 1,  # Z set
            0b0001: cpsr.zero_flag == 0,  # Z clear
            0b0010: cpsr.carry_flag == 1,  # C set
            0b0011: cpsr.carry_flag == 0,  # C clear
            0b0100: cpsr.negative_flag == 1,  # N set
            0b0101: cpsr.negative_flag == 0,  # N clear
            0b0110: cpsr.overflow_flag == 1,  # V set
            0b0111: cpsr.overflow_flag == 0,  # V clear
            0b1000: cpsr.carry_flag == 1 and cpsr.zero_flag == 0,  # C set Z clear
            0b1001: cpsr.carry_flag == 0 and cpsr.zero_flag == 1,  # C clear Z set
            0b1010: cpsr.negative_flag == cpsr.overflow_flag,  # N and V the same
            0b1011: cpsr.negative_flag != cpsr.overflow_flag,  # N and V differ
            0b1100: cpsr.zero_flag == 0 and (cpsr.negative_flag == cpsr.overflow_flag),  # Z clear, N and V the same
            0b1101: cpsr.zero_flag == 1 and (cpsr.negative_flag != cpsr.overflow_flag),  # Z set, N and V differ
            0b1110: True,  # Any
            0b1111: False,  # Not Valid
            }
    return cond[val >> 28]


def binprint(val, bit_size):
    return "0b%s" % bin(val)[2:].zfill(bit_size)


def hexprint(val, bit_size):
    return "0x%s" % hex(val)[2:].zfill(bit_size / 4).replace("L", "")


def register_list(val, size):
    return [register for register, x in enumerate([val >> pos & 0b1 for pos in range(size)]) if x == 1]


def togglebit(val, pos):
    return val ^ 1 << pos


def getbytes(val, pos, mask):
    return val >> pos & mask


def getword(val, pos):
    return val >> pos & 0b1111


def gethword(val, pos):
    return val >> pos & 0b11


def getbit(val, pos):
    return val >> pos & 1


def setbit(val, pos):
    return val | 1 << pos


def clearbit(val, pos):
    return val & ~(1 << pos)


def ror(val, count=1, size=32):
    return ((val & ((1 << count) - 1)) << (size - count)) | (val >> count)


def sign_extend(val, size=24, align=30):
    return (((1 << (align - size)) - 1) << size) | val


def signed_int(val):
    int_val = val & 0xffffffff
    if int_val > 0x7fffffff:
        return ~int_val ^ 0xffffffff
    return int_val


def signed_short(val):
    short_val = val & 0xffff
    if short_val > 0x7fff:
        return ~short_val ^ 0xffff
    return short_val


def signed_char(val):
    char_val = val & 0xff
    if char_val > 0x7f:
        return ~char_val ^ 0xff
    return char_val


def isZero(val):
    return val == 0


def isZeroBit(val):
    if val == 0:
        return 1
    return 0


def isOnes(val, size):
    return val == (1 << size) - 1


def isOnesBit(val, size):
    if val == (1 << size) - 1:
        return 1
    return 0

