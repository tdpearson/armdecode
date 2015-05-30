__author__ = 'tdp'

from Decode.utils import lsl, lsr, asr, ror, rrx


def shift_c(val, SRType, amount, carry_in):
    if amount == 0:
        return val, carry_in
    else:
        if SRType == "LSL":
            return lsl(val, amount, carry=True)
        if SRType == "LSR":
            return lsr(val, amount, carry=True)
        if SRType == "ASR":
            return asr(val, amount, carry=True)
        if SRType == "ROR":
            return ror(val, amount, carry=True)
        if SRType == "RRX":
            return rrx(val, amount, carry=True)