__author__ = 'tdp'

from Decode.utils import getbit, ror as _decode_ror


class NotShifted(Exception):
    pass


def lsl(args, psr, registers):
    return (val << count) & ((1 << size) - 1)


def lsr(args, psr, registers):
    return val >> count


def asr(args, psr, registers):
    '''
    :param args: Instruction Arguments
    :param psr: Program Status Register
    :param registers:
    :return: (Shifted value, [carry value])
    '''
    val = args['Rm']  # value to shift
    count = args['imm5']  # number of shifts
    if getbit(val, 31):
        # TODO: calculate carry value and add to returned
        return (((1 << count) - 1) << (31 - count) | val >> count, None)
    return (val >> count)


def ror(args, psr, registers):
    return ((val & ((1 << count) - 1)) << (size - count)) | (val >> count)


def rrx(args, psr, registers):
    print('rrx')


def _ror_or_rrx(imm5):
    if imm5 == 0:
        return rrx
    return ror


def decode_immediate_shift(args, psr, registers):
    if args['imm5'] == 0 and args['type'] != 3:
        raise NotShifted

    return {0: lsl,
            1: lsr,
            2: asr,
            3: _ror_or_rrx(args['imm5']),
            }[args['type']](args, psr, registers)


def decode_register_shift(args, psr, registers):
    return {0: lsl,
            1: lsr,
            2: asr,
            3: ror,
            }[args['type']](args, psr, registers)


def arm_expand_immediate(imm12, carry_in, expand_size=32):
    # TODO - confirm / correct carry handling
    unrotated_value = imm12 & 255  # get lower 8bits
    rotate_amount = 2 * (imm12 >> 8)
    if rotate_amount:
        return _decode_ror(unrotated_value, rotate_amount, expand_size)
    return unrotated_value, carry_in


def memory_access_read(memory, bytedata, position, size, aligned=True, unpriv=False):
    # TODO - write code
    pass


def memory_access_write(memory, bytedata, position, aligned=True, unpriv=False):
    # TODO - complete writing out
    memory.write_blob(bytedata, position)

