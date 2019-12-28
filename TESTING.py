#For this testing I am trying to figure out which SS files are making MakingCombinations divide by 0 
    
#Loading in Packages that are necessary for SOSA to run
import numpy as np
from os import listdir
#%matplotlib notebook #THis is automatically enabled on Mac's 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import xlwt
from xlwt import Workbook
from os import path
import pandas as pd


def FileLocations():
    '''
    Input: None
    Output: A tuple of strings (SS Folder Path if have,Binary File Path,Excel File Path if have)
    '''
    binarypath = BinaryFileQuestion()
    haveExcelFilequestion = input('''
-----------------------------------------------------------
Do you have previously generated SS that you would like to use? (Yes/No)''')
    if haveExcelFilequestion.lower() in ['yes','y']:
        excelpath = ExcelFileQuestion()
        return ("None",binarypath,excelpath)
    else:
        sspath = SSFolderQuestion()
        return (sspath,binarypath,"None")
        
def SSFolderQuestion():
    print('''
-----------------------------------------------------------
Enter the path to the folder that contains all your SS 
    EXAMPLE: /home/jgussman/Research/Binaries/Data/SS/''')
    ssLocationFound=''
    while True:
        ssLocation=input("\nYours:  ")
        if ssLocation[len(ssLocation)-1]!='/': #In case the user forgets to put the \ at the end of the path 
            ssLocation=ssLocation+"/"
        if not path.exists(ssLocation):
                print("This location does NOT exist! Try again!")
        else:
            print("SS Folder Path Found!")
            return ssLocation

def BinaryFileQuestion():
    '''
    Input: None
    Output: String of Binary Spectra file path
    '''
    print('''
-----------------------------------------------------------
Enter the path to your Observed Binary Spectra! 
    EXAMPLE: /home/jgussman/Research/Binaries/Data/Binaries/HIP86201.txt''')
    while True:
        binaryLocation=input("\nYours:  ")
        if not path.exists(binaryLocation):
            print("This location does NOT exist! Try again!")
        else:
            print("Binary File Path Found!")
            return binaryLocation

def ExcelFileQuestion(): 
    '''
    Input: None
    Output: String of Excel file path
    '''
    print('''
-----------------------------------------------------------
Enter the path to the excel file. 
    EXAMPLE:/home/jgussman/Research/Combinations/HIP86201SS.xls''')
    while True:
        excelLocation=input("\nYours: ")
        if  not path.exists(excelLocation):
            print("This location does NOT exist! Try again!")
        else:
            print("Excel File Path Found!")
            return excelLocation                                                    
                
ssLocation, binaryLocation, excelLocation = FileLocations()

#Loading Data.
print('''
-----------------------------------------------------------
Loading Data...
''')

def LoadInData(FolderLocation,binaryLoc):
    '''
    Input: String SS Folder Path, float wavelength seperation  
    Output: Dictionary of SS for left SS, Dictionary of SS for Right SS, an int of how many decimal places the SS have
    Dictionaries; KEY: Temp of SS, ITEM: ['wavelength','flux']
    '''
    filenames = [name for name in listdir(FolderLocation)] #Extracting the file names 
    for i in range(len(filenames)): #Displaying all the file names nicely so the user can pick which to use
        print(str(i)+": "+ filenames[i])
        
    listofFilesForLeftStar = list(map(int, input('''
Type in the number/s seperated by spaces corresponding to the Synthetic Spectra files you want to be used for the Left star.
Example: 1 3 5 6
Your Answer: ''').split())) 
    listofFilesForRightStar = list(map(int, input('''
Type in the number/s seperated by spaces corresponding to the Synthetic Spectra files you want to be used for the Right star.
Example: 2 7 10
Your Answer: ''').split())) 

    leftSStoUse = [filenames[i] for i in listofFilesForLeftStar]
    rightSStoUse = [filenames[j] for j in listofFilesForRightStar]

    wav_bi,flux_bi=np.loadtxt(binaryLoc,unpack=True)
    input("SOSA is about to display the observed spectra so you can determine the wavelength seperation of the two stars. If you are ready press enter")
    plt.plot(wav_bi, flux_bi)
    plt.show()
    wavelengthShift = float(input("What is the wavelength difference for the two stars(In angstroms)? "))

    lengthofTxtFile = 0
    numberofdecimals = str(wavelengthShift)[::-1].find('.')
    indexforShift = int(wavelengthShift * eval('10000000000'[0:numberofdecimals+1]))
    LSS = {} #KEY: Temp of SS, ITEM: ['wavelength','flux']
    RSS = {} #KEY: Temp of SS, ITEM: ['wavelength','flux']
    for data in leftSStoUse:
        if lengthofTxtFile ==0:
            lengthofTxtFile = len(np.loadtxt(ssLocation+data,unpack=True)[0])
        LSS[int(data[:4])]=[np.loadtxt(ssLocation+data,unpack=True)[0]+wavelengthShift,np.loadtxt(ssLocation+data,unpack=True)[1]]
        LSS[int(data[:4])]=[LSS[int(data[:4])][0][indexforShift:],LSS[int(data[:4])][1][indexforShift:]]
    for data in rightSStoUse:
        RSS[int(data[:4])]=[np.loadtxt(ssLocation+data,unpack=True)[0][:lengthofTxtFile-indexforShift],
                                    np.loadtxt(ssLocation+data,unpack=True)[1][:lengthofTxtFile-indexforShift]]
    decimals = str(LSS[int(leftSStoUse[0][:4])][0][0])[::-1].find('.')
    #wav_bi=np.round(wav_bi,decimals) #Round the binary wavelength if necessary ***This is what is giving me an error of NA*** i.e. it is dividing by 0 
    wav_bi += 0.370
    return (LSS,RSS,wav_bi,flux_bi)
        
