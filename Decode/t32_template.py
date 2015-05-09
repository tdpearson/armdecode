__author__ = 'tdp'

from Decode.decoder_tools import instruction_decoder

default_encoding = "T2"


@instruction_decoder
class t32():
    """
    op1:01
        op2:00xx0xx =        _load_store_multiple
        op2:00xx1xx =        _load_store_dual_load_store_exclusive_table_branch
        op2:01xxxxx =        _data_processing_shifted_register
        op2:1xxxxxx =        _coprocessor_advanced_SIMD_floating_point_instructions
    op1:10
        op2:x0xxxxx + op:0 = _data_processing_modified_immediate
        op2:x1xxxxx + op:0 = _data_processing_plain_binary_immediate
        op:1                 _branches_misc_control
    op1:11
        op2:000xxx0 =        _store_single_data_item
        op2:00xx001 =        _load_byte_memory_hints
        op2:00xx011 =        _load_halfword_memory_hints
        op2:00xx101 =        _load_word
        op2:00xx111 =        UDF
        op2:001xxx0 =        _advanced_SIMD_element_structure_load_store_instructions
        op2:010xxxx =        _data_processing_register
        op2:0110xxx =        _multiply_multiply_accumulate_absolute_difference
        op2:0111xxx =        _long_multiply_long_multiply_accumulate_divide
        op2:1xxxxxx =        _coprocessor_advanced_SIMD_floating_point_intructions
    """
    positions = {'op1': 27,
                 'op2': 20,
                 'op': 15}


@instruction_decoder
class _load_store_multiple():
    """
    op:00
        L:0 =                 SRS   #b9-2002 T1 encoding DB - mask 110111000000000xxxxx
        L:1 =                 RFE   #b9-1998 T1 encoding DB - mask 1100000000000000
    op:01
        L:0 =                 STM   #a8-664  T2 encoding -    mask 0x0xxxxxxxxxxxxx
        L:1
            W:!1 | Rn:!1101 = LDM   #a8-396  T2 encoding -    mask 0xxxxxxxxxxxxx
            W:1 & Rn:1101 =   POP   #a8-534  T2 encoding -    mask 0xxxxxxxxxxxxx
    op:10
        L:0
            W:!1 | Rn:!1101 = STMDB #a8-668  T1 encoding -    mask 0x0xxxxxxxxxxxxx
            W:1 & Rn:1101 =   PUSH  #a8-538  T2 encoding -    mask 0x0xxxxxxxxxxxxx
        L:1 =                 LDMDB #a8-402  T1 encoding -    mask 0xxxxxxxxxxxxx
    op:11
        L:0 =                 SRS   #b9-2002 T2 encoding IA - mask 110111000000000xxxxx
        L:1 =                 RFE   #b9-1998 T2 encoding IA - mask 1100000000000000
    """
    positions = {'L': 20,
                 'Rn': 16,
                 'W': 21,
                 'op': 23}


@instruction_decoder
class _load_store_dual_load_store_exclusive_table_branch():
    """
    op1:00
        op2:00 =          STREX  #a8-690
        op2:01 =          LDREX  #a8-432 - mask 1111xxxxxxxx
    op1:0x + op2:10 =     STRD   #a8-686 immediate
    op1:1x + op2:x0 =     STRD   #a8-686 immediate
    Rn:!1111
        op1:0x + op2:11 = LDRD   #a8-426 immediate
        op1:1x + op2:x1 = LDRD   #a8-426 immediate
    Rn:1111
        op1:0x + op2:11 = LDRD   #a8-428 literal
        op1:1x + op2:x1 = LDRD   #a8-428 literal
    op1:01
        op2:00
            op3:0100 =    STREXB #a8-692 - mask 1111xxxxxxxx
            op3:0101 =    STREXH #a8-696 - mask 1111xxxxxxxx
            op3:0111 =    STREXD #a8-694
        op2:01
            op3:0000 =    TBB    #a8-736 - mask 11110000xxxxxxxx
            op3:0001 =    TBH    #a8-736 - mask 11110000xxxxxxxx
            op3:0100 =    LDREXB #a8-434 - mask 1111xxxx1111
            op3:0101 =    LDREXH #a8-438 - mask 1111xxxx1111
            op3:0111 =    LDREXD #a8-436 - mask 1111
    """
    positions = {'Rn': 16,
                 'op1': 23,
                 'op3': 4,
                 'op2': 20}


