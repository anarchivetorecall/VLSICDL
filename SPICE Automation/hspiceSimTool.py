'''
Original ver. written by: Prof. H. Jeong
Revised by: VLSICDL
'''

import re
import numpy as np
import math
import probTool
import matplotlib.pyplot as plt
import scipy
import time
import os
import subprocess
from scipy.stats import probplot

def removeFailed(arrayIn):
    arrayOut = np.array([])
    for k in arrayIn:
        if k == "failed":
            pass
        else:
            arrayOut = np.append(arrayOut, k)
            
    return arrayOut
 
def grepVar(MClis, varName):
    pVarName = re.compile("^\s*"+varName+"="+"\s*(\S+)")
    valueList = []
    grepLog = MClis.replace(".lis", "_"+varName+".log")
    error = 0
    with open(grepLog, "w") as fLog:
        with open(MClis, "r") as fMClis:
            for line in fMClis.readlines():
                mVarName = pVarName.search(line)
                if mVarName:
                    grepVal = mVarName.group(1)
                    if grepVal != "failed":
                        grepVal = float(grepVal)
                    else:
                        error += 1
                        fLog.write("failed is observed in %s"%MClis)
                    valueList.append(grepVal)
    print("%d error exist : find %s"%(error, grepLog))
    return valueList

def runFileGen(fileNameList, runFileName, parallel=5):
    Np = 1
    with open(runFileName, "w") as fRun:
        for fileName in fileNameList:
            runOrder = "runHspice %s"%fileName
            if (Np%parallel):
                runOrder = runOrder+"&"
            fRun.write(runOrder+"\n")
            Np += 1

def num2Str(Num):
    numStr = str(Num).replace(".", "p")
    #numStr = numStr.replace(".", "p")
    return numStr

def deriveProb(txtFile, lessthan=0):
    data = np.loadtxt(txtFile)
    event = data<lessthan
    return sum(event)/len(event)

def timetoDelayDic(inDic):
 
    outList = []
    for stg in inDic.keys():
        if(str(int(stg)+1) in inDic.keys()):
            outList.append( float(inDic[str(int(stg)+1)]) - float(inDic[stg]) )
        else:
            break
        
    return outList

def cirNumVsCirName(fileLIS):
    
    fIN_lis = open(fileLIS, "r")
    lines = fIN_lis.readlines()
    
    lineNum = 0
    enable = 0 
    
    numVsName = re.compile("\s*(\d+)\s+(\S+)")
    lineEnd   = re.compile("[^\S]+\n")
    
    circuitNumName = {}
    
    while(1):
        line = lines[lineNum]
        mNumVsName = numVsName.search(line)
        mLineEnd   = lineEnd.search(line)
        if(enable):
            if(mNumVsName):
                circuitNum  = mNumVsName.group(1)
                circuitName = mNumVsName.group(2).rstrip(".")
                circuitNumName[circuitNum] = circuitName
            elif(mLineEnd):
                break
        elif("circuit number to circuit name directory" in line):
            enable = 1
        else:
            pass
        lineNum += 1

    return circuitNumName

def replaceSp(fileSpIn, fileSpOut, dicReplace):
    #Usage : replaceSp("REF.sp", "target.sp", {FFName, TGFF, nMonte, 20 ...} )
    fHIn  = open(fileSpIn, "r")
    fHOut = open(fileSpOut, "w")
    
    for line in fHIn.readlines():
        for parORG in dicReplace.keys():
            if(parORG in line):
                line = line.replace("{"+str(parORG)+"}", str(dicReplace[parORG]))
                break
        fHOut.write(line)
    
    fHOut.close()
    fHIn.close()
    
    
