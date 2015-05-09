#ArmDecode

__ArmDecode__ is a tool written entirely in **Python 3** to decode ARMv7 instructions / executables. 
This is currently pre-alpha software and is not feature complete.

##Decoding
This tool can be used to decode single instructions:

####Arm instruction example:
```python
from Decode.arm_template import arm
print(arm(0xc))
```
Returns:
```
{'Rm': 12, 'imm5': 0, 'Rn': 0, 'Rd': 0, 'instr': 'AND', 'type': 0, 'S': 0, 'encoding': 'A1-R'}
```

An example of getting the condition of an instruction:
```python
from Decode.utils import arm_condition
print(arm_condition(0xc))
```
Returns
```
'EQ'
```

####Thumb 16 instruction example:
```python
from Decode.t16_template import t16
print(t16(0xc))
```
Returns:
```
{'Rm': 1, 'imm5': 0, 'Rd': 4, 'instr': 'LSL', 'encoding': 'T1-I'}
```


##Emulating

####Example:
```python
from Emulate.emulate import Emulate
from struct import unpack

emu = Emulate()
emu.registers.PC = 0x8000
emu.registers.R1 = emu.registers.R7 = 12
emu.process_mode.change_mode(emu.process_mode.SVC)
zimage_magic_num = 0x016F2818

with open('kernel.img', 'rb') as f:
    f.seek(0x24)
    if unpack('<I', f.read(4))[0] == zimage_magic_num:
        emu.memory.write_blob(f.read(), 0x8000)
    else:
        f.seek(0)
        emu.memory.write_blob(f.read(), 0x8000)

emu.step(8, emu.execute)
```