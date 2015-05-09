from Decode.decoder_tools import instruction_decoder
from Decode.utils import ror

default_encoding = "A1"


@instruction_decoder
class arm():
    """
    cond:!1111
        op1:00x =  _data_processing_and_misc                           #a5-196
        op1:010 =  _load_store_word_and_unsigned_byte                  #a5-208
        op1:011
            op:0 = _load_store_word_and_unsigned_byte                  #a5-208
            op:1 = _media_instructions                                 #a5-209
        op1:10x =  _branch_branch_with_link_and_block_data_transfer    #a5-214
        op1:11x =  _coprocessor_instructions_and_supervisor_call       #a5-215
    cond:1111 =    _unconditional_instructions                         #a5-216
    """
    positions = {'cond': [28, 4],
                 'op':   [4,  1],
                 'op1':  [25, 3]}



@instruction_decoder
class _data_processing_and_misc():
    """
    op:0
        op1:!10xx0
            op2:xxx0 = _data_processing_register                      #a5-197
            op2:0xx1 = _data_processing_register_shifted              #a5-198
        op1:10xx0
            op2:0xxx = _misc_instructions                             #a5-207
            op2:1xx0 = _halfword_multiply_and_multiply_accumulate     #a5-203
        op1:0xxxx
            op2:1001 = _multiply_and_multiply_accumulate              #a5-202
        op1:1xxxx
            op2:1001 = _synchronization_primitives                    #a5-205
        op1:!0xx1x
            op2:1011 = _extra_load_store_instructions                 #a5-203
            op2:11x1 = _extra_load_store_instructions                 #a5-203
        op1:0xx1x
            op2:1011 = _extra_load_store_instructions_unprivileged    #a5-204
            op2:11x1 = _extra_load_store_instructions                 #a5-203
    op:1
        op1:!10xx0 =   _data_processing_immediate                     #a5-199
        op1:10000  =   MOV (S, Rd, imm12)                        A1-I #a8-484 if RD = 1111 and S = 1 then SUBS PC, LR
        op1:10100  =   MOVT (imm4, Rd, imm12)                    A1   #a8-491
        op1:10x10  =   _msr_and_hints_immediate                       #a5-206
    """
    positions = {'op':  [25, 1],
                 'op1': [20, 5],
                 'op2': [4,  4]}
    ops = {'Rd':    (12, 4),
           'imm12': (0, 12),
           'S':     (20, 1),
           'imm4':  (16, 4)}


@instruction_decoder
class _data_processing_register():
    """
    op:0000x = AND (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-326
    op:0001x = EOR (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-384
    op:0010x = SUB (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-712
    op:0011x = RSB (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-576
    op:0100x = ADD (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-312
    op:0101x = ADC (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-302
    op:0110x = SBC (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-594
    op:0111x = RSC (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-582
    op:10xx0 = _data_processing_and_misc                #a5-196
    op:10001 = TST (Rn, imm5, type, Rm)            A1-R #a8-746
    op:10011 = TEQ (Rn, imm5, type, Rm)            A1-R #a8-740
    op:10101 = CMP (Rn, imm5, type, Rm)            A1-R #a8-372
    op:10111 = CMN (Rn, imm5, type, Rm)            A1-R #a8-366
    op:1100x = ORR (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-518
    op:1101x
        op2:00
            imm5:00000  = MOV (S, Rd, Rm)          A1-R #a8-488
            imm5:!00000 = LSL (S, Rd, imm5, Rm)    A1-I #a8-468
        op2:01 = LSR (S, Rd, imm5, Rm)             A1-I #a8-472
        op2:10 = ASR (S, Rd, imm5, Rm)             A1-I #a8-330
        op2:11
            imm5:00000  = RRX (S, Rd, Rm)          A1   #a8-572
            imm5:!00000 = ROR (S, Rd, imm5, Rm)    A1-I #a8-568
    op:1110x = BIC (S, Rn, Rd, imm5, type, Rm)     A1-R #a8-342
    op:1111x = MVN (S, Rd, imm5, type, Rm)         A1-R #a8-506
    """
    positions = {'op':   [20, 5],
                 'imm5': [7,  5],
                 'op2':  [5,  2]}
    ops = {'Rd':   (12, 4),
           'S':    (20, 1),
           'type': (5,  2),
           'imm5': (7,  5),
           'Rn':   (16, 4),
           'Rm':   (0,  4)}


@instruction_decoder
class _data_processing_register_shifted():
    """
    op1:0000x =  AND (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-328
    op1:0001x =  EOR (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-386
    op1:0010x =  SUB (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-714
    op1:0011x =  RSB (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-578
    op1:0100x =  ADD (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-314
    op1:0101x =  ADC (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-304
    op1:0110x =  SBC (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-596
    op1:0111x =  RSC (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-584
    op1:10xx0 =  _data_processing_and_misc               #a5-196
    op1:10001 =  TST (Rn, Rs, type, Rm)           A1-RSR #a8-748
    op1:10011 =  TEQ (Rn, Rs, type, Rm)           A1-RSR #a8-742
    op1:10101 =  CMP (Rn, Rs, type, Rm)           A1-RSR #a8-374
    op1:10111 =  CMN (Rn, Rs, type, Rm)           A1-RSR #a8-368
    op1:1100x =  ORR (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-520
    op1:1101x
        op2:00 = LSL (S, Rd, Rm, Rn)              A1-R   #a8-470
        op2:01 = LSR (S, Rd, Rm, Rn)              A1-R   #a8-474
        op2:10 = ASR (S, Rd, Rm, Rn)              A1-R   #a8-332
        op2:11 = ROR (S, Rd, Rm, Rn)              A1-R   #a8-570
    op1:1110x =  BIC (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-344
    op1:1111x =  MVN (S, Rn, Rd, Rs, type, Rm)    A1-RSR #a8-508
    """
    positions = {'op1': [20, 5],
                 'op2': [5,  2]}
    ops = {'Rd':   (12, 4),
           'S':    (20, 1),
           'Rs':   (8,  4),
           'type': (5,  2),
           'Rn':   (16, 4),
           'Rm':   (0,  4)}


