__author__ = 'tdp'

import re
import shlex
from inspect import cleandoc
from sys import modules
from functools import reduce
from itertools import product
from operator import or_


class instruction_decoder(object):
    classes = {}  # this is used for the lexer to test for class tokens
    def __init__(self, cls):
        self.name = cls.__name__
        self.template = cleandoc(cls.__doc__)
        self.positions = getattr(cls, 'positions', None)
        self.ops = getattr(cls, 'ops', None)
        self._code = None
        self._code_dict = None
        self._bytecode = None
        self.positions_mask = positionMask(cls.positions) if cls.positions else None
        #self._dict = {}
        self.module = modules[cls.__module__]

        try:
            instruction_decoder.classes[self.name]
        except KeyError:
            instruction_decoder.classes[self.name] = cls

        # Make modified classes visible to __call__
        #setattr(self.module, self.name, self)
        globals()[self.name] = self

    def __getattr__(self, name):
        def code_gen(call_class):
            return parse_template(template_text=self.template,
                                  positions=self.positions,
                                  ops=self.ops,
                                  default_encoding=self.module.default_encoding,
                                  call_class=call_class)
        if name == 'code':
            if self._code:  # only generate code once then reuse
                return self._code
            self._code = code_gen(True)
            return self._code
        elif name == 'code_dict':
            # FIXME: This section needs to be rewritten - this will go towards enabling decoding using lookup dicts
            if self._code_dict:  # only generate code once then reuse
                return self._code_dict
            self._code_dict = code_gen(False)
            return self._code_dict
        else:
            return instruction_decoder.__getattribute__(self, name)

    def __call__(self, val):
        """
        def func(val):
            <generated source code>
        modified_val = func(val) <-- make return accessible as variable
        """
        globals()['val'] = val
        if not self._bytecode:
            func_code = "def func(val):\n%s\nmodified_val = func(val)" % indent_code(self.code)
            self._bytecode = compile(func_code, '<string>', 'exec')
        exec(self._bytecode, globals())
        return modified_val  # this is set by the above exec


def is_decoder_class(text):
    return text in instruction_decoder.classes.keys()


def _gen_op_mask(positions):
    def mask(length):
        return (1 << length) - 1

    val = 0
    for position in positions.values():
        val = val | (mask(position[1]) << position[0])

    return val


def parse_template(template_text, **kwargs):
    text = ''
    for line in template_text.split('\n'):
        try:
            text += parse_line(line, **kwargs) + '\n'
        except TypeError:
            pass
    return text


def parse_line(line, **kwargs):
    positions = kwargs.get('positions')
    ops = kwargs.get('ops')
    default_encoding = kwargs.get('default_encoding')
    call_class = kwargs.get('call_class')
    text = ''
    position = ''
    returns_value = False
    tokens = tokenize(line)
    for token in tokens:
        if is_logic_token(token):
            text += ' %s ' % token.replace('+', '&')
            continue
        if positions and token in positions and not returns_value:  # prevent collisions between positions and ops
            position = positions[token][0]
            continue
        if is_mask_template(token):
            num = create_number_from_template(token, position)
            mask = create_mask_from_template(token, position)
            equ = get_mask_equality(token)
            text += '(val & %s %s %s)' % (mask, equ, num)
            continue
        if token == '=':
            returns_value = True
            text += ': return '
            token = tokens.__next__()
            # token following '=' is either a class or an instruction
            if is_decoder_class(token):
                if call_class:
                    text += '%s(val)' % token
                    continue
                else:
                    text += token
                    continue
            else:
                text += "({'instr': '%s' " % token
                continue
        if token == "(":
            continue
        if ops and token in ops:
            shift = ops[token][0]
            shift_text = ", '%s': val & %s" % (token, get_mask_by_size(ops[token][1]))  # if no shift
            if shift:
                shift_text = ", '%s': val >> %s & %s" % (token, shift, get_mask_by_size(ops[token][1]))
            text += shift_text
            while True:
                try:
                    token = tokens.__next__()
                    text += ", '%s': val >> %s & %s" % (token, ops[token][0], get_mask_by_size(ops[token][1]))
                except KeyError:
                    break
        if token == ")":
            try:
                token = tokens.__next__()
                if is_encoding_type_token(token):
                    text += ", 'encoding': '%s'" % token
            except StopIteration:
                text += ", 'encoding': '%s'" % default_encoding
                pass
            text += "})"
    if text:
        text = '%sif %s' % (get_indentation(line), text)
        if not returns_value: text += ':'
        return text


def create_mask_from_template(val, position=0):
    tmp = re.sub(r'^!', '', val)
    tmp = re.sub(r'[10]', '1', tmp)
    return int('0b' + re.sub(r'x', '0', tmp, flags=re.IGNORECASE), 2) << position


def create_number_from_template(val, position=0):
    tmp = re.sub(r'^!', '', val)
    return int('0b' + re.sub(r'x', '0', tmp, flags=re.IGNORECASE), 2) << position


def tokenize(text):
    lexer = shlex.shlex(text)
    lexer.whitespace += ',:'
    lexer.wordchars += '!-'
    yield from lexer


def get_mask_equality(text):
    if text[0] == '!':
        return '!='
    return '=='


def is_mask_template(text):
    return re.match(r'^!?[01x]*', text, flags=re.IGNORECASE).group() != ''


def is_logic_token(text):
    return re.match(r'[+|]?', text).group() != ''


def is_encoding_type_token(text):
    return re.match(r'[AT][1234][-EILMPRS]*', text, flags=re.IGNORECASE).group() != ''


def get_indentation(text):
    return re.match(r'^[ \t]*', text).group()


def get_mask_by_size(size):
    return (1 << size) - 1


def indent_code(text, count=4):
    indention = " " * count
    return indention + re.sub(r'\n', '\n%s' % indention, text)


# The following two functions are to go towards enabling decoding using lookup dicts
def positionMask(positions):
    """ Generate mask to look at positional decoding parameters """
    return reduce(or_, [((1 << size) - 1) << pos for pos, size in positions.values()])


def decoderMasks(positions):
    """ Generate list of masks using position values from instruction_decoder templates """
    partialMasks = [[val << pos for val in range(1 << size)] for pos, size in positions.values()]
    return [reduce(or_, partialMask) for partialMask in product(*partialMasks)]
