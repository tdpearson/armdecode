from importlib import import_module

_modules = ['branching', 'data_processing']

class Execute(object):
    def __init__(self, registers, process_mode, memory):
        self.instruction = {}

        for module_name in _modules:
            mod = import_module("Execute." + module_name)
            for cls in [obj for obj in mod.__dict__ if type(mod.__dict__[obj]) == type]:
                cls_instance = mod.__dict__[cls](registers, process_mode, memory)
                for cls_instr in [func for func in mod.__dict__[cls].__dict__ if not func.startswith('_')]:
                    try:
                        self.instruction[cls_instr]
                    except KeyError:
                        self.instruction[cls_instr] = cls_instance[cls_instr]
                    else:
                        raise Warning('Multiple instruction handlers detected for "%s"' % cls_instr)

    def __call__(self, args):
        try:
            self.instruction[args['instr']](args)
        except (KeyError, NotImplementedError):
            print('unhandled: %s - %s' % (args['instr'], args['encoding']))