@instruction_decoder
class _data_processing_immediate():
    """
    op:0000x =     AND (S, Rn, Rd, imm12)       A1-I #a8-324
    op:0001x =     EOR (S, Rn, Rd, imm12)       A1-I #a8-382
    op:0010x
        Rn:!1111 = SUB (S, Rn, Rd, imm12)       A1-I #a8-710
        Rn:1111  = ADR (Rd, imm12)              A2   #a8-322
    op:0011x =     RSB (S, Rn, Rd, imm12)       A1-I #a8-574
    op:0100x
        Rn:!1111 = ADD (S, Rn, Rd, imm12)       A1-I #a8-308
        Rn:1111  = ADR (Rd, imm12)              A1   #a8-322
    op:0101x =     ADC (S, Rn, Rd, imm12)       A1-I #a8-300
    op:0110x =     SBC (S, Rn, Rd, imm12)       A1-I #a8-592
    op:0111x =     RSC (S, Rn, Rd, imm12)       A1-I #a8-580
    op:10xx0 =     _data_processing_and_misc         #a5-196
    op:10001 =     TST (Rn, imm12)              A1-I #a8-744
    op:10011 =     TEQ (Rn, imm12)              A1-I #a8-738
    op:10101 =     CMP (Rn, imm12)              A1-I #a8-370
    op:10111 =     CMN (Rn, imm12)              A1-I #a8-364
    op:1100x =     ORR (S, Rn, Rd, imm12)       A1-I #a8-516
    op:1101x =     MOV (S, Rd, imm12)           A1-I #a8-484 if RD = 1111 and S = 1 then SUBS PC, LR
    op:1110x =     BIC (S, Rn, Rd, imm12)       A1-I #a8-340
    op:1111x =     MVN (S, Rd, imm12)           A1-I #a8-504
    """
    positions = {'op': [20, 5],
                 'Rn': [16, 4]}
    ops = {'Rd':    (12, 4),
           'imm12': (0, 12),
           'S':     (20, 1),
           'Rn':    (16, 4)}


def _modified_immediate_constants(val):
    const = val & 0b11111111
    count = ((val >> 8) & 0b1111) * 2
    return ror(const, count, 32)



@instruction_decoder
class _multiply_and_multiply_accumulate():
    """
    op:000x = MUL   (S, Rd, Rm, Rn)            A1 #a8-502
    op:001x = MLA   (S, Rd, Ra, Rm, Rn)        A1 #a8-480
    op:0100 = UMAAL (RdHi, RdLo, Rm, Rn)       A1 #a8-774
    op:0101 = UDF   ()
    op:0110 = MLS   (Rd, Ra, Rm, Rn)           A1 #a8-482
    op:0111 = UDF   ()
    op:100x = UMULL (S, RdHi, RdLo, Rm, Rn)    A1 #a8-778
    op:101x = UMLAL (S, RdHi, RdLo, Rm, Rn)    A1 #a8-776
    op:110x = SMULL (S, RdHi, RdLo, Rm, Rn)    A1 #a8-646
    op:111x = SMLAL (S, RdHi, RdLo, Rm, Rn)    A1 #a8-624
    """
    positions = {'op': [20, 4]}
    ops = {'Rd':   (16, 4),
           'S':    (20, 1),
           'Rm':   (8,  4),
           'RdLo': (12, 4),
           'RdHi': (16, 4),
           'Ra':   (12, 4),
           'Rn':   (0,  4)}


@instruction_decoder
class _saturating_addition_and_subtraction():
    """
    op:00 = QADD  (Rn, Rd, Rm)    A1 #a8-540
    op:01 = QSUB  (Rn, Rd, Rm)    A1 #a8-554
    op:10 = QDADD (Rn, Rd, Rm)    A1 #a8-548
    op:11 = QDSUB (Rn, Rd, Rm)    A1 #a8-550
    """
    positions = {'op': [21, 2]}
    ops = {'Rd': (12, 4),
           'Rn': (16, 4),
           'Rm': (0,  4)}


@instruction_decoder
class _halfword_multiply_and_multiply_accumulate():
    """
    op1:00 =   SMLA  (Rd, Ra, Rm, M, N, Rn)        A1 #a8-620
    op1:01
        op:0 = SMLAW (Rd, Ra, Rm, M, Rn)           A1 #a8-630
        op:1 = SMULW (Rd, Rm, M, Rn)               A1 #a8-648
    op1:10 =   SMLAL (RdHi, RdLo, Rm, M, N, Rn)    A1 #a8-626
    op1:11 =   SMUL  (Rd, Rm, M, N, Rn)            A1 #a8-644
    """
    positions = {'op':  [7,  1],
                 'op1': [21, 2]}
    ops = {'Rd':   (16, 4),
           'Rm':   (8,  4),
           'N':    (5,  1),
           'M':    (6,  1),
           'RdLo': (12, 4),
           'RdHi': (16, 4),
           'Ra':   (12, 4),
           'Rn':   (0,  4)}


@instruction_decoder
class _extra_load_store_instructions():
    """
    op2:00 | op1:0xx11 = _data_processing_and_misc                     #a5-196
    op2:0x + op1:0xx10 = _data_processing_and_misc                     #a5-196
    op2:01
        op1:xx0x0 =      STRH (P, U, W, Rn, Rt, Rm)               A1-R #a8-702
        op1:xx0x1 =      LDRH (P, U, W, Rn, Rt, Rm)               A1-R #a8-446
        op1:xx1x0 =      STRH (P, U, W, Rn, Rt, imm4H, imm4L)     A1-I #a8-700
        op1:xx1x1
            Rn:!1111 =   LDRH (P, U, W, Rn, Rt, imm4H, imm4L)     A1-I #a8-442
            Rn:1111  =   LDRD (P, U, W, Rt, imm4H, imm4L)         A1-L #a8-444
    op2:10
        op1:xx0x0 =      LDRD  (P, U, W, Rn, Rt, Rm)              A1-R #a8-430
        op1:xx0x1 =      LDRSB (P, U, W, Rn, Rt, Rm)              A1-R #a8-454
        op1:xx1x0
            Rn:!1111 =   LDRD (P, U, W, Rn, Rt, imm4H, imm4L)     A1-I #a8-426
            Rn:1111  =   LDRD (U, Rt, imm4H, imm4L)               A1-L #a8-428
        op1:xx1x1
            Rn:!1111 =   LDRSB (P, U, W, Rn, Rt, imm4H, imm4L)    A1-I #a8-450
            Rn:1111  =   LDRSB (U, Rt, imm4H, imm4L)              A1-L #a8-452
    op2:11
        op1:xx0x0 =      STRD  (P, U, W, Rn, Rt, Rm)              A1-R #a8-688
        op1:xx0x1 =      LDRSH (P, U, W, Rn, Rt, Rm)              A1-R #a8-462
        op1:xx1x0 =      STRD  (P, U, W, Rn, Rt, imm4H, imm4L)    A1-I #a8-686
        op1:xx1x1
            Rn:!1111 =   LDRSH (P, U, W, Rn, Rt, imm4H, imm4L)    A1-I #a8-458
            Rn:1111  =   LDRSH (U, Rt, imm4H, imm4L)              A1-L #a8-460
    """
    positions = {'op1': [20, 5],
                 'Rn':  [16, 4],
                 'op2': [5,  2]}
    ops = {'imm4L': (0,  4),
           'Rt':    (12, 4),
           'P':     (24, 1),
           'W':     (21, 1),
           'imm4H': (8,  4),
           'Rn':    (16, 4),
           'Rm':    (0,  4),
           'U':     (23, 1)}


