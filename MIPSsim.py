"this function is used to process self-defined mips instructions. something can be improve: some instructions are the same structure, so they can be process by one function"
import os
import string
from collections import OrderedDict

Cycle = 0 #count turn of simulation
Pclist = [] # store the begin address of value and end of value and the cycle number and the pc now is excuted
Pclist.append(Cycle)
InfoDIc = OrderedDict() #Dictionary of infolist
ValueDic = OrderedDict() #list contains address pc and the value
RigsterDic = OrderedDict() #list contains register and their contained data
ActionDic = OrderedDict() #list contains informations each simulate need
SimulationDic = OrderedDict() # list store simulations should be output
#initialize rigister dictionary
initial = 0
while initial < 32:
    RigsterDic["R" + str(initial)] = 0
    initial += 1

def GetFile():
    "this function is used to get source file. return: List of each line"
    try:
        _sourcefilepath = "C:/Users/Hanyue Zheng/PycharmProjects/ComputerStructureproj1/"
        _sourcefilename = raw_input("Please enter sourcefile name: ")
        filelineArr = []
        f = open(_sourcefilepath + _sourcefilename, "r")
        for eachline in f:
            filelineArr.append(eachline.replace('\n', ''))
        return filelineArr
    except IOError, e:
        print "file open error: ", e

def twototen(targetaddress):
    "this function used to change decimal to number"
    position = 0
    addressnum = 0
    while position < len(targetaddress):
        if targetaddress[position] == "1":
            addressnum += 2 ** (len(targetaddress) - position - 1)
        position += 1
    return addressnum

def tentotwo(num):
    "this function used to change number to decimal"
    la = []
    if num < 0:
        versestr = ""
        element = tentotwo(abs(num))
        for item in element:
            if item == "1":
                item = 0
            elif item == "0":
                item = 1
            versestr += str(item)
        loriginal = list(versestr)
        index = len(loriginal - 1)
        while index > 0:
            if loriginal[index] == "0":
                loriginal[index] == "1"
                break
            else:
                loriginal[index] == "0"
            index -= 1
        versestr = "".join((loriginal))
        return versestr
    str1 = ""
    while True:
        num, remainder = divmod(num, 2)
        la.append(str(remainder))
        if num == 0:
            print  "lengrh:" ,len(la)
            length = len(la)
            if length < 32:
                for i in range(32 - length):
                    str1 += "0"
                for item in reversed(la):
                    str1 += item
            return str1

def CountMinusnum(element):
    "this function is used to change minus decimal to number "
    versestr = ""
    for item in element:
        if item == "1":
            item = 0
        elif item == "0":
            item = 1
        versestr += str(item)
    index = len(versestr) - 1
    lversestr = list(versestr)
    while index >  0:
        if versestr[index] == "0":
            lversestr[index] = "1"
            break
        else:
            lversestr[index] = "0"
        index -= 1
    if index == 0:
        return 0
    versestr = "".join(lversestr)
    return twototen(versestr)

def JInstr(element, pcindex):
    "this function process 01's string which represent J instruction, return a list which contains all the info need to be print"
    targetaddress = element[6: ] + "00"  # 2 offset
    addressnum = twototen(targetaddress)
    infolist = [] # list need to be return
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("J")
    infolist.append("#" + str(addressnum))
    InfoDIc[pcindex] = infolist

def JRInstr(element, pcindex):
    "this function process 01's string which represent JR instruction, return a list which contains all the info need to be print"
    rs = element[6: 10]
    addressnum = twototen(rs)
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("JR")
    infolist.append("R" + str(addressnum))
    InfoDIc[pcindex] = infolist

def BEQInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    offset = twototen(element[16: 32] + "00")
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("BEQ")
    infolist.append("R" + str(rs))
    infolist.append("R" + str(rt))
    infolist.append("#" + str(offset))
    InfoDIc[pcindex] = infolist

def BLTZInstr(element, pcindex):
    rs = twototen(element[6: 11])
    offset = twototen(element[16:32] + "00")
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("BLTZ")
    infolist.append("R" + str(rs))
    infolist.append("#" + str(offset))
    InfoDIc[pcindex] = infolist

def BGTZInstr(element, pcindex):
    rs = twototen(element[6: 11])
    offset = twototen(element[16:32] + "00")
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("BGTZ")
    infolist.append("R" + str(rs))
    infolist.append("#" + str(offset))
    InfoDIc[pcindex] = infolist

def BREAKInstr(element, pcindex):
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("BREAK")
    InfoDIc[pcindex] = infolist

def SWInstr(element, pcindex):
    rt = twototen(element[11: 16])
    base = twototen(element[6: 11])
    offset = twototen(element[16: 32])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("SW")
    infolist.append("R" + str(rt))
    infolist.append(str(offset) + "(R" + str(base) + ")")
    InfoDIc[pcindex] = infolist