def netDvth0Label(fileNetlist):
    fIN = open(fileNetlist, "r")
    lines = fIN.readlines()
    
    subcktDefine = re.compile("^\s*.subckt\s+(\S+)\s+")
    subcktEnd   = re.compile("^\s*.ends")
    
    #subcktList = []
    subcktComplete = {}
    defLine = {}
    endLine = {}
    #Forming subckt lists
    for line in lines:
        mSubcktDefine = subcktDefine.search(line)
        mSubcktEnd = subcktEnd.search(line)
        if(mSubcktDefine):  # Check Wsubcircuit definition 
            curSubckt = mSubcktDefine.group(1)
            subcktComplete[curSubckt]=0
        else:
            pass
            
    #Adding dvth0's for FETs
    FETInst    = re.compile("^\s*(x\S*)\s+\S+\s+\S+\s+\S+\s+\S+\s+((pfet\S+)|(nfet\S+))\s+(.*)", re.I)
    subcktInst = re.compile("^\s*(x\S*)\s+[^=]*\s+([^=\s]+)(\s+\S+\s*=|\s*\n)", re.I)
    dvth0Define = re.compile("dvth0[^=\s]*\s*=\s*[^=\s]+")
    
    lineNum = 0
    lineNumMax = len(lines)
    linesOUT = lines
    inSubckt   = 0
    loop = 0
    
    #Subcircuit Labeling while Loop
    #while(math.prod(subcktComplete.values())!=1):
    instDic = {}
    finalLoop=0
    while(1):       
        line = lines[lineNum]
        lineOUT = line
        
        mSubcktDefine = subcktDefine.search(lineOUT)
        mSubcktEnd = subcktEnd.search(lineOUT)
        mFET       = FETInst.search(lineOUT)
        mSubckt    = subcktInst.search(lineOUT)
        
        if(mSubcktDefine):  # Check Wsubcircuit definition 
            curSubckt = mSubcktDefine.group(1)
            if(subcktComplete[curSubckt]):
                lineNum = endLine[curSubckt]
                continue
            defLine[curSubckt] = lineNum
            inSubckt = 1
            instDic[curSubckt] = []
            completeSubckt = 1
            
        elif(mSubcktEnd):
            subcktComplete[curSubckt]=completeSubckt
            endLine[curSubckt] = lineNum
            #print("curSubckt = "+curSubckt+" search is completed as %d" %completeSubckt)
            if(completeSubckt):
                lineOUTsubcktDef = linesOUT[defLine[curSubckt]].rstrip("\n")
                for inst in instDic[curSubckt]:
                    lineOUTsubcktDef = lineOUTsubcktDef + " dvth0_" + inst + "=0"
                linesOUT[defLine[curSubckt]] = lineOUTsubcktDef + "\n"
            curSubckt = ""
            inSubckt = 0
    
        elif(inSubckt): # check whether 
            #Duplciation Check        
            while(1):
                mDvth0Define = dvth0Define.search(lineOUT)
                if(not mDvth0Define):
                    break            
                lineOUT = lineOUT.replace(mDvth0Define.group(0),"")
                #print("remove " + mDvth0Define.group(0))
            if(mFET):   #if FET is called, labeling FET to dvth                      
                instFETName = mFET.group(1)
                instDic[curSubckt].append(instFETName)
                #print(curSubckt + " : instComp is added : " +instFETName )
                dvthVar = "dvth0_" + instFETName
                lineOUT = lineOUT.rstrip("\n") + " dvth0=" + dvthVar + "\n"
                
            elif(mSubckt): #if subckt other than FET is called,
                subcktCalled = mSubckt.group(2)
                instName = mSubckt.group(1)
                if(subcktComplete[subcktCalled]==1):
                    lineOUT = lineOUT.rstrip("\n")
                    for instSub in instDic[subcktCalled]:
                        instDic[curSubckt].append(instName + "_" + instSub)
                        lineOUT = lineOUT + " dvth0_" + instSub + "=" + "dvth0_" + instName + "_" + instSub
                    lineOUT= lineOUT + "\n"
                    #print("do something")
                elif(subcktComplete[subcktCalled]==0):
                    completeSubckt = 0 
                    #print("do nothing")
                else:
                    print("ERROR : Invalid subckt")
                    exit("ERROR : Invalid subckt")
            else: # other circuit components inside the subcircuit define parts. 
                pass
           
        else:   #outside subcircuit parts: for top-level circuit
            pass
            if(finalLoop):
                
                mFET       = FETInst.search(lineOUT)
                mSubckt    = subcktInst.search(lineOUT)
                mDvth0Define = dvth0Define.search(lineOUT)
                #Duplciation Check        
                while(1):
                    if(not mDvth0Define):
                        break            
                    lineOUT = lineOUT.replace(mDvth0Define.group(0),"")
                    
                if(mFET):   #if FET is called, labeling FET to dvth                      
                    instFETName = mFET.group(1)
                    dvthVar = "dvth0_" + instFETName
                    
                    lineOUT = lineOUT.rstrip("\n") + " dvth0=" + dvthVar + "\n"
                    
                elif(mSubckt): #if subckt other than FET is called,
                    subcktCalled = mSubckt.group(2)
                    instName = mSubckt.group(1)
                    lineOUT = lineOUT.rstrip("\n")
                    for instSub in instDic[subcktCalled]:
                        lineOUT = lineOUT + " dvth0_" + instSub + "=" + "dvth0_" + instName + "_" + instSub
                    lineOUT= lineOUT + "\n"
                    #print("do something")
                else:
                    pass
                #print(str(lineNum) + " finalLoop : " + lineOUT)
            else:
                pass
            
        lineNum = lineNum + 1        
    
        linesOUT[lineNum-1] = lineOUT
    
        if(lineNum == lineNumMax):
            lineNum = 0
            loop = loop + 1
            if(finalLoop):
                print("final")
                break
            elif(math.prod(subcktComplete.values())==1):
                finalLoop=1
                print("finalLoop Start")
            
       
    fIN.close()    
    fOUTName = fileNetlist + ".dvth0"
    
    fOUT = open(fOUTName, "w")
    for lineOUT in linesOUT:        
        fOUT.write(lineOUT)        
    fOUT.close()