@instruction_decoder
class _extra_load_store_instructions_unprivileged():  # TODO: Confirm
    """
    op2:00 =        _data_processing_and_misc                #a5-196
    op2:1x + op:0 = _extra_load_store_instructions           #a5-203
    op2:01
        op:0
            pos22:1 = STRHT  (U, Rn, Rt, imm4H, imm4L)    A1 #a8-704 #TODO: confirm decoding
            pos22:0 = STRHT  (U, Rn, Rt, Rm)              A2 #a8-704 #TODO: confirm decoding
        op:1
            pos22:1 = LDRHT  (U, Rn, Rt, imm4H, imm4L)    A1 #a8-448 #TODO: confirm decoding
            pos22:0 = LDRHT  (U, Rn, Rt, Rm)              A2 #a8-448 #TODO: confirm decoding
    op2:10 + op:1
            pos22:1 = LDRSBT (U, Rn, Rt, imm4H, imm4L)    A1 #a8-456 #TODO: confirm decoding
            pos22:0 = LDRSBT (U, Rn, Rt, Rm)              A2 #a8-456 #TODO: confirm decoding
    op2:11 + op:1
            pos22:1 = LDRSHT (U, Rn, Rt, imm4H, imm4L)    A1 #a8-464 #TODO: confirm decoding
            pos22:0 = LDRSHT (U, Rn, Rt, Rm)              A2 #a8-464 #TODO: confirm decoding
    """
    positions = {'op':    [20, 1],
                 'op2':   [5,  2],
                 'pos22': [22, 1]}
    ops = {'imm4L': (0,  4),
           'Rm':    (0,  4),
           'imm4H': (8,  4),
           'Rn':    (16, 4),
           'Rt':    (12, 4),
           'U':     (23, 1)}


@instruction_decoder
class _synchronization_primitives():
    """
    op:0x00 = SWP    (B, Rn, Rt, Rt2)    A1 #a8-722 - deprecated
    op:1000 = STREX  (Rn, Rd, Rt2)       A1 #a8-690
    op:1001 = LDREX  (Rn, Rt)            A1 #a8-432
    op:1010 = STREXD (Rn, Rd, Rt2)       A1 #a8-694
    op:1011 = LDREXD (Rn, Rt)            A1 #a8-436
    op:1100 = STREXB (Rn, Rd, Rt2)       A1 #a8-692
    op:1101 = LDREXB (Rn, Rt)            A1 #a8-434
    op:1110 = STREXH (Rn, Rd, Rt2)       A1 #a8-696
    op:1111 = LDREXH (Rn, Rt)            A1 #a8-438
    """
    positions = {'op': [20, 4]}
    ops = {'Rd':  (12, 4),
           'Rt2': (0,  4),
           'B':   (22, 1),
           'Rn':  (16, 4),
           'Rt':  (12, 4)}


@instruction_decoder
class _msr_and_hints_immediate():
    """
    op:0
        op1:0000
            op2:00000000 = NOP   ()                  A1 #a8-510
            op2:00000001 = YIELD ()                  A1 #a8-1108
            op2:00000010 = WFE   ()                  A1 #a8-1104
            op2:00000011 = WFI   ()                  A1 #a8-1106
            op2:00000100 = SEV   ()                  A1 #a8-606
            op2:1111xxxx = DBG   (option)            A1 #a8-377
        op1:0100 | 1x00 =  MSR   (mask, imm12)       A1 #a8-498 - application level
        op1:xx00 | xx1x =  MSR   (R, mask, imm12)    A1 #b9-1994 - system level
    op:1 =                 MSR   (R, mask, imm12)    A1 #b9-1994 - system level
    """
    positions = {'op':  [22, 1],
                 'op1': [16, 4],
                 'op2': [0,  8]}
    ops = {'imm12':  (0,  12),
           'option': (0,  4),
           'mask':   (18, 2),
           'R':      (22, 1)}


@instruction_decoder
class _misc_instructions():  # TODO: Confirm
    """
    op2:000
        B:1
            op:x0 =               MRS  (R, m1, Rd, m)                     A1-BR #b9-1990
            op:x1 =               MSR  (R, m1, m, Rn)                     A1-BR #b9-1992
        B:0
            op:x0 =               MRS  (R, Rd)                            A1    #app level a8-496, sys level b9-1988
            op:01
                op1:xx00 =        MSR  (mask, Rn)                         A1-R  #a8-500
                op1:xx01 | xx1x = MSR  (R, mask, Rn)                      A1-R  #b9-1996
            op:11 =               MSR  (R, mask, Rn)                      A1-R  #b9-1996
    op2:001
        op:01 =                   BX   (Rm)                               A1    #a8-352
        op:11 =                   CLZ  (Rd, Rm)                           A1    #a8-362
    op2:010 + op:01 =             BXJ  (Rm)                               A1    #a8-354
    op2:011 + op:01 =             BLX  (Rm)                               A1-R  #a8-350
    op2:101 =                     _saturating_addition_and_subtraction          #a5-202
    op2:110 + op:11 =             ERET ()                                 A1    #b9-1980
    op2:111
        op:01 =                   BKPT (imm12, imm4)                      A1    #a8-346
        op:10 =                   HVC  (imm12, imm4)                      A1    #b9-1982
        op:11 =                   SMC  (imm4)                             A1    #b9-2000 - previously SMI
    """
    positions = {'op':  [21, 2],
                 'op1': [16, 4],
                 'B':   [9,  1],
                 'op2': [4,  3]}
    ops = {'Rd':    (12, 4),
           'imm12': (8,  12),
           'mask':  (18, 2),
           'imm4':  (0,  4),
           'm':     (8,  1),
           'R':     (22, 1),
           'm1':    (16, 4),
           'Rn':    (0,  4),
           'Rm':    (0,  4)}