def LWInstr(element, pcindex):
    base = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    offset = twototen(element[16: 32])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("LW")
    infolist.append("R" + str(rt))
    infolist.append(str(offset) + "(R" + str(base) + ")")
    InfoDIc[pcindex] = infolist

def SLLInstr(element, pcindex):
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    sa = twototen(element[21: 26])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("SLL")
    infolist.append("R" + str(rd))
    infolist.append("R" + str(rt))
    infolist.append("#" + str(sa))
    InfoDIc[pcindex] = infolist

def SRLInstr(element, pcindex):
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    sa = twototen(element[21: 26])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("SRL")
    infolist.append("R" + str(rt))
    infolist.append("R" + str(rd))
    infolist.append("#" + str(sa))
    InfoDIc[pcindex] = infolist

def SRAInstr(element, pcindex):
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    sa = twototen(element[21: 26])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("SRL")
    infolist.append("R" + str(rt))
    infolist.append("R" + str(rd))
    infolist.append("#" + str(sa))
    InfoDIc[pcindex] = infolist

def NOPInstr(element, pcindex):
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("NOP")
    InfoDIc[pcindex] = infolist

def ADDInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("ADD")
    infolist.append("R" + str(rd))
    infolist.append("R" + str(rs))
    infolist.append("R" + str(rt))
    InfoDIc[pcindex] = infolist

def SUBInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("SUB")
    infolist.append("R" + str(rd))
    infolist.append("R" + str(rs))
    infolist.append("R" + str(rt))
    InfoDIc[pcindex] = infolist

def MULIntr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("MUL")
    infolist.append("R" + str(rd))
    infolist.append("R" + str(rs))
    infolist.append("R" + str(rt))
    InfoDIc[pcindex] = infolist

def ANDInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("AND")
    infolist.append("R" + str(rd))
    infolist.append("R" + str(rs))
    infolist.append("R" + str(rt))
    InfoDIc[pcindex] = infolist

def ORInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("OR")
    infolist.append("R" + str(rd))
    infolist.append("R" + str(rs))
    infolist.append("R" + str(rt))
    InfoDIc[pcindex] = infolist

def XORInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("XOR")
    infolist.append("R" + str(rd))
    infolist.append("R" + str(rs))
    infolist.append("R" + str(rt))
    InfoDIc[pcindex] = infolist

def NORInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("MUL")
    infolist.append("R" + str(rd))
    infolist.append("R" + str(rs))
    infolist.append("R" + str(rt))
    InfoDIc[pcindex] = infolist

def SLTInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    rd = twototen(element[16: 21])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("SLT")
    infolist.append("R" + str(rd))
    infolist.append("R" + str(rs))
    infolist.append("R" + str(rt))
    InfoDIc[pcindex] = infolist

def ADDIInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    immediate = twototen(element[16: 32])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("ADDI")
    infolist.append("R" + str(rt))
    infolist.append("R" + str(rs))
    infolist.append("#" + str(immediate))
    InfoDIc[pcindex] = infolist

def ANDIInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    immediate = twototen(element[16: 32])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("ANDI")
    infolist.append("R" + str(rt))
    infolist.append("R" + str(rs))
    infolist.append("#" + str(immediate))
    InfoDIc[pcindex] = infolist

def ORIInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    immediate = twototen(element[16: 32])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("ORI")
    infolist.append("R" + str(rt))
    infolist.append("R" + str(rs))
    infolist.append("#" + str(immediate))
    InfoDIc[pcindex] = infolist

def XORIInstr(element, pcindex):
    rs = twototen(element[6: 11])
    rt = twototen(element[11: 16])
    immediate = twototen(element[16: 32])
    infolist = []
    infolist.append(element)
    infolist.append(pcindex)
    infolist.append("XORI")
    infolist.append("R" + str(rt))
    infolist.append("R" + str(rs))
    infolist.append("#" + str(immediate))
    InfoDIc[pcindex] = infolist

