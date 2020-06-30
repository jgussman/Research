print("SOSA means 'Synthetic & Observed Spectra  Analyzer'")
print('''                                 ******READ THIS******
      The purpose of this program is to find Synthetic Spectra (SS) pairs that match accurately with an observed 
          binary"+str("'s")+" spectra.
          2.For this program to be successful you must run it using python 3!
                              *****Making Sure This Runs Smoothly***** 
     ''')
 
    
#Loading in Packages that are necessary for SOSA to run
import numpy as np
from os import listdir
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import xlwt
from xlwt import Workbook
from os import path
import pandas as pd 
from astropy.table import Table, Column, MaskedColumn
from astropy.io import ascii
from PyAstronomy import pyasl


def FileLocations():
    '''
    Input: None
    Output: A tuple of strings (SS Folder Path if have,Binary File Path,Excel File Path if have)
    '''
    binarypath = BinaryFileQuestion()
    haveExistingFilequestion = input('''
-----------------------------------------------------------
Do you have previously generated SS that you would like to use? (Y/N)''')
    if haveExistingFilequestion.lower() in ['yes','y']:
        existingpath = ExistingFileQuestion()
        return ("None",binarypath,existingpath)
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

def ExistingFileQuestion(): 
    '''
    Input: None
    Output: String of Ascii/Excel file path
    '''
    print('''
-----------------------------------------------------------
Enter the path to the ascii/excel file. 
    EXAMPLE:/home/jgussman/Research/Combinations/HIP86201SS.xls''')
    while True:
        Location=input("\nYours: ")
        if  not path.exists(Location):
            print("This location does NOT exist! Try again!")
        else:
            print("Excel File Path Found!")
            return Location                                                    
                
ssLocation, binaryLocation, existingLocation = FileLocations()

#Loading Data.
print('''
-----------------------------------------------------------
Loading Data...
''')

def LoadInData(FolderLocation,existingLoc,binaryLoc):
    '''
    Input: String SS Folder Path, float wavelength seperation  
    Output: Dic of SS for left Star, Dic of SS for Right Star, Array of Binary's Wavelength, Array of Binary's Flux, Possible Combinations, difference in Weight
    Dictionaries; KEY: Temp of SS, ITEM: ['wavelength','flux']
    left star and right star dictionaries will be have the Temps as keys but "NA" for the items if existingLoc is NOT "None" because that means you don't need to create new pairs
    Possible Combinations will be "None" if existingLoc is "None" and delta weight will = 0
    '''
    wav_bi,flux_bi=np.loadtxt(binaryLoc,unpack=True)
    #Loading Data from Excel or ascii (If there was a an excel file) 
    delta_weight=0
    possibleCombos,LSS,RSS={},{},{}
    if existingLoc!="None":
        LSS,RSS = ("None","None")
        if existingLocation[-4:]==".xls":
            LeftList,RightList = [],[]
            exceldataframe=pd.read_excel(existingLoc)
            for i in range(len(existingLoc)):
                possibleCombos[(float(exceldataframe.loc[i][0]),float(exceldataframe.loc[i][1]),float(exceldataframe.loc[i][2]),float(exceldataframe.loc[i][3]))]=float(exceldataframe.loc[i][4])
                if ((float(exceldataframe.loc[i][0]),"NA")) not in LeftList:
                    LeftList.append((float(exceldataframe.loc[i][0]),"NA"))
                if (float(exceldataframe.loc[i][1]),"NA") not in RightList:
                    RightList.append((float(exceldataframe.loc[i][1]),"NA"))
            #To see what is the incridments
            delta_weight=((exceldataframe.loc[2][2])*100-(exceldataframe.loc[1][2])*100)
            LSS = dict(list(LeftList)) #This has not been tested yet
            RSS = dict(list(RightList)) #This has not been tested yet
        elif existingLocation[-4:]==".asc":
            try:
                l,r,lw,rw,std = np.loadtxt(existingLoc,unpack=True,skiprows=0)  #In case there isn't a header i.e. the user removed it 
            except:
                l,r,lw,rw,std = np.loadtxt(existingLoc,unpack=True,skiprows=1) 
            
            keys = list(map(lambda w,x,y,z: (w,x,y,z),l,r,lw,rw))
            keysandvalues = list(map(lambda x,y: (x,y), keys, std))
            possibleCombos = dict(keysandvalues)
            print(lw[0])
            print(lw[1])
            print(str(float(lw[0]))[::-1].find('.'))
            decimalplaces = str(float(lw[0]))[::-1].find('.')
            delta_weight = round(float(lw[0])-float(lw[1]),decimalplaces)*100
            LSS = dict(list(map(lambda x,y: (x,y),l,["NA"]*len(l))))
            RSS = dict(list(map(lambda x,y: (x,y),r,["NA"]*len(r))))

    else:
        filenames = [name for name in listdir(FolderLocation)] #Extracting the file names 
        for i in range(len(filenames)): #Displaying all the file names nicely so the user can pick which to use
            print(str(i)+": "+ filenames[i])
            
        listofFilesForLeftStar = list(map(int, input('''
Type in the number/s seperated by spaces corresponding to the Synthetic Spectra files you want to be used for the Left star.
Example: 1 3 5 6
Your Answer: ''').split())) 
        listofFilesForRightStar = list(map(int, input('''
Type in the number/s seperated by spaces corresponding to the Synthetic Spectra files you want to be used for the Right star.
Example: 0 2 7 10 11
Your Answer: ''').split())) 

        leftSStoUse = [filenames[i] for i in listofFilesForLeftStar]
        rightSStoUse = [filenames[j] for j in listofFilesForRightStar]

        
        input("SOSA is about to display the observed spectra so you can determine the wavelength seperation of the two stars. If you are ready press enter")
        plt.plot(wav_bi, flux_bi)
        plt.xlabel("Angstrom")
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
    binary_shift_question = input("Do you need to shift your binary spectra's wavelength?(Y/N)")
    if binary_shift_question.lower() in ['y','yes']:
        binary_shift = float(input("Enter the number (In angstroms) of how much you would like to shift your binary"))
        wav_bi += binary_shift
    return (LSS,RSS,wav_bi,flux_bi,possibleCombos,delta_weight)
        