@instruction_decoder
class _load_store_word_and_unsigned_byte():
    """
    A:0
        op1:xx0x0 + !0x010 =       STR   (P, U, W, Rn, Rt, imm12)             A1-I #a8-674
        op1:0x010 =                STRT  (U, Rn, Rt, imm12)                   A1   #a8-706
        op1:xx0x1 + !0x011
            Rn:!1111 =             LDR   (P, U, W, Rn, Rt, imm12)             A1-I #a8-408
            Rn:1111  =             LDR   (U, Rt, imm12)                       A1-L #a8-410
        op1:0x011 =                LDRT  (U, Rn, Rt, imm12)                   A1   #a8-466
        op1:xx1x0 + !0x110 =       STRB  (P, U, W, Rn, Rt, imm12)             A1-I #a8-680
        op1:0x110 =                STRBT (U, Rn, Rt, imm12)                   A1   #a8-684
        op1:xx1x1 + !0x111
            Rn:!1111 =             LDRB  (P, U, W, Rn, Rt, imm12)             A1-I #a8-418
            Rn:1111  =             LDRB  (U, Rt, imm12)                       A1-L #a8-420
        op1:0x111 =                LDRBT (U, Rn, Rt, imm12)                   A1   #a8-424
    A:1
        op1:xx0x0 + !0x010 + B:0 = STR   (P, U, W, Rn, Rt, imm5, type, Rm)    A1-R #a8-676
        op1:0x010 + B:0 =          STRT  (U, Rn, Rt, imm5, type, Rm)          A2   #a8-706
        op1:xx0x1 + !0x011 + B:0 = LDR   (P, U, W, Rn, Rt, imm5, type, Rm)    A1-R #a8-414
        op1:0x001 + B:0 =          LDRT  (U, Rn, Rt, imm5, type, Rm)          A2   #a8-466
        op1:xx1x0 + !0x110 + B:0 = STRB  (P, U, W, Rn, Rt, imm5, type, Rm)    A1-R #a8-682
        op1:0x110 + B:0 =          STRBT (U, Rn, Rt, imm5, type, Rm)          A2   #a8-684
        op1:xx1x1 + !0x111 + B:0 = LDRB  (P, U, W, Rn, Rt, imm5, type, Rm)    A1-R #a8-422
        op1:0x111 + B:0 =          LDRBT (U, Rn, Rt, imm5, type, Rm)          A2   #a8-424
    """
    positions = {'A':   [25, 1],
                 'op1': [20, 5],
                 'B':   [4,  1],
                 'Rn':  [16, 4]}
    ops = {'imm12': (0, 12),
           'Rt':    (12, 4),
           'P':     (24, 1),
           'W':     (21, 1),
           'type':  (5,  2),
           'imm5':  (7,  5),
           'Rn':    (16, 4),
           'Rm':    (0,  4),
           'U':     (23, 1)}


@instruction_decoder
class _media_instructions():  # TODO: Confirm
    """
    op1:000xx =           _parallel_addition_subtraction_signed             #a5-210
    op1:001xx =           _parallel_addition_subtraction_unsigned           #a5-211
    op1:01xxx =           _packing_unpacking_saturation_reversal            #a5-212
    op1:10xxx =           _signed_multiply_signed_and_unsigned_divide       #a5-213
    op1:11000 + op2:000
        Rd:1111  =        USAD8  (Rd, Rm, Rn)                            A1 #a8-792
        Rd:!1111 =        USADA8 (Rd, Ra, Rm, Rn)                        A1 #a8-794
    op1:1101x + op2:x10 = SBFX   (widthm1, Rd1, lsb, Rn)                 A1 #a8-598
    op1:1110x + op2:x00
        Rn:1111  =        BFC    (msb, Rd1, lsb)                         A1 #a8-336
        Rn:!1111 =        BFI    (msb, Rd1, lsb, Rn)                     A1 #a8-338
    op1:1111x + op2:x10 = UBFX   (widthm1, Rd1, lsb, Rn)                 A1 #a8-756
    ## *** TODO: confirm the following decoding ***
    #op1:11111 + op2:111
    #    cond:1110  =     UDF    (imm12, imm4)                            A1 #a8-758
    #    cond:!1110 =     UDF    (imm12, imm4)                            A1 #a8-758
    """
    positions = {#'cond': [28, 4], # uncomment if the above template needs this
                 'Rd':  [12, 4],
                 'op1': [20, 5],
                 'op2': [5,  3],
                 'Rn':  [0,  4]}
    ops = {'Rd':      (16, 4),
           'imm12':   (8, 12),
           'lsb':     (7,  5),
           'Rd1':     (12, 4),
           'Ra':      (12, 4),
           'widthm1': (16, 5),
           'imm4':    (0,  4),
           'Rn':      (0,  4),
           'msb':     (16, 5),
           'Rm':      (8,  4)}


@instruction_decoder
class _parallel_addition_subtraction_signed():
    """
    op1:01
        op2:000 = SADD16  (Rn, Rd, Rm)    #a8-586
        op2:001 = SASX    (Rn, Rd, Rm)    #a8-590
        op2:010 = SSAX    (Rn, Rd, Rm)    #a8-656
        op2:011 = SSUB16  (Rn, Rd, Rm)    #a8-658
        op2:100 = SADD8   (Rn, Rd, Rm)    #a8-588
        op2:111 = SSUB8   (Rn, Rd, Rm)    #a8-660
    op1:10
        op2:000 = QADD16  (Rn, Rd, Rm)    #a8-542
        op2:001 = QASX    (Rn, Rd, Rm)    #a8-546
        op2:010 = QSAX    (Rn, Rd, Rm)    #a8-552
        op2:011 = QSUB16  (Rn, Rd, Rm)    #a8-556
        op2:100 = QADD8   (Rn, Rd, Rm)    #a8-544
        op2:111 = QSUB8   (Rn, Rd, Rm)    #a8-558
    op1:11
        op2:000 = SHADD16 (Rn, Rd, Rm)    #a8-608
        op2:001 = SHASX   (Rn, Rd, Rm)    #a8-612
        op2:010 = SHSAX   (Rn, Rd, Rm)    #a8-614
        op2:011 = SHSUB16 (Rn, Rd, Rm)    #a8-616
        op2:100 = SHADD8  (Rn, Rd, Rm)    #a8-610
        op2:111 = SHSUB8  (Rn, Rd, Rm)    #a8-618
    """
    positions = {'op1': [20, 2],
                 'op2': [5,  3]}
    ops = {'Rd': (12, 4),
           'Rn': (16, 4),
           'Rm': (0,  4)}