def genDataSweepSp(dataFile, dataName, fileRef, fileOUT):
    fRef = open(fileRef, "r")
    fOUT = open(fileOUT, "w")
    refLines = fRef.readlines()
    for line in refLines:
        if "{dataFile}" in line:
            line = line.replace("{dataFile}", dataFile)
        if "{dataName}" in line:
            line = line.replace("{dataName}", dataName)
        fOUT.write(line)
    fRef.close()
    fOUT.close()

def removeMonte(fSpIN, fSpOUT):
    fHIN  = open(fSpIN, "r")
    fHOUT = open(fSpOUT, "w")
    
    inLines = fHIN.readlines()
    pMonte = re.compile("\s+(sweep\s+monte\s*=\s*\S+)", re.I)
    
    for line in inLines:
        mMonte = pMonte.search(line)
        if (mMonte):
            sMonte = mMonte.groups()[0]
            line = line.replace(sMonte,"")
        else:
            pass
        fHOUT.write(line)
    fHIN.close()
    fHOUT.close()

def setMonte(fSpIN, fSpOUT, MonteNum, seed=1):
    pSpExt = re.compile("\.sp$")
    mSpExt = pSpExt.search(fSpIN)
    if(mSpExt):
        pass
    else:
        print("*.sp File should be inputted")
        raise Exception("Wrong fileInitialSearch format \n")        

    fSpNoMC = fSpIN.replace(".sp", "_noMC.sp")
    removeMonte(fSpIN, fSpNoMC)
    fHIN  = open(fSpNoMC, "r")
    fHOUT = open(fSpOUT, "w")
    
    inLines = fHIN.readlines()
    outLines = []
    pTran  = re.compile("^\s*\.tran\s+\S+\s+\S+\s+", re.I)
    pMonte = re.compile("\s*(sweep\s+monte\s*=\s*\S+)", re.I)
    pSeed  = re.compile("\s*(seed\s*=\s*\S+)", re.I)

    MonteRep = 0    
    seedRep  = 0
    
    k=0
    for line in inLines:
        mTran  = pTran.search(line)
        mMonte = pMonte.search(line)
        mSeed  = pSeed.search(line)
        if (mTran):
            kTran = k
        if (mMonte):
            prevMonteDef = mMonte.groups()[0]
            line = line.replace(prevMonteDef, "sweep monte = %d"%MonteNum)
            MonteRep = 1
        if (mSeed):
            prevSeedDef = mSeed.groups()[0]
            line = line.replace(prevSeedDef, "seed = %d"%seed)
            seedRep  = 1
        else:
            pass
        k+=1
        outLines.append(line)
    
    print(MonteRep)
    print(seedRep)
    if(MonteRep==0):
        print(outLines[kTran])
        outLines[kTran] = outLines[kTran].rstrip("\n") + " sweep Monte = %d\n"%MonteNum
    if(seedRep==0):
        outLines[kTran] = ".option seed = %d\n"%seed + outLines[kTran]
    
    for line in outLines:
        fHOUT.write(line)
        
    fHIN.close()
    fHOUT.close()

