__author__ = 'tdp'

from Decode.decoder_tools import instruction_decoder

default_encoding = "T1"


@instruction_decoder
class t16():
    """
    Opcode:00xxxx = _shift_add_subtract_move_compare                         #a6-224
    Opcode:010000 = _data_processing                                         #a6-225
    Opcode:010001 = _special_data_instructions_branch_exchange               #a6-226
    Opcode:01001x = LDR (Rt, imm8)                                    T1-L   #a8-410
    Opcode:0101xx | 011xxx | 100xxx = _load_store_single_data_item           #a6-227
    Opcode:10100x = ADR (Rd, imm8)                                    T1     #a8-322 - generate PC-relative address
    Opcode:10101x = ADD (Rd, imm8)                                    T1-SPI #a8-316 - SP plus immediate
    Opcode:1011xx = _misc_16bit_instructions                                 #a6-228
    Opcode:11000x = STM (Rn, register_list)                           T1     #a8-664
    Opcode:11001x = LDM (Rn, register_list)                           T1     #a8-396
    Opcode:1101xx = _conditional_branch_supervisor_call                      #a6-229
    Opcode:11100x = B (imm11)                                         T2     #a8-334
    """
    positions = {'Opcode': [10, 6]}
    ops = {'imm8':          (0, 8),
           'Rn':            (8, 3),
           'register_list': (0, 8),
           'Rd':            (8, 3),
           'Rt':            (8, 3),
           'imm11':         (0, 11)}


@instruction_decoder
class _shift_add_subtract_move_compare():
    """
    Opcode:000xx = LSL (imm5, Rm, Rd)    T1-I #a8-468
    Opcode:001xx = LSR (imm5, Rm, Rd)    T1-I #a8-472
    Opcode:010xx = ASR (imm5, Rm, Rd)    T1-I #a8-330
    Opcode:01100 = ADD (Rm_2, Rn, Rd)    T1-R #a8-310
    Opcode:01101 = SUB (Rm_2, Rn, Rd)    T1-R #a8-712
    Opcode:01110 = ADD (imm3, Rn, Rd)    T1-I #a8-306
    Opcode:01111 = SUB (imm3, Rn, Rd)    T1-I #a8-708
    Opcode:100xx = MOV (Rd, imm8)        T1-I #a8-484
    Opcode:101xx = CMP (Rn_2, imm8)      T1-I #a8-370
    Opcode:110xx = ADD (Rdn, imm8)       T2-I #a8-306
    Opcode:111xx = SUB (Rdn, imm8)       T2-I #a8-708
    """
    positions = {'Opcode': [9, 5]}
    ops = {'imm8': (0, 8),
           'Rn':   (3, 3),
           'Rd_2': (8, 3),
           'Rdn':  (8, 3),
           'imm5': (6, 5),
           'Rd':   (0, 3),
           'Rn_2': (8, 3),
           'imm3': (6, 3),
           'Rm':   (3, 3),
           'Rm_2': (6, 3)}


@instruction_decoder
class _data_processing():
    """
    Opcode:0000 = AND (Rm, Rdn)      T1-R #a8-326
    Opcode:0001 = EOR (Rm, Rdn)      T1-R #a8-384
    Opcode:0010 = LSL (Rm, Rdn)      T1-R #a8-470
    Opcode:0011 = LSR (Rm, Rdn)      T1-R #a8-474
    Opcode:0100 = ASR (Rm, Rdn)      T1-R #a8-332
    Opcode:0101 = ADC (Rm, Rdn)      T1-R #a8-302
    Opcode:0110 = SBC (Rm, Rdn)      T1-R #a8-594
    Opcode:0111 = ROR (Rm, Rdn)      T1-R #a8-570
    Opcode:1000 = TST (Rm, Rn)       T1-R #a8-746
    Opcode:1001 = RSB (Rn_2, Rd)     T1-I #a8-574
    Opcode:1010 = CMP (Rm, Rn)       T1-R #a8-372
    Opcode:1011 = CMN (Rm, Rn)       T1-R #a8-366
    Opcode:1100 = ORR (Rm, Rdn)      T1-R #a8-518
    Opcode:1101 = MUL (Rn_2, Rdm)    T1   #a8-502
    Opcode:1110 = BIC (Rm, Rdn)      T1-R #a8-342
    Opcode:1111 = MVN (Rm, Rd)       T1-R #a8-506
    """
    positions = {'Opcode': [6, 4]}
    ops = {'Rd':   (0, 3),
           'Rn':   (0, 3),
           'Rdn':  (0, 3),
           'Rdm':  (0, 3),
           'Rm':   (3, 3),
           'Rn_2': (3, 3)}


@instruction_decoder
class _special_data_instructions_branch_exchange():
    """
    Opcode:0000 =        ADD (DN, Rm, Rdn)    T2-R #a8-310
    Opcode:0001 | 001x = ADD (DN, Rm, Rdn)    T2-R #a8-310
    Opcode:01xx =        CMP (N, Rm, Rn)      T2-R #a8-372
    Opcode:1000 =        MOV (D, Rm, Rd)      T1-R #a8-486
    Opcode:1001 | 101x = MOV (D, Rm, Rd)      T1-R #a8-486
    Opcode:110x =        BX  (Rm)             T1   #a8-352 bits 0-2 must be 000
    Opcode:111x =        BLX (Rm)             T1   #a8-350 bits 0-2 must be 000
    """
    positions = {'Opcode': [6, 4]}
    ops = {'N':   (7, 1),
           'Rn':  (0, 3),
           'DN':  (7, 1),
           'Rdn': (0, 3),
           'Rd':  (0, 3),
           'D':   (7, 1),
           'Rm':  (3, 4)}


