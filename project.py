import os
import sys
import pathlib
if os.path.isfile("output.cdl") == False:
    print("Error: output.cdl does not exist.")
    sys.exit()
if os.path.isfile(sys.argv[1]) == False:
    print("Error: " + sys.argv[1] +  " does not exist.")
    sys.exit()
code = []
codeEND = []
data = []
dataEND = []
count = 65536 - os.path.getsize("output.cdl")
for byte in pathlib.Path("output.cdl").read_bytes():
    if byte&2**0 != 0 and byte&2**1 == 0:
        code.append(hex(count).replace("0x", ""))
    elif byte&2**1 != 0 and byte&2**0 == 0:
        data.append(hex(count).replace("0x", ""))
    count += 1
file = open(sys.argv[1], "r")
flag = False
linesArr = []
while True:
    line = file.readline()
    if not line:
        break
    code = line
    if "; C000" in line:
        flag = True
    if flag == True and ";" in line and "-" not in line:
        if ":" in line and "L" in line and ":=" not in line and "a:" not in line:
            dataByte = line.split()[0] + "  .byte "
        else:
            dataByte = "        .byte "
        for entry in range(len(line.split(";")[1].split())):
            if entry != 0 and entry != len(line.split(";")[1].split()) - 1:
                dataByte = dataByte + "$" + line.split(";")[1].split()[entry] + ", "
            elif entry != 0 and entry == len(line.split(";")[1].split()) - 1:
               dataByte = dataByte + "$" + line.split(";")[1].split()[entry]
        while len(dataByte) != 48:
            dataByte = dataByte + " "
        dataByte = dataByte + ";" + line.split(";")[1]
        line = line.split(";")[1].split()[0]
        for addr in range(len(data)):
            if int(data[addr], 16) == int(line, 16):
                code = dataByte
    linesArr.append(code)
file.close()
file = open(sys.argv[1], "w")
for line in range(len(linesArr)):
    file.write(linesArr[line])
file.close()