def netChange(fSpIN, fSpOUT, oldNet, newNet):
    fHIN  = open(fSpIN, "r")
    fHOUT = open(fSpOUT, "w")
    
    inLines = fHIN.readlines()
    pNetInc = re.compile("^\s*\.(inc|include)\s+\S*%s"%oldNet, re.I)
    
    for line in inLines:
        mNetInc = pNetInc.search(line)
        if (mNetInc):
            line = line.replace(oldNet,newNet)
        else:
            pass
        fHOUT.write(line)
    fHIN.close()
    fHOUT.close()
    
def setSimTime(fSpIN, fSpOUT, simTime):
    fHIN  = open(fSpIN, "r")
    fHOUT = open(fSpOUT, "w")
    
    inLines = fHIN.readlines()
    pTran = re.compile("^\s*\.tran\s+\S+\s+(\S+)\s+", re.I)
    
    for line in inLines:
        mTran = pTran.search(line)
        if (mTran):
            simTimeOld = mTran.groups()[0]
            line = line.replace(simTimeOld,simTime)
        else:
            pass
        fHOUT.write(line)
    fHIN.close()
    fHOUT.close()
    
def includeFile(fSpIN, fSpOUT, fileIncluded):
    fHIN  = open(fSpIN, "r")
    fHOUT = open(fSpOUT, "w")
    
    inLines = fHIN.readlines()
    pInclude = re.compile("^\s*\.(inc|include)\s+\S+", re.I)
    
    lineIdx = 0
    incEn=0
    for line in inLines:
        mInclude = pInclude.search(line)
        if (mInclude):
            incEn = 1
        elif(incEn==1):
            newIncLine =".include \"%s\"\n"%fileIncluded
            inLines[lineIdx] = newIncLine + line
            break
        else:
            pass
        lineIdx += 1
        
    for line in inLines:
        fHOUT.write(line)
    fHIN.close()
    fHOUT.close()
    
def genParamFile(sampleDic, fileParamSp):
    fHOUT = open(fileParamSp, "w")
    fHOUT.write(".param\n")
    for par in sampleDic.keys():
        fHOUT.write("+"+par+" = "+str(sampleDic[par])+"\n")
        
def extSeqPar(fileLis, baseParName):
    # grepRun = subprocess.Popen("grep -P \"twlen2sae\d+\"= vbl_single.lis | wc | awk '{print $1}'", shell=True, stdout=subprocess.PIPE)
    # Num = int(grepRun.stdout.read())
    # for n in np.arange(Num):
    #     print(n)
    fHLis = open(fileLis, "r")
    parDic = {}
    pPar = re.compile(baseParName+"(\d+)=\s*(\S+)", re.I)
    for line in fHLis.readlines():
        mPar = pPar.search(line)
        if(mPar):
            nIdx = mPar.groups()[0]
            val  = mPar.groups()[1]
            parDic[nIdx] = val
        
    fHLis.close()
    return parDic