@instruction_decoder
class _parallel_addition_subtraction_unsigned():
    """
    op1:01
        op2:000 = UADD16  (Rn, Rd, Rm)    #a8-750
        op2:001 = UASX    (Rn, Rd, Rm)    #a8-754
        op2:010 = USAX    (Rn, Rd, Rm)    #a8-800
        op2:011 = USUB16  (Rn, Rd, Rm)    #a8-802
        op2:100 = UADD8   (Rn, Rd, Rm)    #a8-752
        op2:111 = USUB8   (Rn, Rd, Rm)    #a8-804
    op1:10
        op2:000 = UQADD16 (Rn, Rd, Rm)    #a8-780
        op2:001 = UQASX   (Rn, Rd, Rm)    #a8-784
        op2:010 = UQSAX   (Rn, Rd, Rm)    #a8-786
        op2:011 = UQSUB16 (Rn, Rd, Rm)    #a8-788
        op2:100 = UQADD8  (Rn, Rd, Rm)    #a8-782
        op2:111 = UQSUB8  (Rn, Rd, Rm)    #a8-790
    op1:11
        op2:000 = UHADD16 (Rn, Rd, Rm)    #a8-762
        op2:001 = UHASX   (Rn, Rd, Rm)    #a8-766
        op2:010 = UHSAX   (Rn, Rd, Rm)    #a8-768
        op2:011 = UHSUB16 (Rn, Rd, Rm)    #a8-770
        op2:100 = UHADD8  (Rn, Rd, Rm)    #a8-764
        op2:111 = UHSUB8  (Rn, Rd, Rm)    #a8-772
    """
    positions = {'op1': [20, 2],
                 'op2': [5,  3]}
    ops = {'Rd': (12, 4),
           'Rn': (16, 4),
           'Rm': (0,  4)}


@instruction_decoder
class _packing_unpacking_saturation_reversal():
    """
    op1:000
        op2:xx0 =       PKH     (Rn, Rd, imm5, tb, Rm)          #a8-522
        op2:011
            A:!1111 =   SXTAB16 (Rn, Rd, rotate, Rm)            #a8-726
            A:1111  =   SXTB16  (Rd, rotate, Rm)                #a8-732
        op2:101 =       SEL     (Rn, Rd, Rm)                    #a8-602
    op1:01x + op2:xx0 = SSAT    (sat_imm, Rd, imm5, sh, Rn1)    #a8-652
    op1:010
        op2:001 =       SSAT16  (sat_imm, Rd, Rn1)              #a8-654
        op2:011
            A:!1111 =   SXTAB   (Rn, Rd, rotate, Rm)            #a8-724
            A:1111  =   SXTB    (Rd, rotate, Rm)                #a8-730
    op1:011
        op2:001 =       REV     (Rd, Rm)                        #a8-562
        op2:011
            A:!1111 =   SXTAH   (Rn, Rd, rotate, Rm)            #a8-728
            A:1111  =   SXTH    (Rd, rotate, Rm)                #a8-734
        op2:101 =       REV16   (Rd, Rm)                        #a8-564
    op1:100 + op2:011
        A:!1111 =       UXTAB16 (Rd, Rd, rotate, Rm)            #a8-808
        A:1111  =       UXTB16  (Rd, rotate, Rm)                #a8-814
    op1:11x + op2:xx0 = USAT    (sat_imm, Rd, imm5, sh, Rn1)    #a8-796
    op1:110
        op2:001 =       USAT16  (sat_imm, Rd, Rn1)              #a8-798
        op2:011
            A:!1111 =   UXTAB   (Rn, Rd, rotate, Rm)            #a8-806
            A:1111  =   UXTB    (Rd, rotate, Rm)                #a8-812
    op1:111
        op2:001 =       RBIT    (Rd, Rm)                        #a8-560
        op2:011
            A:!1111 =   UXTAH   (Rn, Rd, rotate, Rm)            #a8-810
            A:1111  =   UXTH    (Rd, rotate, Rm)                #a8-816
        op2:101 =       REVSH   (Rd, Rm)                        #a8-566
    """
    positions = {'A':   [16, 4],
                 'op1': [20, 3],
                 'op2': [5,  3]}
    ops = {'Rd':      (12, 4),
           'Rn1':     (0, 4),
           'tb':      (6, 1),
           'rotate':  (10, 2),
           'sh':      (6, 1),
           'imm5':    (7, 5),
           'Rn':      (16, 4),
           'Rm':      (0, 4),
           'sat_imm': (16, 5)}


@instruction_decoder
class _signed_multiply_signed_and_unsigned_divide():
    """
    op1:000
        op2:00x
            A:!1111 =   SMLAD  (Rd, Ra, Rm, M, Rn)        #a8-622
            A:1111  =   SMUAD  (Rd, Rm, M, Rn)            #a8-642
        op2:01x
            A:!1111 =   SMLSD  (Rd, Ra, Rm, M, Rn)        #a8-632
            A:1111  =   SMUSD  (Rd, Rm, M, Rn)            #a8-650
    op1:001 + op2:000 = SDIV   (Rd, Rm, Rn)               #a8-600
    op1:011 + op2:000 = UDIV   (Rd, Rm, Rn)               #a8-760
    op1:100
        op2:00x =       SMLALD (RdHi, RdLo, Rm, M, Rn)    #a8-628
        op2:01x =       SMLSLD (RdHi, RdLo, Rm, M, Rn)    #a8-634
    op1:101
        op2:00x
            A:!1111 =   SMMLA  (Rd, Ra, Rm, R, Rn)        #a8-636
            A:1111  =   SMMUL  (Rd, Rm, R, Rn)            #a8-640
        op2:11x =       SMMLS  (Rd, Ra, Rm, R, Rn)        #a8-638
    """
    positions = {'A':   [12, 4],
                 'op1': [20, 3],
                 'op2': [5,  3]}
    ops = {'Rd':   (16, 4),
           'Rm':   (8, 4),
           'R':    (5, 1),
           'M':    (5, 1),
           'RdLo': (12, 4),
           'RdHi': (16, 4),
           'Ra':   (12, 4),
           'Rn':   (0, 4)}