@instruction_decoder
class _data_processing_shifted_register():
    """
    op:0000
        Rd:!1111 | S:!1 = AND #a8-326
        Rd:1111 & S:1 =   TST #a8-746
    op:0001 =             BIC #a8-342
    op:0010
        Rn:!1111 =        ORR #a8-518
        Rn:1111 =         _move_register_immediate_shifts #a6-244
    op:0011
        Rn:!1111 =        ORN #a8-514
        Rn:1111 =         MVN #a8-506
    op:0100
        Rd:!1111 | S:!1 = EOR #a8-384
        Rd:1111 & S:1 =   TEQ #a8-740
    op:0110 =             PKH #a8-522
    op:1000
        Rd:!1111 | S:!1 = ADD #a8-310
        Rd:1111 & S:1 =   CMN #a8-366
    op:1010 =             ADC #a8-302
    op:1011 =             SBC #a8-594
    op:1101
        Rd:!1111 | S:!1 = SUB #a8-712
        Rd:1111 | S:1 =   CMP #a8-372
    op:1110 =             RSB #a8-576
    """
    positions = {'Rn': 16,
                 'S': 19,
                 'op': 21,
                 'Rd': 8}


@instruction_decoder
class _move_register_immediate_shifts():
    """
    type:00
        imm3:000 + imm2:00 =   MOV () #a8-486
        imm3:!000 | imm2:!00 = LSL () #a8-468 # TODO: confirm logic imm3:imm2 -> not 00000
    type:01 = LSR () #a8-472
    type:10 = ASR () #a8-330
    type:11
        imm3:000 + imm2:00 =   RRX () #a8-572
        imm3:!000 | imm2:!00 = ROR () #a8-568 # TODO: confirm logic imm3:imm2 -> not 00000
    """
    positions = {'type': 4,
                 'imm2': 6,
                 'imm3': 12}


@instruction_decoder
class _coprocessor_advanced_SIMD_floating_point_instructions(): #TODO: finish intruction decoding
    """
    op1:00000x = UDF
    op1:11xxxx = _advanced_SIMD_data_processing #a7-261
    coproc:!101x
        op1(0xxxx0 + !000x0x) = STC #a8-662
        op1(0xxxx1 + !000x0x)
            Rn:!1111 = LDC #a8-392 immediate
            Rn:1111 = LDC #a8-394 literal
        op1:000100 = MCRR #a8-478
        op1:000101 = MRRC #a8-494
        op1:10xxxx + op:0 = CDP #a8-358
        op1:10xxx0 + op:1 = MCR #a8-476
        op1:10xxx1 + op:1 = MRC #a8-492
    coproc:101x
        op1(0xxxxx + !000x0x) = _extension_register_load_store #a7-274
        op1:00010x = _64_bit_transfers_between_ARM_core_and_extension_registers #a7-279
        op1:10xxxx + op:0 = _floating_point_data_processing #a7-272
        op1:10xxxx + op:1 = _8_16_32_transfer_between_ARM_core_and_extension_registers #a7-278
    """
    positions = {'coproc': 8,
                 'op1': 20,
                 'op': 4,
                 'Rn': 16}


@instruction_decoder
class _advanced_SIMD_data_processing():
    """
    U:0 + A:1x11x + C:xxx0 = VEXT #a8-890
    U:1 + A:1x11x
        B:0xxx + C:xxx0 = _two_registers_misc #a7-267
        B:10xx + C:xxx0 = VTBL #a8-1094
        B:1100 + C:0xx0 = VDUP (scalar) #a8-884
    A:0xxxx = _three_registers_of_same_length #a7-262
    C:0xx1
        A:1x000 = _one_register_and_a_modified_immediate_value #a7-269
        A(1x001 | 1x01x | 1x1xx) = _two_registers_and_a_shift_amount #a7-266
    C:1xx1 + A:1xxxx = _two_registers_and_a_shift_amount #a7-266
    C:x0x0 + A(1x0xx | 1x10x) = _three_registers_of_different_lengths #a7-264
    C:x1x0 + A(1x0xx | 1x10x) = _two_registers_and_a_scalar #a7-265
    """
    positions = {'U': 28,
                 'A': 19,
                 'B': 8,
                 'C': 4}


