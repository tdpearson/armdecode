class PSR(object):
    #NZCVQ  J    GE--      EAIFTM----
    #33222222222211111111110000000000
    #10987654321098765432109876543210
    def __init__(self):
        #Condition Flags - can be read or written to in any mode - see A2-49
        self.negative_flag = 0 #N, bit[31]
        self.zero_flag = 0 #Z, bit[30]
        self.carry_flag = 0 #C, bit[29]
        self.overflow_flag = 0 #V, bit[28]

        #cumulative saturation can be read or written to in any mode - see A2-49
        self.cumulative_saturation = 0 #Q, bit[27]

        self.if_then_state_bits = 0 #IT[7:0], bits[15:10, 26:25] - see A2-51 & A8-390

        self.jazelle_bit = 0 #J, bit[24]

        self.greater_than_or_equal_flags = 0 #GE[3:0], bits[19:16] - see A2-49 & A4-171

        self.endianness = 0 #E, bit[9] 0 = Little-endian, 1 = Big-endian - see A2-53 & B1-1150

        #mask bits, bits[8:6], 0 = Exception not masked, 1 = Exception masked - see B1-1151, B1-1183, C4-2089
        self.asynchronous_abort_mask = 0
        self.irq_mask = 0
        self.fiq_mask = 0

        self.thumb_bit = 0 #T, bit[5] - see A2-50, B1-1150, B1-1151

        self.mode = 0 #M[4:0], bits[4:0] - see B1-1139, B1-1144

    def __repr__(self):
        return str(self.__dict__)


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