@instruction_decoder
class _branch_branch_with_link_and_block_data_transfer():  # TODO: Confirm
    """
    op:0000x0 =    STMDA (W, Rn, register_list)          A1    #a8-666
    op:0000x1 =    LDMDA (W, Rn, register_list)          A1    #a8-400
    op:0010x0 =    STM   (W, Rn, register_list)          A1    #a8-664
    op:001001 =    LDM   (W, Rn, register_list)          A1    #a8-398
    op:001011
        Rn:!1101 = LDM   (W, Rn, register_list)          A1    #a8-398
        Rn:1101  = POP   (register_list)                 A1    #a8-536
    op:010000 =    STMDB (W, Rn, register_list)          A1    #a8-668
    op:010010
        Rn:!1101 = STMDB (W, Rn, register_list)          A1    #a8-668
        Rn:1101 =  PUSH  (register_list)                 A1    #a8-538
    op:0100x1 =    LDMDB (W, Rn, register_list)          A1    #a8-402
    op:0110x0 =    STMIB (W, Rn, register_list)          A1    #a8-670
    op:0110x1 =    LDMIB (W, Rn, register_list)          A1    #a8-404
    op:0xx1x0 =    STM   (P, U, Rn, register_list)       A1    #b9-2006
    op:0xx1x1
        R:0 =      LDM   (P, U, Rn, register_list)       A1    #b9-1986
        R:1 =      LDM   (P, U, W, Rn, register_list)    A1-ER #b9-1984
    op:10xxxx =    B     (imm24)                         A1    #a8-334
    op:11xxxx =    BL    (imm24)                         A1-I  #a8-348
    """
    positions = {'op': [20, 6],
                 'Rn': [16, 4],
                 'R':  [15, 1]}
    ops = {'register_list': (0, 16),
           'imm24':         (0, 24),
           'P':             (24, 1),
           'W':             (21, 1),
           'Rn':            (16, 4),
           'U':             (23, 1)}


@instruction_decoder
class _coprocessor_instructions_and_supervisor_call():
    """
    op1:00000x =               UDF  ()
    op1:11xxxx =               SVC  (imm24)                                         #a8-720
    coproc:!101x
        op1:0xxxx0 | !000x00 = STC  (P, U, D, W, Rn, CRd, coproc, imm8)             #a8-662
        op1:0xxxx1 | !000x01
            Rn:!1111 =         LDC  (P, U, D, W, Rn, CRd, coproc, imm8)             #a8-392 - immediate
            Rn:1111  =         LDC  (P, U, D, W, CRd, coproc, imm8)                 #a8-394 - literal
        op1:000100 =           MCRR (Rt2, Rt, coproc, opc1, CRm)                    #a8-478
        op1:000101 =           MRRC (Rt2, Rt, coproc, opc1, CRm)                    #a8-494
        op1:10xxxx + op:0 =    CDP  (opc1_2, CRn, CRd, coproc, opc2, CRm)           #a8-358
        op1:10xxx0 + op:1 =    MCR  (opc1_2, CRn, CRd, coproc, opc2, CRm)           #a8-476
        op1:10xxx1 + op:1 =    MRC  (opc1_3, CRn, Rt, coproc, opc2, CRm)            #a8-492
    coproc:101x
        op1:0xxxxx | !000x0x = _extension_register_load_store_instructions          #a7-274
        op1:00010x =           _64bit_transfers_arm_core_extension_registers        #a7-279
        op1:10xxxx
            op:0 =             _floating_point_data_processing_instructions         #a7-272
            op:1 =             _8_16_32bit_transfer_arm_core_extension_registers    #a7-278

    """
    positions = {'op':     [4,  1],
                 'op1':    [20, 6],
                 'Rn':     [16, 4],
                 'coproc': [8, 4]}
    ops = {'Rt2':    (16, 4),
           'imm24':  (0, 24),
           'CRm':    (0,  4),
           'Rt':     (12, 4),
           'opc1':   (4,  4),
           'W':      (21, 1),
           'D':      (22, 1),
           'opc1_3': (21, 3),
           'imm8':   (0,  8),
           'CRd':    (12, 4),
           'opc1_2': (20, 4),
           'coproc': (8,  4),
           'P':      (24, 1),
           'opc2':   (5,  3),
           'CRn':    (16, 4),
           'Rn':     (16, 4),
           'U':      (23, 1)}


@instruction_decoder
class _extension_register_load_store_instructions():  # TODO: Confirm
    """
    opcode:0010x = _64bit_transfers_arm_core_extension_registers    #A7-279
    opcode:01x00 = VSTM  (P, U, D, W, Rn, Vd, imm8)                 #a8-1080 - no writeback TODO: confirm A1 encoding
    opcode:01x10 = VSTM  (P, U, D, W, Rn, Vd, imm8)                 #a8-1080
    opcode:1xx00 = VSRT  (U, D, Rn, Vd, imm8)                       #a8-1082
    opcode:10x10
        Rn:!1101 = VSTM  (P, U, D, W, Rn, Vd, imm8)                 #a8-1080
        Rn:1101  = VPUSH (D, Vd, imm8)                              #a8-992
    opcode:01x01 = VLDM  (P, U, D, W, Rn, Vd, imm8)                 #a8-922 - no writeback
    opcode:1xx01
        Rn:!1101 = VLDM  (P, U, D, W, Rn, Vd, imm8)                 #a8-922
        Rn:1101  = VPOP  (D, Vd, imm8)                              #a8-990
    opcode:1x001 = VLDR  (U, D, Rn, Vd, imm8)                       #a8-924
    opcode:10x11 = VLDM  (P, U, D, W, Rn, Vd, imm8)                 #a8-922 - Decrement before, writeback
    """
    positions = {'Rn':     [16, 4],
                 'opcode': [20, 5]}
    ops = {'imm8': (0,  8),
           'Vd':   (12, 4),
           'P':    (24, 1),
           'W':    (21, 1),
           'D':    (22, 1),
           'Rn':   (16, 4),
           'U':    (23, 1)}