LeftSS,RightSS, wav_binary, flux_binary= LoadInData(ssLocation,binaryLocation)


#Make Combinations

def MakingCombinations(LeftSS,RightSS,wav_binary,flux_binary,delta_weight):
    '''
    Input: {Temp of Left SS : ['wavelength','flux']} , {Temp of Right SS : ['wavelength','flux']}, {wavelengths of binaries : fluxes of binaries} , incredment for the weight 
    Output: {(Left SS Temp,Right SS Temp, Left SS Weight, Right SS Weight : Standard deviation from the observed spectra}
    '''
    combinations={}
    for l in LeftSS:
        for r in RightSS:
            for weight in np.arange(delta_weight,100,delta_weight):
                weight=float(weight)
                leftWeighted=LeftSS[l][1]*weight/100.
                rightWeighted=RightSS[r][1]*(100.-weight)/100.
                flux_sum=(leftWeighted + rightWeighted)/2
                wav_sum=(LeftSS[l][0]+RightSS[r][0])/2
                indexINTOsum=np.where(np.isin(wav_sum,wav_binary))
                indexINTObinary=np.where(np.isin(wav_binary,wav_sum))
                if NA (flux_sum[indexINTOsum]/flux_binary[indexINTObinary]).std() 
    return combinations 

#Loading Data from Excel (If there was a an excel file) and if not it will begin finding the possible combinations
#If there is a excel file then assigning its' results to possibleCombinations and asigning it to the 
delta_weight=0
if excelLocation!="None":
    possibleCombinations={}
    exceldataframe=pd.read_excel(excelLocation)
    for i in range(len(exceldataframe)):
        possibleCombinations[(float(exceldataframe.loc[i][0]),float(exceldataframe.loc[i][1]),float(exceldataframe.loc[i][2]),float(exceldataframe.loc[i][3]))]=float(exceldataframe.loc[i][4])
    #To see what is the incridments
    delta_weight=((exceldataframe.loc[2][2])*100-(exceldataframe.loc[1][2])*100)

print("DATA LOADED\n-----------------------------------------------------------\n")
if delta_weight==0:
    delta_weight=float(input('''
-----------------------------------------------------------
Enter the incredment for the weights:
    '''))
    print("Making All Possible Pairs! Depending on how many possible combinations there are this could take awhile")    
    print("SOSA is currently making "+str(float(len(LeftSS))*float(len(RightSS))*100./delta_weight)+" Different Pairs!")
    possibleCombinations = MakingCombinations(LeftSS,RightSS,wav_binary,flux_binary,delta_weight)

stdvalues=sorted([value for value in possibleCombinations.values()],key=float)
pairs=[pair for value in stdvalues for pair in possibleCombinations if possibleCombinations[pair]==value]

