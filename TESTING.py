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
Loading Data...''')
#-----------------------------------Only testing code below
#Putting the SS into a dictionary so they can be called 
LeftSS={} #KEY: Temp of SS, ITEM: ['wavelength','flux'] 
RightSS={} #KEY: Temp of SS, ITEM: ['wavelength','flux'] 

# wavelengthShift = float(input("The wavelength difference for the two stars(In angstroms): "))
# lengthofTxtFile = 0
# numberofdecimals = str(wavelengthShift)[::-1].find('.')
# indexforShift = int(wavelengthShift * eval('1000000'[0:numberofdecimals+1]))
# decimalplaces=0 #for binary
# Leftstar = 0 
# for data in listdir(ssLocation):
#     if lengthofTxtFile ==0:
#         lengthofTxtFile = len(np.loadtxt(ssLocation+data,unpack=True)[0])
        
#     LeftSS[int(data[:4])]=[np.loadtxt(ssLocation+data,unpack=True)[0]+wavelengthShift,np.loadtxt(ssLocation+data,unpack=True)[1]]
#     LeftSS[int(data[:4])]=[LeftSS[int(data[:4])][0][indexforShift:],LeftSS[int(data[:4])][1][indexforShift:]]
#     Leftstar = int(data[:4])
#     RightSS[int(data[:4])]=[np.loadtxt(ssLocation+data,unpack=True)[0][:lengthofTxtFile-indexforShift],
#                                 np.loadtxt(ssLocation+data,unpack=True)[1][:lengthofTxtFile-indexforShift]]
# decimalplaces = str(LeftSS[Leftstar][0][0])[::-1].find('.')
print('Hope you are having a great day! :D')

def LoadInSS(FolderLocation,delta_lambda):
    '''
    Input: String SS Folder Path, float wavelength seperation  
    Output: [Files to use for the left star, Files to use for the right star]
    '''
    filenames = [name for name in listdir(FolderLocation)] #Extracting the file names 
    # def WhichFilesToUse(filelist):
    #     '''
    #     Input: List of strings that are the names of the files in the given SS location
    #     Output: []
    #     '''
    for i in range(0,len(filenames)): #Displaying all the file names nicely so the user can pick which to use
        pass

    listofFilesForLeftStar = list(map(int, input("Enter a multiple value: ").split())) 
        



LoadInSS(ssLocation,1)