@instruction_decoder
class _floating_point_data_processing_instructions():
    """
    opc1:0x00 =               VMLA  (D, op, sz, Vn, Vd, N, Q, M, Vm)          #a8-932
    opc1:0x01 =               VNMLA (D, Vn, Vd, sz_2, N, op_2, M, Vm)         #a8-970
    opc1:0x10
        opc3:x1 =             VNMLA (D, Vn, Vd, sz_2, N, op_2, M, Vm)         #a8-970
        opc3:x0 =             VMUL  (D, sz, Vn, Vd, N, Q, M, Vm)              #a8-960
    opc1:0x11
        opc3:x0 =             VADD  (D, sz, Vn, Vd, N, Q, M, Vm)              #a8-830
        opc3:x1 =             VSUB  (D, sz, Vn, Vd, N, Q, M, Vm)              #a8-1086
    opc1:1x00 + opc3:x0 =     VDIV  (D, Vn, Vd, sz_2, N, M, Vm)               #a8-882
    opc1:1x01 =               VFNMA (D, Vn, Vd, sz_2, N, op_2, M, Vm)         #a8-894
    opc1:1x10 =               VFMA  (D, op, sz, Vn, Vd, N, Q, M, Vm)          #a8-892
    opc1:1x11
        opc3:x0 =             VMOV  (i, D, imm3, Vd, cmode, Q, op_3, imm4)    #a8-936 - immediae
        opc2:0000
            opc3:01 =         VMOV  (D, Vm, Vd, M_2, Q, M, Vm)                #a8-938 - register
            opc3:11 =         VABS  (D, size, Vd, F, Q, M, Vm)                #a8-824
        opc2:0001
            opc3:01 =         VNEG  (D, size, Vd, F, Q, M, Vm)                #a8-968
            opc3:11 =         VSQRT (D, Vd, sz_2, M, Vm)                      #a8-1058
        opc2:001x + opc3:x1 = VCVTB (D, op_4, Vd, T, M, Vm)                   #a8-880
        opc2:010x + opc3:x1 = VCMP  (D, Vd, sz_2, E)                          #a8-864
        opc2:0111 + opc3:11 = VCVT  (D, Vd, sz_2, M, Vm)                      #a8-876 - double and single precision
        opc2:1000 + opc3:x1 = VCVT  (D, opc2, Vd, sz_2, op_5, M, Vm)          #a8-870 - floating and integer
        opc2:101x + opc3:x1 = VCVT  (D, op_6, U, Vd, sf, sx, i_2, imm4)       #a8-874 - floating and fixed
        opc2:110x + opc3:x1 = VCVT  (D, opc2, Vd, sz_2, op_5, M, Vm)          #a8-870 - floating and integet
        opc2:111x + opc3:x1 = VCVT  (D, op_6, U, Vd, sf, sx, i_2, imm4)       #a8-874 - floating and fixed
    """
    positions = {'opc1': [20, 4],
                 'opc2': [16, 4],
                 'opc4': [0,  4],
                 'opc3': [6,  2]}
    ops = {'size':  (18, 2),
           'op_6':  (18, 1),
           'T':     (7,  1),
           'imm3':  (16, 3),
           'Vd':    (12, 4),
           'imm4':  (0,  4),
           'i_2':   (5,  1),
           'N':     (7,  1),
           'op_3':  (5,  1),
           'Vm':    (0,  4),
           'sz':    (20, 1),
           'F':     (10, 1),
           'Vn':    (16, 4),
           'sx':    (7,  1),
           'Q':     (6,  1),
           'opc2':  (16, 3),
           'op_5':  (7,  1),
           'U':     (16, 1),
           'i':     (24, 1),
           'M':     (5,  1),
           'M_2':   (7,  1),
           'D':     (22, 1),
           'op_4':  (16, 1),
           'op_2':  (6,  1),
           'sf':    (8,  1),
           'cmode': (8,  4),
           'op':    (21, 1),
           'E':     (7,  1),
           'sz_2':  (8,  1)}


@instruction_decoder
class _8_16_32bit_transfer_arm_core_extension_registers():
    """
    L:0
        C:0
            A:000 =        VMOV (op, Vn, Rt, N)               #a8-944
            A:111 =        VMSR (reg, Rt)                     #a8-956 or b9-2014 for system level - use reg if sys level
        C:1
            A:0xx =        VMOV (opc1, Vd, Rt, D, opc2)       #a8-940
            A:1xx + B:0x = VDUP (B, Q, Vd, Rt, D, E)          #a8-886
    L:1
        C:0
            A:000 =        VMOV (op, Vn, Rt, N)               #a8-944
            A:111 =        VMRS (reg, Rt)                     #a8-954 or B9-2012 for system level - use reg if sys level
        C:1 =              VMOV (U, opc1, Vn, Rt, N, opc2)    #a8-942
    """
    positions = {'A': [21, 3],
                 'C': [8,  1],
                 'L': [20, 1],
                 'B': [5,  2]}
    ops = {'Q':    (21, 1),
           'Vd':   (16, 4),
           'Rt':   (12, 4),
           'opc1': (21, 2),
           'D':    (7,  1),
           'N':    (7,  1),
           'E':    (5,  1),
           'Vn':   (16, 4),
           'op':   (20, 1),
           'opc2': (5,  2),
           'U':    (23, 1),
           'B':    (22, 1),
           'reg':  (16, 4)}


@instruction_decoder
class _64bit_transfers_arm_core_extension_registers():
    """
    op:00x1
        C:0 = VMOV (op, Rt2, Rt, M, Vm)    #a9-946 - two single-precision registers
        C:1 = VMOV (op, Rt2, Rt, M, Vm)    #a8-948 - doubleword extension register
    """
    positions = {'op': [4,  4],
                 'C':  [20, 1]}
    ops = {'op':  (20, 1),
           'Rt2': (16, 4),
           'Vm':  (0,  4),
           'M':   (5,  1),
           'Rt':  (12, 4)}