LeftSS,RightSS, wav_binary, flux_binary,possibleCombinations,delta_weight= LoadInData(ssLocation,existingLocation,binaryLocation)

def CreateLineBroadening(LeftSS,RightSS,bWav,bFlux):
    '''
    Input: {Temp of Left SS : ['wavelength','flux']} , {Temp of Right SS : ['wavelength','flux']}, {wavelengths of binary : fluxes of binary}
    Output: {(Temp of Left SS,epislon,vsini) : ['wavelength','flux']} , {(Temp of Right SS,epsilon,vsini) : ['wavelength','flux']} ALL LINEBROADEN
    Using:  pyasl.fastRotBroad from the PyAstronomy package 
    '''
    plt.plot(bWav,bFlux,label="Binary")
    plt.legend()
    plt.title("Write down what the ranges you want to try for \n each star's vsini and epsilon")
    plt.show()

    leftStarVSINIrange = input("Please enter the range you want to look for the vsini of the LEFT star: \n ex: start,stop,step\n").split(",")
    leftStarVSINIrange = [float(i) for i in leftStarVSINIrange]
    leftStarEPSILONrange = input("Please enter the range you want to look for the epsilon of the LEFT star: \n ex: start,stop,step\n").split(",")
    leftStarEPSILONrange = [float(i) for i in leftStarEPSILONrange]
    rightStarVSINIrange = input("Please enter the range you want to look for the vsini of the RIGHT star: \n ex: start,stop,step\n").split(",")
    rightStarVSINIrange = [float(i) for i in rightStarVSINIrange]
    rightStarEPSILONrange = input("Please enter the range you want to look for the epsilon of the RIGHT star: \n ex: start,stop,step\n").split(",")
    rightStarEPSILONrange = [float(i) for i in rightStarEPSILONrange]
    print(''''
            SOSA is now making all the different SS models based on the ranges given...
                    This is could take a bit. Sit back, relax, and enjoy some Lofi''')
    def lineBroaden(dic,epislonRange,vsiniRange):
        returndic = {}
        for temp in dic:
            for epsilon in np.arange(epislonRange[0],epislonRange[1],epislonRange[2]):
                for vsini in np.arange(vsiniRange[0],vsiniRange[1],vsiniRange[2]):
                    wvl, flux = dic[temp][0], pyasl.fastRotBroad(dic[temp][0], dic[temp][1] , epsilon , vsini)
                    PrecentOfLen = int(len(wvl)*0.025) #The fluxes at each end of the broadened wavelengths needs to be removed **THIS IS IMPORTANT**
                    orgiLen = len(wvl)
                    wvl = wvl[PrecentOfLen:len(wvl)-PrecentOfLen]
                    flux = flux[PrecentOfLen:orgiLen-PrecentOfLen]
                    returndic[(temp,epsilon,vsini)] = [wvl,flux]
        return returndic
    return lineBroaden(LeftSS,leftStarEPSILONrange,leftStarVSINIrange),lineBroaden(RightSS,rightStarEPSILONrange,rightStarVSINIrange)