@instruction_decoder
class _load_store_single_data_item():
    """
    opA:0101
        opB:000 = STR   (Rm, Rn, Rt)     T1-R #a8-676
        opB:001 = STRH  (Rm, Rn, Rt)     T1-R #a8-702
        opB:010 = STRB  (Rm, Rn, Rt)     T1-R #a8-682
        opB:011 = LDRSB (Rm, Rn, Rt)     T1-R #a8-454
        opB:100 = LDR   (Rm, Rn, Rt)     T1-R #a8-412
        opB:101 = LDRH  (Rm, Rn, Rt)     T1-R #a8-446
        opB:110 = LDRB  (Rm, Rn, Rt)     T1-R #a8-422
        opB:111 = LDRSH (Rm, Rn, Rt)     T1-R #a8-462
    opA:0110
        opB:0xx = STR   (imm5, Rn, Rt)   T1-I #a8-672
        opB:1xx = LDR   (imm5, Rn, Rt)   T1-I #a8-406
    opA:0111
        opB:0xx = STRB  (imm5, Rn, Rt)   T1-I #a8-678
        opB:1xx = LDRB  (imm5, Rn, Rt)   T1-I #a8-416
    opA:1000
        opB:0xx = STRH  (imm5, Rn, Rt)   T1-I #a8-698
        opB:1xx = LDRH  (imm5, Rn, Rt)   T1-I #a8-440
    opA:1001
        opB:0xx = STR   (Rt, imm8)       T2-I #a8-672
        opB:1xx = LDR   (Rt, imm8)       T2-I #a8-406
    """
    positions = {'opB': [9,  3],
                 'opA': [12, 4]}
    ops = {'Rt_2': (8, 3),
           'imm5': (6, 5),
           'Rm':   (6, 3),
           'Rn':   (3, 3),
           'Rt':   (0, 3),
           'imm8': (0, 8)}

@instruction_decoder
class _misc_16bit_instructions():
    """
    Opcode:00000xx = ADD    (imm7)               T2-SPpI #a8-316
    Opcode:00001xx = SUB    (imm7)               T1-SPmI #a8-716
    Opcode:0001xxx = CBZ    (op, i, imm5, Rn)    T1      #a8-356
    Opcode:001000x = SXTH   (Rm, Rd)             T1      #a8-734
    Opcode:001001x = SXTB   (Rm, Rd)             T1      #a8-730
    Opcode:001010x = UXTH   (Rm, Rd)             T1      #a8-816
    Opcode:001011x = UXTB   (Rm, Rd)             T1      #a8-812
    Opcode:0011xxx = CBZ    (op, i, imm5, Rn)    T1      #a8-356
    Opcode:010xxxx = PUSH   (M, register_list)   T1      #a8-538
    Opcode:0110010 = SETEND (E)                  T1      #a8-604 bits 0-4 must be 1x000
    Opcode:0110011 = CPS    (im, A, I, F)        T1      #b9-1976 bit 3 must be 0
    Opcode:1001xxx = CBNZ   (op, i, imm5, Rn)    T1      #a8-356
    Opcode:101000x = REV    (Rm, Rd)             T1      #a8-562
    Opcode:101001x = REV16  (Rm, Rd)             T1      #a8-564
    Opcode:101011x = REVSH  (Rm, Rd)             T1      #a8-566
    Opcode:1011xxx = CBNZ   (op, i, imm5, Rn)    T1      #a8-356
    Opcode:110xxxx = POP    (P, register_list)   T1      #a8-534
    Opcode:1110xxx = BKPT   (imm8)               T1      #a8-346
    Opcode:1111xxx = _if_then_hints                      #a8-229
    """
    positions = {'Opcode': [5, 7]}
    ops = {'op':   (11, 1),
           'i':    (9,  1),
           'M':    (8,  1),
           'P':    (8,  1),
           'im':   (4,  1),
           'E':    (3,  1),
           'Rm':   (3,  3),
           'imm5': (3,  5),
           'A':    (2,  1),
           'I':    (1,  1),
           'F':    (0,  1),
           'Rd':   (0,  3),
           'Rn':   (0,  3),
           'imm7': (0,  7),
           'imm8': (0,  8),
           'register_list': (0,  8)}

@instruction_decoder
class _if_then_hints():
    """
    opB:!0000 =           IT    (firstcond, mask)    T1 #a8-390
    opA:0000 + opB:0000 = NOP   ()                   T1 #a8-510
    opA:0001 + opB:0000 = YIELD ()                   T1 #a8-1108
    opA:0010 + opB:0000 = WFE   ()                   T1 #a8-1104
    opA:0011 + opB:0000 = WFI   ()                   T1 #a8-1106
    opA:0100 + opB:0000 = SEV   ()                   T1 #a8-606
    """
    positions = {'opB': [0, 4],
                 'opA': [4, 4]}
    ops = {'firstcond': (4, 4),
           'mask':      (0, 4)}


@instruction_decoder
class _conditional_branch_supervisor_call():
    """
    Opcode:!111x = B   (cond, imm8)    T1 #a8-334
    Opcode:1110 =  UDF (imm8)          T1 #a8-758
    Opcode:1111 =  SVC (imm8)          T1 #a8-720
    """
    positions = {'Opcode': [8, 4]}
    ops = {'imm8': (0, 8),
           'cond': (8, 4)}