def ProcessFile(filelineArr):
    "this function is used to process each element and conduct which type instrution it is"
    # count numbers after break instruction
    linecount = len(filelineArr)
    j = 0
    pcindex = 256
    Pclist.append(pcindex)
    tempinfoDic = OrderedDict()
    while filelineArr[j][0: 6] != "010101":
        pcindex += 4
        j += 1
    valuepc = pcindex + 4
    pcindex = pcindex + 4
    j = j + 1
    while j < linecount:
        element = filelineArr[j]
        infolist = []
        infolist.append(element)
        infolist.append(pcindex)
        if element[0] == "0":
            infolist.append(twototen(element))
            ValueDic[pcindex] = twototen(element)
            tempinfoDic[pcindex] = infolist
        elif element[0] == "1":
            infolist.append("-" + str(CountMinusnum(element)))
            ValueDic[pcindex] = "-" + str(CountMinusnum(element))
            tempinfoDic[pcindex] = infolist
        j += 1
        pcindex += 4
    endpc = pcindex - 4
    Pclist.append(valuepc)
    Pclist.append(endpc)
    pcindex = 256
    i = 0
    while i < linecount:
        element = filelineArr[i]
        instrtype = element[2: 6]
        if element[0: 2] == "01":
            if instrtype == "0000":
                JInstr(element, pcindex)
            elif instrtype == "0001":
                JRInstr(element, pcindex)
            elif instrtype == "0010":
                BEQInstr(element, pcindex)
            elif instrtype == "0011":
                BLTZInstr(element, pcindex)
            elif instrtype == "0100":
                BGTZInstr(element, pcindex)
            elif instrtype == "0101":
                BREAKInstr(element, pcindex)
                break;
            elif instrtype == "0110":
                SWInstr(element, pcindex)
            elif instrtype == "0111":
                LWInstr(element, pcindex)
            elif instrtype == "1000":
                SLLInstr(element, pcindex)
            elif instrtype == "1001":
                SRLInstr(element, pcindex)
            elif instrtype == "1010":
                SRAInstr(element, pcindex)
            elif instrtype == "1011":
                NOPInstr(element, pcindex)
        elif element[0: 2] == "11":
            if instrtype == "0000":
                ADDInstr(element, pcindex)
            elif instrtype == "0001":
                SUBInstr(element, pcindex)
            elif instrtype == "0010":
                MULIntr(element, pcindex)
            elif instrtype == "0011":
                ANDInstr(element, pcindex)
            elif instrtype == "0100":
                ORInstr(element, pcindex)
            elif instrtype == "0101":
                XORInstr(element, pcindex)
            elif instrtype == "0110":
                NORInstr(element, pcindex)
            elif instrtype == "0111":
                SLTInstr(element, pcindex)
            elif instrtype == "1000":
                ADDIInstr(element, pcindex)
            elif instrtype == "1001":
                ANDIInstr(element, pcindex)
            elif instrtype == "1010":
                ORIInstr(element, pcindex)
            elif instrtype == "1011":
                XORIInstr(element, pcindex)
        pcindex += 4
        i += 1
    for k, v in tempinfoDic.items():
        InfoDIc[k] = v

def WriteDisassemblely():
    "this function used to write diaassemblely result to a txt file"
    try:
        outputfile = open("C:/Users/Hanyue Zheng/PycharmProjects/ComputerStructureproj1/disassembly.txt", "w")
    except IOError, e:
        print "file open error: ", e
    for key in InfoDIc:
        outputfile.write(str(InfoDIc[key][0]) + "\t")
        outputfile.write(str(InfoDIc[key][1]) + " ")
        outputfile.write(str(InfoDIc[key][2]) + " ")
        i = 3
        while i < len(InfoDIc[key]):
            if i == len(InfoDIc[key]) - 1:
                outputfile.write(str(InfoDIc[key][i]))
            else:
                outputfile.write(str(InfoDIc[key][i]) + ", ")
            i += 1
        outputfile.write("\n")

def WriteSimulation(cycle, infolist):
    "this function used to write Simulation result to a txt file"
    try:
        outputfile = open("C:/Users/Hanyue Zheng/PycharmProjects/ComputerStructureproj1/simulation.txt", "a")
    except IOError, e:
        print "file open error: ", e
    for i in range(20):
        outputfile.write("-")
    outputfile.write("\n")
    outputfile.write("Cycle:" + str(cycle)  + "\t")
    outputfile.write(str(infolist[1]) + " ")
    outputfile.write(str(infolist[2]) + " ")
    i = 3
    while i < len(infolist):
        if i == len(infolist) - 1:
            outputfile.write(str(infolist[i]))
        else:
            outputfile.write(str(infolist[i]) + ", ")
        i += 1
    outputfile.write("\n" + "\n")
    outputfile.write("Registers")
    for i in range(32):
        if i % 8 == 0:
            outputfile.write("\n")
            if i < 10:
                outputfile.write("R" +  "0" + str(i) + ":" + "\t" )
            else:
                outputfile.write("R" + str(i) + ":" + "\t")
        outputfile.write(str(RigsterDic["R" + str(i)]) + "\t")
    outputfile.write("\n" + "\n")
    outputfile.write("Data")
    j = Pclist[2]
    while j <= Pclist[3]:
        if (j - Pclist[2]) % 32 == 0:
            outputfile.write("\n")
            outputfile.write(str(j) + ":" + "\t")
        outputfile.write(str(ValueDic[j]) + "\t")
        j += 4
    outputfile.write("\n" + "\n")

