import sys
import os
import zlib
import pathlib
os.system("del *.bin")
os.system("del a.out")
os.system("del *.asm")
os.system("del *.o")
os.system("del output.cdl")
if sys.argv[1].endswith(".nes") == False:
    print("Only .NES files are supported!")
    sys.exit()
check = open(sys.argv[1], "rb")
check = check.read()
if check[0:4] != b"NES\x1a":
    print(check[0:4])
    print("Not a valid INES header!")
    sys.exit()
prgBanks = int.from_bytes(check[4:5])
chrBanks = int.from_bytes(check[5:6])
expectedSize = 16 + (prgBanks * 16384) + (chrBanks * 8192)
if os.path.getsize(sys.argv[1]) != expectedSize:
    print("Expected Size: " + str(expectedSize))
    print("Actual Size: " + str(os.path.getsize(sys.argv[1])))
    print("Invalid NES file!")
    sys.exit()
os.system('python nessplitter.py "' + sys.argv[1] + '"')
os.system('python cdlsplit.py "' + sys.argv[1].replace(".nes", ".cdl") + '"')
question = input("Continue? ")
while question != "yes" and question != "no":
    question = input("Continue? ")
if question == "yes":
    bank = input("PRG Bank: ")
    while os.path.isfile(bank) == False or os.path.getsize(bank) != 16384:
        bank = input("PRG Bank: ")
    os.system('da65 --comments 3 --cpu 6502 -o "' + bank.replace(".bin", ".asm") + '" "' + bank + '"')
    os.system('ca65 "' + bank.replace(".bin", ".asm") + '"')
    os.system('ld65 -C nes.cfg "' + bank.replace(".bin", ".o") + '"')
    hash1 = open(bank, "rb")
    hash1 = hash1.read()
    hash1 = hex(zlib.crc32(hash1)).replace("0x", "")
    hash2 = open("a.out", "rb")
    hash2 = hash2.read()
    hash2 = hex(zlib.crc32(hash2)).replace("0x", "")
    if hash1 != hash2:
        print(hash1)
        print(hash2)
        sys.exit()
elif question == "no":
    sys.exit()
file = open(bank.replace(".bin", ".asm"), "r")
labels = ["C000"]
while True:
    line = file.readline()
    if not line:
        break
    if ":" in line and "L" in line and ":=" not in line and "a:" not in line and "LC000" not in line:
        labels.append(line.split(": ")[0].replace("L", ""))
file.close()
codeANDdata = []
unused = []
code = []
data = []
bytesArr = []
count = 49152
for byte in pathlib.Path("cdl" + bank).read_bytes():
    for label in range(len(labels)):
        if byte&2**0 != 0 and byte&2**1 != 0 and int(labels[label], 16) == count:
            codeANDdata.append(hex(count).replace("0x", ""))
            break
        elif byte&2**0 == 0 and byte&2**1 == 0 and int(labels[label], 16) == count:
            unused.append(hex(count).replace("0x", ""))
            break
        elif byte&2**0 != 0 and int(labels[label], 16) == count:
            code.append(hex(count).replace("0x", ""))
            break
        elif byte&2**1 != 0 and int(labels[label], 16) == count:
            data.append(hex(count).replace("0x", ""))
            break
    bytesArr.append(byte)
    count += 1
num = []
for addr in range(len(unused)):
    for label in range(len(labels)):
        if int(unused[addr], 16) == int(labels[label], 16):
            num.append(label)
            break
for addr in range(len(codeANDdata)):
    for label in range(len(labels)):
        if int(codeANDdata[addr], 16) == int(labels[label], 16):
            num.append(label)
            break
for label in range(len(num)):
    count = int(labels[num[label]], 16) - 49152
    while count < int(labels[num[label] + 1], 16) - 49152:
        if bytesArr[count]&2**0 != 0 and bytesArr[count]&2**1 == 0:
            code.append(hex(int(labels[num[label]], 16)).replace("0x", ""))
            break
        elif bytesArr[count]&2**1 != 0 and bytesArr[count]&2**0 == 0:
            data.append(hex(int(labels[num[label]], 16)).replace("0x", ""))
            break
        count += 1
        if count == int(labels[num[label] + 1], 16) - 49152:
            print(labels[num[label]] + " cannot be determined!")
            sys.exit()
for addr in range(len(code)):
    code[addr] = int(code[addr], 16)
for addr in range(len(data)):
    data[addr] = int(data[addr], 16)
code = sorted(code)
data = sorted(data)
for addr in range(len(code)):
    code[addr] = hex(code[addr]).replace("0x", "")
for addr in range(len(data)):
    data[addr] = hex(data[addr]).replace("0x", "")
codeS = []
codeE = []
dataS = []
dataE = []
flag = ""
count = 49152
while count < 65536:
    for label in range(len(labels)):
        if count == int(labels[label], 16):
            for addr in range(len(code)):
                if int(labels[label], 16) == int(code[addr], 16):
                    if flag == "data":
                        dataE.append(hex(int(code[addr], 16) - 1).replace("0x", ""))
                    if flag != "code":
                        codeS.append(code[addr])
                    flag = "code"
            for addr in range(len(data)):
                if int(labels[label], 16) == int(data[addr], 16):
                    if flag == "code":
                        codeE.append(hex(int(data[addr], 16) - 1).replace("0x", ""))
                    if flag != "data":
                        dataS.append(data[addr])
                    flag = "data"
    count += 1
if flag == "data":
    dataE.append("ffff")
elif flag == "code":
    codeE.append("ffff")
for addr in range(len(codeS)):
    print("CODE: $" + codeS[addr] + "-$" + codeE[addr])
for addr in range(len(dataS)):
    print("DATA: $" + dataS[addr] + "-$" + dataE[addr])
file = open("output.cdl", "wb")
count = 49152
bytesArr = []
while count < 65536:
    for addr in range(len(codeS)):
        if count >= int(codeS[addr], 16) and count <= int(codeE[addr], 16):
            bytesArr.append(1)
            break
    for addr in range(len(dataS)):
        if count >= int(dataS[addr], 16) and count <= int(dataE[addr], 16):
            bytesArr.append(2)
            break
    count += 1
file.write(bytearray(bytesArr))
file.close()
os.system('python project.py "' + bank.replace(".bin", ".asm") + '"')