def MCSeedExpansion(fSpIN, seedNum):
    pSpExt = re.compile("\.sp$")
    mSpExt = pSpExt.search(fSpIN)
    if(mSpExt):
        pass
    else:
        print("*.sp File should be inputted")
        raise Exception("Wrong fileInitialSearch format \n")        

    seedList = np.arange(seedNum)+1
    pOption = re.compile("^\s*\.(option|options)")
  
    
    for seed in seedList:
        fSpOUT = re.sub("\.sp$", "_seed%d.sp"%seed, fSpIN)
        fHOUT = open(fSpOUT, "w")
        fHIN  = open(fSpIN, "r")
        inLines = fHIN.readlines()
    
        lineIdx=0
        optionEn=0
        for line in inLines:
            mOption = pOption.search(line)
            if (mOption):
                optionEn=1
            elif(optionEn==1):
                newLine = ".option seed=%d\n"%seed
                inLines[lineIdx] = newLine + line
                break
            else:
                pass
            lineIdx += 1
            
        for line in inLines:
            fHOUT.write(line)
        fHOUT.close()
        print(fSpOUT+" is generated!")
        fHIN.close()    
        
    fileRun  = "runSeedExpan%d_"%seed+fSpIN.replace(".sp", ".csh")
    fHRun  = open(fileRun, "w")
    fHRun.write("#!/bin/csh -f \n\n")
    
    fileGrep = fileRun.replace("runSeed", "grepResult")
    fHGrep = open(fileGrep, "w")
    fHGrep.write("#!/bin/csh -f \n\n")
    
    fResult= "%s_seedExpan%d_grep_{$argv[1]}.txt"%(fSpIN.replace(".sp", ""), seed)
    j=0
    for seed in seedList:
        fSpOUT = re.sub("\.sp$", "_seed%d.sp"%seed, fSpIN)
        fLisOUT= fSpOUT.replace(".sp", ".lis")
        
        fHRun.write("runHspice %s & \n"%fSpOUT)
        if(j==0):
            fHGrep.write(":grepVar.csh $argv[1] %s > %s \n"%(fLisOUT, fResult))
        else:
            fHGrep.write(":grepVar.csh $argv[1] %s >> %s \n"%(fLisOUT, fResult))
        j+=1
    fHRun.write("\n")
    fHRun.close()
    fHGrep.close()
    os.system("chmod +x %s"%fileRun)
    os.system("chmod +x %s"%fileGrep)
    print("runfile %s is generated"%fileRun)
    print("grepfile %s is generated"%fileGrep)
    
    
def nfinExtract(fileSp, FETNumVsName, spiceRun=0):
    numFET = 0
    nfinName = []
    fileNfinPrint = fileSp.replace(".sp", "_nfinParam.sp")
    fNfinPrt = open(fileNfinPrint, "w")
    for FETName in FETNumVsName.values():
        measParam = FETName+".nfin"
        fNfinPrt.write(".print par('" + measParam + "')\n")
        nfinName.append(measParam)
        numFET += 1    
    fNfinPrt.close()    
    
    fileSpNoMC = fileSp.replace(".sp", "_noMC.sp")
    fileSpShort = fileSp.replace(".sp", "_short.sp")
    fileSpNfinPrint = fileSp.replace(".sp", "_nfinPrint.sp")
    removeMonte(fileSp, fileSpNoMC)
    setSimTime(fileSpNoMC, fileSpShort, "10p")
    includeFile(fileSpShort, fileSpNfinPrint, fileNfinPrint)
    
    if(spiceRun):
        print("spiceRun is enabled, thus hspice is run for extracting Nfin\n")
        os.system("runHspice "+fileSpNfinPrint)    
    else:
        print("spiceRun is disabled, thus hspice is NOT run for extracting Nfin\n")
    fileNfinLIS = fileSpNfinPrint.replace(".sp", ".lis")
    fNfinLIS = open(fileNfinLIS, "r")
    paramPrintStart = re.compile("^ x$")
    parValue        = re.compile("^\s*\S+\s+(\S+)")
    paramPrintEnd   = re.compile("^y$") 
    
    parNum = 0 
    lineNum = 0
    parGrepEn = 0
    numFET = 0
    nfinNameVsVal = {}
    for line in fNfinLIS.readlines():
        lineNum += 1
        if(paramPrintStart.search(line)):
            parGrepEn = 1
        elif(paramPrintEnd.search(line)):
            parGrepEn = 0
            numFET += 1
        
        mParValue = parValue.search(line)
        if(parGrepEn):
            if(mParValue):
                parGrep = mParValue.group(1)
                nfinNameVsVal[nfinName[numFET].replace(".nfin", "")]=parGrep
        else:
            pass
    return nfinNameVsVal