@instruction_decoder
class _unconditional_instructions():
    """
    op1:0xxxxxxx =             _memory_hints_advanced_simd_instructions_and_misc_instructions         #a5-217
    op1:100xx1x0 =             SRS   (P, U, W, mode)                                                  #b9-2004
    op1:100xx0x1 =             RFE   (P, U, W, Rn)                                                    #b9-1998
    op1:101xxxxx =             BL    (H, imm24)                                                  A2-I #a8-348 - BLX
    op1:110xxxx0 | !11000x00 = STC2  (P, U, D, W, Rn, CRd, coproc, imm8)                              #a8-662
    op1:110xxxx1 | !11000x01
        Rn:!1111 =             LDC2  (P, U, D, W, Rn, CRd, coproc, imm8)                              #a8-392
        Rn:1111  =             LDC2  (P, U, D, W, CRd, coproc, imm8)                                  #a8-394
    op1:11000100 =             MCRR2 (Rt2, Rt, coproc, opc1, CRm)                                     #a8-478
    op1:11000101 =             MRRC2 (Rt2, Rt, coproc, opc1, CRm)                                     #a8-494
    op1:1110xxxx + op:0 =      CDP2  (opc1_2, CRn, CRd, coproc, opc2, CRm)                            #a8-358
    op1:1110xxx0 + op:1 =      MCR2  (opc1_2, CRn, Rt, coproc, opc2, CRm)                             #a8-476
    op1:1110xxx1 + op:1 =      MRC2  (opc1_2, CRn, Rt, coproc, opc2, CRm)                             #a8-492
    """
    positions = {'op':  [4,  1],
                 'op1': [20, 8],
                 'Rn':  [16, 4]}
    ops = {'Rt2':    (16, 4),
           'imm24':  (0, 24),
           'CRm':    (0,  4),
           'mode':   (0,  5),
           'Rt':     (12, 4),
           'opc1':   (4,  4),
           'W':      (21, 4),
           'D':      (22, 1),
           'imm8':   (0,  8),
           'CRd':    (12, 4),
           'opc1_2': (20, 4),
           'H':      (24, 1),
           'coproc': (8,  4),
           'P':      (24, 1),
           'opc2':   (5,  3),
           'CRn':    (16, 4),
           'Rn':     (16, 4),
           'U':      (23, 4)}


@instruction_decoder
class _memory_hints_advanced_simd_instructions_and_misc_instructions():  # TODO: Complete
    """
    op1:0010000
        op2:xx0x + Rn:xxx0 = CPS    (imod, M, A, I, F, mode)                     #b9-1978
        op2:0000 + Rn:xxx1 = SETEND (E)                                          #a8-604
    op1:01xxxxx =            _advanced_SIMD_data_processing_instructions         #a7-261
    op1:100xxx0 = "Advanced SIMD element or structure load/store instructions a7-275"
    op1:100x001 = "Unallocated memory hint (treat as NOP)"
    op1:100x101 =            PLI    (U, Rn, imm12)                               #a8-530
    op1:100xx11 =           "UNPREDICTABLE"
    op1:101x001
        Rn:!1111 =           PLD    (U, R, Rn, imm12)                            #a8-524
        Rn:1111  =           "UNPREDICTABLE" #possibly PLD literal a8-526
    op1:101x101
        Rn:!1111 =           PLD    (U, R, Rn, imm12)                            #a8-524
        Rn:1111  =           PLD    (U, imm12)                                   #a8-526
    op1:1010011 =            "UNPREDICTABLE"
    op1:1010111
        op2:0000 =           "UNPREDICTABLE"
        op2:0001 =           CLREX ()                                            #a8-360
        op2:001x =           "UNPREDICTABLE"
        op2:0100 =           DSB    (option)                                     #a8-380
        op2:0101 =           DMB    (option)                                     #a8-378
        op2:0110 =           ISB    (option)                                     #a8-389
        op2:0111 =           "UNPREDICTABLE"
        op2:1xxx =           "UNPREDICTABLE"
    op1:1011x11 =            "UNPREDICTABLE"
    op2:xxx0
        op1:110x001 =        "Unallocated memory hint (treat as NOP)"
        op1:110x101 =        PLI    (U, Rn, imm5, type, Rm)                      #a8-532
        op1:111x001 =        PLD    (U, R, Rn, imm5, type, Rm)                   #a8-528
        op1:111x101 =        PLD    (U, R, Rn, imm5, type, Rm)                   #a8-528
        op1:11xxx11 =        "UNPREDICTABLE"
    op1:1111111 + op2:1111 = UDF    (imm12, imm4)                                #a8-758
    """
    positions = {'op1': [20, 7],
                 'Rn':  [16, 4],
                 'op2': [4,  4]}
    ops = {'imm12':   (0, 12),
           'E':       (9,  1),
           'imod':    (18, 2),
           'imm4':    (0,  4),
           'mode':    (0,  5),
           'imm5':    (7,  5),
           'Rm':      (0,  4),
           'option':  (0,  4),
           'F':       (6,  1),
           'R':       (22, 1),
           'A':       (8,  1),
           'I':       (7,  1),
           'imm12_2': (8, 12),
           'M':       (17, 1),
           'Rn':      (16, 4),
           'type':    (5,  2),
           'U':       (23, 1)}


@instruction_decoder
class _advanced_SIMD_data_processing_instructions():  # TODO: Complete
    """
    A:0xxxx =                         "Three registers of the same length"    #a7-262
    C:0xx1
        A:1x000 =                     "One register and a modified immediate" #a7-269
        A:1x001 | A:1x01x | A:1x1xx = "Two registers and a shift amount"      #a7-266
    A:1xxxx + C:1xx1 =                "Two registers and a shift amount"      #a7-266
    C:x0x0
        A:1x0xx | A:1x10x =           "Three registers of different lengths"  #a7-264
    C:x1x0
        A:1x0xx | A:1x10x =           "Tw registers and a scalar"             #a7-265
    U:0 + A:1x11x + C:xxx0 =          VEXT                                    #a8-890
    U:1 + A:1x11x
        C:xxx0
            B:0xxx =                  "Two registers, misc"                   #a7-267
            B:10xx =                  VTBL #or VTBX                           #a8-1094
        B:1100 + C:0xx0 =             VDUP                                    #a8-884

    """
    positions = {'A': [19, 5],
                 'C': [4,  4],
                 'B': [8,  4],
                 'U': [24, 1]}

@instruction_decoder
class _advanced_SIMD_element_structure_load_store_instructions:
    """

    """
    positions = {}