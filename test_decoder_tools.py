__author__ = 'tdp'

import unittest

from Decode.decoder_tools import *
from Decode.t16_template import t16
#from t32_template import t32
#from arm_template import arm

class test_tools(unittest.TestCase):

    def setUp(self):
        pass

    def test_mask_from_template(self):
        self.assertEqual(create_mask_from_template('01x', 0), 0b110)
        self.assertEqual(create_mask_from_template('01x', 1), 0b1100)
        self.assertEqual(create_mask_from_template('01x', 2), 0b11000)
        self.assertEqual(create_mask_from_template('xxx'), 0b000)
        self.assertEqual(create_mask_from_template('XXX'), 0b000)
        self.assertEqual(create_mask_from_template('000'), 0b111)
        self.assertEqual(create_mask_from_template('111'), 0b111)
        self.assertEqual(create_mask_from_template('!111'), 0b111)
        self.assertEqual(create_mask_from_template('!000'), 0b111)
        self.assertEqual(create_mask_from_template('!xxx'), 0b000)
        self.assertRaises(ValueError, create_mask_from_template, '01x', -1)
        self.assertRaises(ValueError, create_mask_from_template, '!!01x')

    def test_number_from_template(self):
        self.assertEqual(create_number_from_template('01x', 0), 0b010)
        self.assertEqual(create_number_from_template('01x', 1), 0b0100)
        self.assertEqual(create_number_from_template('01x', 2), 0b01000)
        self.assertEqual(create_number_from_template('xxx'), 0b000)
        self.assertEqual(create_number_from_template('XXX'), 0b000)
        self.assertEqual(create_number_from_template('000'), 0b000)
        self.assertEqual(create_number_from_template('111'), 0b111)
        self.assertEqual(create_number_from_template('!111'), 0b111)
        self.assertEqual(create_number_from_template('!000'), 0b000)
        self.assertEqual(create_number_from_template('!xxx'), 0b000)
        self.assertRaises(ValueError, create_number_from_template, '01x', -1)
        self.assertRaises(ValueError, create_number_from_template, '!!01x')

    def test_mask_equality(self):
        self.assertEqual(get_mask_equality('!xxx'), '!=')
        self.assertEqual(get_mask_equality('xxx'), '==')

    def test_is_mask_template(self):
        self.assertTrue(is_mask_template('00x'))
        self.assertTrue(is_mask_template('xxx'))
        self.assertTrue(is_mask_template('XXX'))
        self.assertTrue(is_mask_template('11x'))
        self.assertTrue(is_mask_template('000'))
        self.assertTrue(is_mask_template('111'))
        self.assertTrue(is_mask_template('!00x'))
        self.assertTrue(is_mask_template('!xxx'))
        self.assertTrue(is_mask_template('!11x'))
        self.assertTrue(is_mask_template('!000'))
        self.assertTrue(is_mask_template('!111'))
        self.assertFalse(is_mask_template('abc'))
        #self.assertFalse(is_mask_template('!!000'))

    def test_is_logic_token(self):
        self.assertTrue(is_logic_token('+'))
        self.assertTrue(is_logic_token('|'))

    def test_indentation(self):
        self.assertEqual(get_indentation(' ' * 8), ' ' * 8)
        self.assertEqual(get_indentation('\t' * 8), '\t' * 8)
        self.assertEqual(get_indentation('    '), '    ')
        self.assertEqual(get_indentation('\t'), '\t')
        self.assertEqual(get_indentation(' \t'), ' \t')

    def test_mask_by_size(self):
        self.assertEqual(get_mask_by_size(2), 3)
        self.assertEqual(get_mask_by_size(3), 7)
        self.assertEqual(get_mask_by_size(4), 15)
        self.assertEqual(get_mask_by_size(5), 31)
        self.assertEqual(get_mask_by_size(6), 63)
        self.assertEqual(get_mask_by_size(7), 127)
        self.assertEqual(get_mask_by_size(8), 255)

    #def test_shifted_mask(self):
    #    self.assertEqual(shifted_mask((0, 4)), 0b1111)
    #    self.assertEqual(shifted_mask((1, 4)), 0b11110)
    #    self.assertEqual(shifted_mask((2, 4)), 0b111100)
    #    self.assertRaises(ValueError, shifted_mask, (-1, 4))

    def test_indent_code(self):
        self.assertEqual(indent_code('test'), '    test')
        self.assertEqual(indent_code('test', 2), '  test')
        self.assertEqual(indent_code('test', 8), '        test')


class test_parser(unittest.TestCase):

    def setUp(self):
        pass

    def test_t16_shift_add_subtract_move_compare(self):
        self.assertEqual(t16(0b0000000000000000)['instr'], 'LSL')
        self.assertEqual(t16(0b0000100000000000)['instr'], 'LSR')
        self.assertEqual(t16(0b0001000000000000)['instr'], 'ASR')
        self.assertEqual(t16(0b0001100000000000)['instr'], 'ADD')
        self.assertEqual(t16(0b0001101000000000)['instr'], 'SUB')
        self.assertEqual(t16(0b0001110000000000)['instr'], 'ADD')
        self.assertEqual(t16(0b0001111000000000)['instr'], 'SUB')
        self.assertEqual(t16(0b0010000000000000)['instr'], 'MOV')
        self.assertEqual(t16(0b0010100000000000)['instr'], 'CMP')
        self.assertEqual(t16(0b0011000000000000)['instr'], 'ADD')
        self.assertEqual(t16(0b0011100000000000)['instr'], 'SUB')

    def test_t16_data_processing(self):
        self.assertEqual(t16(0b0100000000000000)['instr'], 'AND')
        self.assertEqual(t16(0b0100000001000000)['instr'], 'EOR')
        self.assertEqual(t16(0b0100000010000000)['instr'], 'LSL')
        self.assertEqual(t16(0b0100000011000000)['instr'], 'LSR')
        self.assertEqual(t16(0b0100000100000000)['instr'], 'ASR')
        self.assertEqual(t16(0b0100000101000000)['instr'], 'ADC')
        self.assertEqual(t16(0b0100000110000000)['instr'], 'SBC')
        self.assertEqual(t16(0b0100000111000000)['instr'], 'ROR')
        self.assertEqual(t16(0b0100001000000000)['instr'], 'TST')
        self.assertEqual(t16(0b0100001001000000)['instr'], 'RSB')
        self.assertEqual(t16(0b0100001010000000)['instr'], 'CMP')
        self.assertEqual(t16(0b0100001011000000)['instr'], 'CMN')
        self.assertEqual(t16(0b0100001100000000)['instr'], 'ORR')
        self.assertEqual(t16(0b0100001101000000)['instr'], 'MUL')
        self.assertEqual(t16(0b0100001110000000)['instr'], 'BIC')
        self.assertEqual(t16(0b0100001111000000)['instr'], 'MVN')

    def test_16_special_data_instructions_branch_exchange(self):
        self.assertEqual(t16(0b0100010000000000)['instr'], 'ADD')
        self.assertEqual(t16(0b0100010001000000)['instr'], 'ADD')
        self.assertEqual(t16(0b0100010010000000)['instr'], 'ADD')
        self.assertEqual(t16(0b0100010100000000)['instr'], 'CMP')
        self.assertEqual(t16(0b0100011000000000)['instr'], 'MOV')
        self.assertEqual(t16(0b0100011001000000)['instr'], 'MOV')
        self.assertEqual(t16(0b0100011010000000)['instr'], 'MOV')
        self.assertEqual(t16(0b0100011100000000)['instr'], 'BX')
        self.assertEqual(t16(0b0100011110000000)['instr'], 'BLX')