def truncateMT(fMTIn, fMTOut, Ncut):
    fHIn   = open(fMTIn, "r")
    fHOut  = open(fMTOut, "w")
    
    pStart = re.compile("^ (\d+)\s+", re.I)
    
    for lineIN in  fHIn.readlines():
        mStart = pStart.search(lineIN)
        if(mStart):
            if(int(mStart.groups()[0])== Ncut+1):
                break;
        fHOut.write(lineIN)
    
    fHIn.close()
    fHOut.close()
    
def mt2Data(fileLis, fileMt, indexList, fileOUT):
    cirNumVsName = cirNumVsCirName(fileLis)
    cirNumVsDvth0Name = {}
    
    #Converting instanceName to dvth0
    for k in  cirNumVsName.keys():
        cirNumVsDvth0Name[k]="dvth0_"+cirNumVsName[k].replace(".", "_")
        
    
    fMTIN = open(fileMt, "r")
    
    lines = fMTIN.readlines()
    
    start = re.compile("^\s*index")
    end   = re.compile("\s*alter#")
    gausVal = re.compile("\s+\S*@(\d+):(gaus_val|vthvar)")
    
    lineNum=0
    index=0
    cirNumEn  = 0
    parValueEn = 0
    cirNumList = []
    gausValIdxList = []
    parValList = [[]]
    parValList.append([])
    parIdx = 0
    FETNumVsName = {}
    
    for line in lines:
        lineNum += 1
        lineSplit = line.split()
        mStart = start.search(line)
        if(mStart):
            cirNumEn=1
            
     #   if(cirNumEn):
        for par in lineSplit:
            mEnd = end.search(par)
            if(cirNumEn):
                #par = re.findall("(\d+):gaus_val", par)
                parIdx += 1
                cirNumList.append(par)
                parValList[index].append("")
                gausValcirNum = re.findall("(\d+):(gaus_val|vthvar)", par)
                if(gausValcirNum):
                    gausValIdxList.append(parIdx-1)
                    FETNumVsName[gausValcirNum[0][0]]=cirNumVsName[gausValcirNum[0][0]]
                    parValList[index][parIdx-1] = cirNumVsDvth0Name[gausValcirNum[0][0]]
                
                if(mEnd):
                    print("mEndMatch : ")
                    print(par)
                    cirNumEn=0
                    parValueEn=1
                    parIdx = 0
                    #parValList[index] = cirNumList 
                    index += 1
    
            elif(parValueEn):
                parIdx += 1
                #parValList.append([])
                parValList[index].append(float(par))
                if(parIdx == len(cirNumList)):
                    parValList.append([])
                    parIdx = 0
                    index += 1
                    
    del parValList[-1]
    #for numFET in FETNumVsName.keys():
        
    print("out : ")
    print(np.size(parValList))
    
    fOUT = open(fileOUT, "w")
    parNumLine = 5
    #parNum = 0
    indexList.insert(0, 0)
    
    fOUT.write("$$Extracted from %s\n" %fileLis)
    fOUT.write(".data dataDvth0\n")
    
    sigmaSum = []
    for idxPrint in indexList:
        parNum = 0
        for gausIdx in gausValIdxList:
            parNum += 1
            if(idxPrint>0):
                fOUT.write("%1.3e\t" %-parValList[idxPrint][gausIdx])
            else:
                fOUT.write("%s\t" %parValList[idxPrint][gausIdx])
    
            if(parNum == parNumLine):
                fOUT.write("\n")
                parNum = 0
        fOUT.write("\n")
    
    fOUT.write(".enddata\n")
    fOUT.close()
    
    return parValList, FETNumVsName
    