if LeftSS != "None":
    broadenSpectraQuestion = input("Would you like to Line Broaden your spectrums?(y/n)")
    if(broadenSpectraQuestion[0].lower()=='y'):
        LeftSS,RightSS = CreateLineBroadening(LeftSS,RightSS,wav_binary,flux_binary)
    else:
        print("You have chosen to not Line Broaden\n"+"-"*25)
#Make Combinations
def MakingCombinations(LeftSS,RightSS,wav_binary,flux_binary,delta_weight):
    '''
    Input: {Temp of Left SS : ['wavelength','flux']} , {Temp of Right SS : ['wavelength','flux']}, {wavelengths of binary : fluxes of binary} , incredment for the weight 
    Output: {(Left SS Temp,Right SS Temp, Left SS Weight, Right SS Weight : Standard deviation from the observed spectra}
    '''
    combinations={}
    weightrange = np.arange(delta_weight,100,delta_weight)
    for l in LeftSS:
        for r in RightSS:
            wav_sum=(LeftSS[l][0]+RightSS[r][0])/2
            indexINTOsum=np.where(np.isin(wav_sum,wav_binary))
            indexINTObinary=np.where(np.isin(wav_binary,wav_sum)) 
            for weight in weightrange:
                weight=float(weight)
                leftWeighted=LeftSS[l][1]*weight/100.
                rightWeighted=RightSS[r][1]*(100.-weight)/100.
                flux_sum=(leftWeighted + rightWeighted)/2
                combinations[((l,r,weight/100.,(100.-weight)/100))]=(flux_sum[indexINTOsum]/flux_binary[indexINTObinary]).std()  
    return combinations 

print("DATA LOADED")
if delta_weight==0:
    delta_weight=float(input('''
-----------------------------------------------------------
Enter the incredment for the weights (Most common is 0.1%):
    '''))
    print("Making All Possible Pairs! Depending on how many possible combinations there are this could take awhile")    
    numberofpairs = float(len(LeftSS))*float(len(RightSS))*100./delta_weight
    print("SOSA is currently making "+str(numberofpairs)+" Different Pairs!")
    possibleCombinations = MakingCombinations(LeftSS,RightSS,wav_binary,flux_binary,delta_weight)

pairs=sorted(possibleCombinations.items(), key = lambda kv:(kv[1], kv[0])) #The pair at the 0th index is the best matched to the observed spectra

#3D plotting
print("\n-----------------------------------------------------------\n")
xpos=[]
ypos=[]
dz=[]
for l in LeftSS:
    for r in RightSS:
        #teffspair=[]
        weightschanging=[]
        for weight in np.arange(delta_weight,100.,delta_weight):
            weight = float(weight)
            weightschanging.append(possibleCombinations[(l,r,weight/100.,(100.-weight)/100.)])
        minstd=min(weightschanging)
        index=weightschanging.index(minstd)
        if type(l)==int:
            xpos.append(l)
            ypos.append(r)
            dz.append(minstd)
        else:
            xpos.append(l[0])
            ypos.append(r[0])
            dz.append(minstd)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_trisurf(xpos, ypos, dz, cmap=cm.jet, linewidth=0.9)
plt.xlabel("Left Temp(Kelvin)")
plt.ylabel("Right Temp(Kelvin)")
plt.show()
save3dplot=input("Would you like to save this plot? (Yes/No): ")
if save3dplot.lower()=='yes':
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(xpos, ypos, dz, cmap=cm.jet, linewidth=0.9)
    whattocallplot=input('What would you like to call this plot: ')
    plt.savefig(whattocallplot)
    print("Plot has been saved as "+whattocallplot+'.png')
else:
    print("\nPlot was not Saved!")