@instruction_decoder
class _three_registers_of_same_length(): #TODO: determine how to decode "VORR" and "VMOV"
    """
    A:0000
        B:0 = VHADD #a8-896
        B:1 = VQADD #a8-996
    A:0001
        B:0 = VRHADD #a8-1030
        B:1
            U:0
                C:00 = VAND #a8-836 (register)
                C:01 = VBIC #a8-840 (register)
                C:10 = VORR | VMOV # "or" if source registers differ, "mov" if identical a8-976 / a8-938
                C:11 = VORN #a8-972
            U:1
                C:00 = VEOR #a8-888
                C:01 = VBSL #a8-842
                C:10 = VBIT #a8-842
                C:11 = VBIF #a8-842
    A:0010
        B:0 = VHSUB #a8-896
        B:1 = VQSUB #a8-1020
    A:0011
        B:0 = VCGT #a8-852 (register)
        B:1 = VCGE #a8-848 (register)
    A:0100
        B:0 = VSHL #a8-1048 (register)
        B:1 = VQSHL #a8-1014 (register)
    A:0101
        B:0 = VRSHL #a8-1032
        B:1 = VQRSHL #a8-1010
    A:0110 = VMAX | VMIN #a8-926 (integer)
    A:0111
        B:0 = VABD #a8-820
        B:1 = VABA #a8-818
    """
    positions = {'U': 28,
                 'A': 8,
                 'B': 4,
                 'C': 20}

@instruction_decoder
class _one_register_and_a_modified_immediate_value(): # Todo: add constant value code a7-269
    """
    op:0
        cmode:0xx0 = VMOV #a8-936
        cmode:0xx1 = VORR #a8-974
        cmode:10x0 = VMOV #a8-936
        cmode:10x1 = VORR #a8-974
        cmode:11xx = VMOV #a8-936
    op:1
        cmode:0xx0 = VMVN #a8-964
        cmode:0xx1 = VBIC #a8-838
        cmode:10x0 = VMVN #a8-964
        cmode:10x1 = VBIC #a8-838
        cmode:110x = VMVN #a8-964
        cmode:1110 = VMOV #a8-936
        cmode:1111 = UDF
    """
    positions = {'a': 28,
                 'b': 18,
                 'c': 17,
                 'd': 16,
                 'e': 3,
                 'f': 2,
                 'g': 1,
                 'h': 0,
                 'op': 5,
                 'cmode': 8}



@instruction_decoder
class _two_registers_and_a_shift_amount():
    """
    L:0 + imm3:000 = _one_register_and_a_modified_immediate_value #a7-269
    A:0000 = VSHR
    A:0001 = VSRA
    A:0010 = VRSHR
    A:0011 = VRSRA
    A:0100 + U:1 = VSRI
    A:0101
        U:0 = VSHL
        U:1 = VSLI
    A:011x = VQSHL
    A:1000 + L:0
        U:0
            B:0 = VSHRN
            B:1 = VRSHRN
        U:1
            B:0 = VQSHRN
            B:1 = VQRSHRN
    A:1001 + L:0
        B:0 = VQSHRN
        B:1 = VQRSHRN
    A:1010 + B:0 + L:0 = VSHLL | VMOVL
    A:111x + L:0 = VCVT
    """
    positions = {'A': 8,
                 'U': 28,
                 'B': 6,
                 'L': 7,
                 'imm3': 19}


@instruction_decoder
class _three_registers_of_different_lengths():
    pass


@instruction_decoder
class _two_registers_and_a_scalar():
    pass


@instruction_decoder
class _two_registers_misc():
    pass


@instruction_decoder
class _extension_register_load_store():
    pass


@instruction_decoder
class _64_bit_transfers_between_ARM_core_and_extension_registers():
    pass


@instruction_decoder
class _floating_point_data_processing():
    pass


@instruction_decoder
class _8_16_32_transfer_between_ARM_core_and_extension_registers():
    pass


@instruction_decoder
class _data_processing_modified_immediate():
    pass


@instruction_decoder
class _data_processing_plain_binary_immediate():
    pass


@instruction_decoder
class _branches_misc_control():
    pass


@instruction_decoder
class _change_processor_state_and_hints():
    pass


@instruction_decoder
class _misc_control_instructions():
    pass


@instruction_decoder
class _store_single_data_item():
    pass


@instruction_decoder
class _load_byte_memory_hints():
    pass


@instruction_decoder
class _load_halfword_memory_hints():
    pass


@instruction_decoder
class _load_word():
    pass


@instruction_decoder
class _advanced_SIMD_element_structure_load_store_instructions():
    pass


@instruction_decoder
class _data_processing_register():
    pass


@instruction_decoder
class _parallel_addition_and_subtraction_signed():
    pass


@instruction_decoder
class _parallel_addition_and_subtraction_unsigned():
    pass


@instruction_decoder
class _misc_operations():
    pass


@instruction_decoder
class _multiply_multiply_accumulate_absolute_difference():
    pass


@instruction_decoder
class _long_multiply_long_multiply_accumulate_divide():
    pass