def Simulation():
    "this function used to simulate the process of instructions"
    nowpc = Pclist[1] # pc right now
    terminalflag = True
    while terminalflag:
        information = InfoDIc[nowpc]
        instruction = information[2]
        if instruction == "ADD":
            RigsterDic[information[3]] = int(RigsterDic[information[4]]) + int(RigsterDic[information[5]])
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "ADDI":
            RigsterDic[information[3]] = RigsterDic[information[4]] + int(information[5][1:])
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "BREAK":
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            terminalflag = False
        elif instruction == "SUB":
            RigsterDic[information[3]] = RigsterDic[information[4]] - RigsterDic[information[5]]
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "MUL":
            RigsterDic[information[3]] = int(RigsterDic[information[4]]) * int(RigsterDic[information[5]])
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "AND":
            RigsterDic[information[3]] = RigsterDic[information[4]] and RigsterDic[information[5]]
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "OR":
            RigsterDic[information[3]] = RigsterDic[information[4]] or RigsterDic[information[5]]
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "XOR":
            RigsterDic[information[3]] = RigsterDic[information[4]] ^ RigsterDic[information[5]]
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "SLT":
            if RigsterDic[information[4]] < RigsterDic[information[5]]:
                RigsterDic[information[3]] = 1
            else:
                RigsterDic[information[3]] = 0
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "ANDI":
            RigsterDic[information[3]] = RigsterDic[information[4]] and int(information[5][1:])
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "ORI":
            RigsterDic[information[3]] = RigsterDic[information[4]] or int(information[5][1:])
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "XORI":
            RigsterDic[information[3]] = RigsterDic[information[4]] ^ int(information[5][1:])
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "J":
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc = int(information[3][1:])
        elif instruction == "JR":
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc = int(RigsterDic[information[3]])
        elif instruction == "BGTZ":
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            if RigsterDic[information[3]] > 0:
                nowpc = nowpc + 4 + int(information[4][1:])
            else:
                nowpc += 4
        elif instruction == "BLTZ":
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            if RigsterDic[information[3]] < 0:
                nowpc = nowpc + 4 + int(information[4][1:])
            else:
                nowpc += 4
        elif instruction == "LW":
            index1 = information[4].find("(")
            index2 = information[4].find(")")
            RigsterDic[information[3]] = ValueDic[RigsterDic[information[4][index1 + 1: index2]] + int(information[4][0: index1])]
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "SW":
            index1 = information[4].find("(")
            index2 = information[4].find(")")
            ValueDic[int(information[4][0: index1]) + RigsterDic[information[4][index1 + 1: index2]]] = RigsterDic[information[3]]
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "NOP":
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "BEQ":
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            if int(RigsterDic[information[3]]) == int(RigsterDic[information[4]]):
                nowpc = nowpc + int(information[5][1: ]) + 4
            else:
                nowpc += 4
        elif instruction == "SLL":
            decimal = tentotwo(RigsterDic[information[4]])
            offset = information[5][1:]
            zerostr = ""
            index = 0
            while index < int(offset):
                zerostr += "0"
                index += 1
            finalnum = decimal[int(offset): ] + zerostr
            RigsterDic[information[3]] = twototen(finalnum)
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "SRL":
            decimal = tentotwo(RigsterDic[information[4]])
            offset = information[5][1:]
            zerostr = ""
            index = 0
            while index < int(offset):
                zerostr += "0"
                index += 1
            finalnum = zerostr + decimal[0: 32 - offset]
            RigsterDic[information[3]] = twototen(finalnum)
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "SRA":
            decimal = tentotwo(RigsterDic[information[4]])
            offset = information[5][1:]
            zerostr = ""
            index = 0
            while index < int(offset):
                zerostr += decimal[0]
                index += 1
            finalnum = zerostr + decimal[0: 32 - offset]
            RigsterDic[information[3]] = twototen(finalnum)
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        elif instruction == "NOR":
            RigsterDic[information[3]] = RigsterDic[information[4]] & RigsterDic[information[5]]
            cycle = Pclist[0] + 1
            Pclist[0] += 1
            SimulationDic[cycle] = information
            WriteSimulation(cycle, information)
            nowpc += 4
        else:
            nowpc += 4

if __name__ == '__main__':
    filelineArr = GetFile()
    ProcessFile(filelineArr)
    WriteDisassemblely()
    Simulation()
    print "SimulationDic ", SimulationDic
    print "ValueDic ", ValueDic
    print  "RegisterDic ", RigsterDic

