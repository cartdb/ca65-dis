import sys
file = open(sys.argv[1], "rb")
file = file.read()
prgBanks = int.from_bytes(file[4:5])
chrBanks = int.from_bytes(file[5:6])
print("----------------" + sys.argv[1] + "----------------")
print("PRG ROM Size: " + str(prgBanks * 16384))
print("CHR ROM Size: " + str(chrBanks * 8192))
var = len(sys.argv[1])
length = 0
substr = ""
while length < var:
    substr = substr + "-"
    length += 1
print("----------------" + substr + "----------------")
prgCount = 0
chrCount = 0
header = open(sys.argv[1].replace(".nes", "") + "_HDR.bin", "wb")
header.write(file[0:16])
header.close()
while prgCount < prgBanks:
    if prgCount < 16:
        count = "0" + hex(prgCount).replace("0x", "")
    else:
        count = hex(prgCount).replace("0x", "")
    prg = open(sys.argv[1].replace(".nes", "") + "_PRG" + str(count) + ".bin", "wb")
    num = (prgCount * 16384) + 16
    prg.write(file[num:num + 16384])
    prg.close()
    prgCount += 1
while chrCount < chrBanks:
    if chrCount < 16:
        count = "0" + hex(chrCount).replace("0x", "")
    else:
        count = hex(chrCount).replace("0x", "")
    chr = open(sys.argv[1].replace(".nes", "") + "_CHR" + str(count) + ".bin", "wb")
    num = (prgCount * 16384) + 16 + (chrCount * 8192)
    chr.write(file[num:num + 8192])
    chr.close()
    chrCount += 1