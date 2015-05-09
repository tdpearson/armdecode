from Emulate.emulate import Emulate
from struct import unpack

emu = Emulate()
emu.registers.PC = 0x8000
emu.registers.R1 = emu.registers.R7 = 12
emu.process_mode.change_mode(emu.process_mode.SVC)
zimage_magic_num = 0x016F2818

kernelpath = r'/home/tdp/Downloads/kernel.img'
with open(kernelpath, 'rb') as f:
    f.seek(0x24)
    if unpack('<I', f.read(4))[0] == zimage_magic_num:
        #this is a zimage kernel image
        start_address = unpack('<I', f.read(4))[0]
        end_address = unpack('<I', f.read(4))[0]
        emu.memory.write_blob(f.read(), 0x8000)
    else:
        emu.memory.write_blob(f.read(), 0x8000)

emu.step(64, emu.execute)
#import Decode.arm_template as armtemp
#from Decode.arm_template import arm
#for cls in arm.classes:
#    print('---', cls, '---')
#    print(getattr(armtemp, cls).code_dict)
