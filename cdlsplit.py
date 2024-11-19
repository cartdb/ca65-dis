import sys
import os
import pathlib
rom = open(sys.argv[1].replace(".cdl", ".nes"), "rb")
rom = rom.read()
prgBanks = int.from_bytes(rom[4:5])
chrBanks = int.from_bytes(rom[5:6])
romSize = prgBanks * 16384
file = open(sys.argv[1], "rb")
codeANDdata = 0
code = 0
data = 0
unused = 0
count = 0
for byte in pathlib.Path(sys.argv[1]).read_bytes():
    if byte&2**0 != 0 and byte&2**1 != 0:
        codeANDdata += 1
        code += 1
        data += 1
    elif byte&2**0 == 0 and byte&2**1 == 0:
        unused += 1
    elif byte&2**0 != 0:
        code += 1
    elif byte&2**1 != 0:
        data += 1
    count += 1
    if count >= romSize:
        break
codeANDdata = "ROM logged as both code and data: " + str((codeANDdata / romSize) * 100) + "% - " + hex(codeANDdata)
code = "ROM logged as code: " + str((code / romSize) * 100) + "% - " + hex(code)
data = "ROM logged as data: " + str((data / romSize) * 100) + "% - " + hex(data)
unused = "ROM unused: " + str((unused / romSize) * 100) + "% - " + hex(unused)
print("----------------" + sys.argv[1] + "----------------")
print(codeANDdata)
print(code)
print(data)
print(unused)
var = len(sys.argv[1])
length = 0
substr = ""
while length < var:
    substr = substr + "-"
    length += 1
print("----------------" + substr + "----------------")
file = file.read()
prgCount = 0
chrCount = 0
while prgCount < prgBanks:
    if prgCount < 16:
        count = "0" + hex(prgCount).replace("0x", "")
    else:
        count = hex(prgCount).replace("0x", "")
    prg = open("cdl" + sys.argv[1].replace(".cdl", "") + "_PRG" + str(count) + ".bin", "wb")
    num = prgCount * 16384
    prg.write(file[num:num + 16384])
    prg.close()
    romSize = os.path.getsize("cdl" + sys.argv[1].replace(".cdl", "") + "_PRG" + str(count) + ".bin")
    codeANDdata = 0
    code = 0
    data = 0
    unused = 0
    for byte in pathlib.Path("cdl" + sys.argv[1].replace(".cdl", "") + "_PRG" + str(count) + ".bin").read_bytes():
        if byte&2**0 != 0 and byte&2**1 != 0:
            codeANDdata += 1
            code += 1
            data += 1
        elif byte&2**0 == 0 and byte&2**1 == 0:
            unused += 1
        elif byte&2**0 != 0:
            code += 1
        elif byte&2**1 != 0:
            data += 1
    codeANDdata = "ROM logged as both code and data: " + str((codeANDdata / romSize) * 100) + "% - " + hex(codeANDdata)
    code = "ROM logged as code: " + str((code / romSize) * 100) + "% - " + hex(code)
    data = "ROM logged as data: " + str((data / romSize) * 100) + "% - " + hex(data)
    unused = "ROM unused: " + str((unused / romSize) * 100) + "% - " + hex(unused)
    print("----------------" + "cdl" + sys.argv[1].replace(".cdl", "") + "_PRG" + str(count) + ".bin" + "----------------")
    print(codeANDdata)
    print(code)
    print(data)
    print(unused)
    var = len("cdl" + sys.argv[1].replace(".cdl", "") + "_PRG" + str(count) + ".bin")
    length = 0
    substr = ""
    while length < var:
        substr = substr + "-"
        length += 1
    print("----------------" + substr + "----------------")
    prgCount += 1
while chrCount < chrBanks:
    if chrCount < 16:
        count = "0" + hex(chrCount).replace("0x", "")
    else:
        count = hex(chrCount).replace("0x", "")
    chr = open("cdl" + sys.argv[1].replace(".cdl", "") + "_CHR" + str(count) + ".bin", "wb")
    num = (prgCount * 16384) + (chrCount * 8192)
    chr.write(file[num:num + 8192])
    chr.close()
    romSize = os.path.getsize("cdl" + sys.argv[1].replace(".cdl", "") + "_CHR" + str(count) + ".bin")
    codeANDdata = 0
    code = 0
    data = 0
    unused = 0
    for byte in pathlib.Path("cdl" + sys.argv[1].replace(".cdl", "") + "_CHR" + str(count) + ".bin").read_bytes():
        if byte&2**0 != 0 and byte&2**1 != 0:
            codeANDdata += 1
            code += 1
            data += 1
        elif byte&2**0 == 0 and byte&2**1 == 0:
            unused += 1
        elif byte&2**0 != 0:
            code += 1
        elif byte&2**1 != 0:
            data += 1
    codeANDdata = "ROM logged as both code and data: " + str((codeANDdata / romSize) * 100) + "% - " + hex(codeANDdata)
    code = "ROM logged as code: " + str((code / romSize) * 100) + "% - " + hex(code)
    data = "ROM logged as data: " + str((data / romSize) * 100) + "% - " + hex(data)
    unused = "ROM unused: " + str((unused / romSize) * 100) + "% - " + hex(unused)
    print("----------------" + "cdl" + sys.argv[1].replace(".cdl", "") + "_CHR" + str(count) + ".bin" + "----------------")
    print(codeANDdata)
    print(code)
    print(data)
    print(unused)
    var = len("cdl" + sys.argv[1].replace(".cdl", "") + "_CHR" + str(count) + ".bin")
    length = 0
    substr = ""
    while length < var:
        substr = substr + "-"
        length += 1
    print("----------------" + substr + "----------------")
    chrCount += 1