def list2Data(varNameList, valList2D, fOUTName):    

    parNumLine = 5
    fOUT = open(fOUTName, "w")
    
    for varName in varNameList:
        fOUT.write(varName + "\t")
    fOUT.write("\n")
    
    for valueListIdx in valList2D:
        for value in valueListIdx:
            fOUT.write("%1.3e\t" %value)
        fOUT.write("\n")
        #print(valueListIdx)
    
    fOUT.close()   


def QQplot(dataSetFileName) : ## see the Data plot and select your lowPoint and highPoint 
    data = np.loadtxt("{}".format(dataSetFileName))
    f1, ax1 = plt.subplots( figsize = (12,8))
    probplot(data,plot=ax1)
    

def Tail_fitting(dataSetFileName ,lowTailSigma, highTailSigma, dataMode=0, QQPlot=1):
    
    #Load Data file & Sorting
    if (dataMode>0):
        data = dataSetFileName
    else:
        data = np.loadtxt("{}".format(dataSetFileName))
        
    DataMean = np.average(data)
    DataSigma = np.std(data)
    dataSorted = np.sort(data)
    Ndata = len(dataSorted)
    
    #Calculte CDF value of lowTail & highTail
    lowProb = scipy.stats.norm.cdf(lowTailSigma)
    highProb = scipy.stats.norm.cdf(highTailSigma)

    #Sigma Value extration
    lowDataRanking = int(round(Ndata*lowProb, 0))
    highDataRanking = int(round(Ndata*highProb, 0))
    lowTailSigmaRev = scipy.stats.norm.ppf(lowDataRanking/Ndata)
    highTailSigmaRev = scipy.stats.norm.ppf(highDataRanking/Ndata)
    
    #Calculate the line slop and constant value of Tail
    i=0
    dataLow = 0
    dataHigh = 0
    while True:
        dataLow  += dataSorted[lowDataRanking -3 + i ] #AVG value calculation
        dataHigh += dataSorted[highDataRanking - 3 + i]
        i += 1
        if i >= 6:
            break  
    dataLowAVG = dataLow/i
    dataHighAVG = dataHigh/i
    
    slope = (dataHighAVG-dataLowAVG)/(highTailSigmaRev-lowTailSigmaRev)
    meanTail = -highTailSigma*slope + dataHighAVG
    sigmaTail = slope
    
    #Original data QQ plot
    #data = np.loadtxt("{}".format(dataSetFileName))
    if (QQPlot>0):
        f1, ax1 = plt.subplots( figsize=(12,8)  )
        probplot(data,plot=ax1)
        
        #Tail fitted data QQ plot
        plot_scale = scipy.stats.norm.ppf(1/Ndata)
        xRange = np.arange(plot_scale, -plot_scale, 0.05)
        yPlot = sigmaTail*xRange + meanTail
        ax1.plot(xRange, yPlot, 'g', label = "Tail fitted Data")
        ax1.set_title(" Original QQ plot & Tail fitted QQ plot   ")
        ax1.legend(loc="best")
    print("Previous mean & sigma value :", DataMean, DataSigma)
    print("Current mean & sigma value :", meanTail, sigmaTail )

    return meanTail, sigmaTail