print("\n-----------------------------------------------------------\n")
#Overplotting
if(existingLocation=="None"):
    keepgoing='yes'
    while keepgoing.lower()!='no':
        whattosay='''
    Which pair do you want to look at overplotted with the binary's spectra?\nThere are '''+str(len(pairs))+''' to choose from.
    1 being the best and '''+str(len(pairs))+''' being the worse pair. '''
        pairnumber=int(input(whattosay))
        leftStartemp=pairs[pairnumber-1][0][0]
        rightStartemp=pairs[pairnumber-1][0][1]
        lw=pairs[pairnumber-1][0][2]
        rw=pairs[pairnumber-1][0][3]
        wav_sum=(LeftSS[leftStartemp][0]+RightSS[rightStartemp][0])/2
        flux_sum=(LeftSS[leftStartemp][1]*lw+RightSS[rightStartemp][1]*rw)
        title='Left Star:'+str(leftStartemp)+'K  Weight: '+str(lw*100)+"%\nRight Star: "+str(rightStartemp)+"K  Weight: "+str(rw*100)+"%"
        plt.title(title)
        plt.xlabel("Angstrom")
        plt.plot(wav_binary,flux_binary,'black')
        plt.plot(wav_sum,flux_sum,'r--')
        plt.legend(['Observed','Synthetic'])
        plt.show()
        savethisoverplot=input("Would you like to save this overplot? (Yes/No): ")
        if savethisoverplot.lower()=='yes':
            title='Left Star:'+str(leftStartemp)+'K  Weight: '+str(lw*100)+"%\nRight Star: "+str(rightStartemp)+"K  Weight: "+str(rw*100)+"%"
            plt.title(title)
            plt.plot(wav_binary,flux_binary,'black')
            plt.plot(wav_sum,flux_sum,'r--')
            plt.legend(['Observed','Synthetic'])
            whattocallit=input("What would you like to call this plot? ")
            plt.savefig(whattocallit)
            print('Image has been saved as '+whattocallit+'.png\n')
        keepgoing=input("Would you like to plot some more pairs? (Yes/No): ")
else:
    print("Overplotting from exel and Ascii files is unsupported at this time!")
####WRITING TO EXCEL
if existingLocation=="None":
    storeAnswer = input('''
-----------------------------------------------------------   
Would you like to store your Combinations in an Ascii File or Excel File?(No,Ascii,Excel)''')
    if storeAnswer.lower()=="excel":
        if (numberofpairs>65500):
            print("The number of pairs is over 65500. Therefore you can not create an excel file")
        else:
            makeAnExcelFile=''
            excelFilemade=''
            while not makeAnExcelFile:
                makeAnExcelFile=input('Yes or No\n')
                if makeAnExcelFile.lower()=='yes':
                    wb = Workbook() 
                    # add_sheet is used to create sheet. 
                    sheet1 = wb.add_sheet('Sheet 1') 
                    sheet1.write(0,0, "LEFT TEMP")
                    sheet1.write(0,1,'RIGHT TEMP')
                    sheet1.write(0,2,"LEFT WEIGHT")
                    sheet1.write(0,3, "RIGHT WEIGHT")
                    sheet1.write(0,4, "Standard Dev")
                    row=1 
                    col=1
                    for l in LeftSS:
                        for r in RightSS:
                            for weight in np.arange(delta_weight,100.,delta_weight):                        
                                sheet1.write(row, 0, l)
                                sheet1.write(row, 1, r)
                                sheet1.write(row, 2, weight/100.)
                                sheet1.write(row, 3, (100-weight)/100.)
                                sheet1.write(row, 4, possibleCombinations[(l,r,weight/100.,(100-weight)/100.)]) 
                                row+=1
                    whattocalltheexcelfile=input("\n This file will be created where this code is running.What you you like to call this excel file?\n")+'.xls'
                    print("\n Excel File Name: "+whattocalltheexcelfile)
                    wb.save(whattocalltheexcelfile)
    elif(storeAnswer.lower() == "ascii"):
        l = list(map(lambda x: x[0][0],pairs))
        r = list(map(lambda x: x[0][1],pairs))
        lw = list(map(lambda x: x[0][2],pairs))
        rw = list(map(lambda x: x[0][3],pairs))
        std = list(map(lambda x: x[1],pairs))
        whattocall = input("What would you like to call the Ascii file?")
        whattocall +=".asc"
        data = Table([l,r,lw,rw,std],names=["L_Temp","R_Temp","L_Weight","R_Weight","Standard Dev"])
        ascii.write(data,whattocall)
    else:
        print("Pairs were not stored")

print("\n-----------------------------------------------------------\nSOSA has now ended!")