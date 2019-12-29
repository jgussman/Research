print("SOSA means 'Synthetic & Observed Spectra  Analyzer'")
print('''                                 ******READ THIS******
      The purpose of this program is to find Synthetic Spectra (SS) pairs that match accurately with an observed 
          binary"+str("'s")+" spectra.\n\n2.For this program to be successful you must run it using python 3!
                              *****Making Sure This Runs Smoothly***** 
     n0. I highly suggest that you only have the SS you want to use in the file location. 
     1. The way this program chooses which SS is for the Left star in the binary and which is for the right star is by
     looking at the files"+str("'")+" name.\n       
     1.1 It looks if the file name has (l or L) as the first character signifing that it is the left star. Vis Versa 
     for the right analog. It also looks if the last 4 characters in the name is .txt        
     1.2 the second through fith characters need to be the Temperture of that SS. This means if your SS temp goes 
     above 9999 or below 1000 you will get a strange result.   
          An example of a good Left SS name is L6500.txt           
          An example of a good Right SS name is R5700.txt
     2. Make sure there is no header in the SS or the observed.
     3. You must choose at least 3 SS files for the left and right stars''')
 
    
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
from astropy.table import Table, Column, MaskedColumn
from astropy.io import ascii


def FileLocations():
    '''
    Input: None
    Output: A tuple of strings (SS Folder Path if have,Binary File Path,Excel File Path if have)
    '''
    binarypath = BinaryFileQuestion()
    haveExcelFilequestion = input('''
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
    Output: String of Excel file path
    '''
    print('''
-----------------------------------------------------------
Enter the path to the excel file. 
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
    left star and right star dictionaries will be "None" if existingLoc is NOT "None" because that means you don't need to create new pairs
    Possible Combinations will be "None" if existingLoc is "None" and delta weight will = 0
    '''
    #Loading Data from Excel or ascii (If there was a an excel file) 
    delta_weight=0
    possibleCombos={}
    if existingLoc!="None":
        LSS,RSS = ("None","None")
        if existingLocation[-4:]==".xls":
            exceldataframe=pd.read_excel(excelLocation)
            for i in range(len(exceldataframe)):
                possibleCombos[(float(exceldataframe.loc[i][0]),float(exceldataframe.loc[i][1]),float(exceldataframe.loc[i][2]),float(exceldataframe.loc[i][3]))]=float(exceldataframe.loc[i][4])
            #To see what is the incridments
            delta_weight=((exceldataframe.loc[2][2])*100-(exceldataframe.loc[1][2])*100)
        elif existingLocation[-4:]==".asc":
            l,r,lw,rw,std = np.loadtxt("test.asc",unpack=True)
            possibleCombos=dict(list(map(lambda l,r,lw,rw,std: ((l,r,lw,rw),std),l,r,lw,rw,std)))
            delta_weight = float(lw[1]-lw[0]) 
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

        wav_bi,flux_bi=np.loadtxt(binaryLoc,unpack=True)
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
                combinations[((l,r,weight/100.,(100.-weight)/100))]=(flux_sum[indexINTOsum]/flux_binary[indexINTObinary]).std()  
    return combinations 



print("DATA LOADED")
if delta_weight==0:
    delta_weight=float(input('''
-----------------------------------------------------------
Enter the incredment for the weights:
    '''))
    print("Making All Possible Pairs! Depending on how many possible combinations there are this could take awhile")    
    numberofpairs = float(len(LeftSS))*float(len(RightSS))*100./delta_weight
    print("SOSA is currently making "+str(numberofpairs)+" Different Pairs!")
    possibleCombinations = MakingCombinations(LeftSS,RightSS,wav_binary,flux_binary,delta_weight)


pairs=sorted(possibleCombinations.items(), key = lambda kv:(kv[1], kv[0])) #The pair at the 0th index is the best matched to the observed spectra




print("\n-----------------------------------------------------------\n")

eachpairsbeststd=[]
xpos=[]
ypos=[]
dz=[]
for l in LeftSS:
    for r in RightSS:
        #teffspair=[]
        weightschanging=[]
        for weight in np.arange(delta_weight,100.,delta_weight):
            weightschanging.append(possibleCombinations[(l,r,weight/100.,(100.-weight)/100.)])
            #teffspair.append(str(l)+" "+str(r))
        minstd=min(weightschanging)
        index=weightschanging.index(minstd)
        #split=teffspair[index].split(' ')
        #eachpairsbeststd.append([teffspair[index],minstd])
        xpos.append(l)
        ypos.append(r)
        dz.append(minstd)
        
eachpairsbeststd.sort()

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_trisurf(xpos, ypos, dz, cmap=cm.jet, linewidth=0.9)
plt.xlabel("Temperture(Kelvin)")
plt.ylabel("Temperture(Kelvin)")
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

####WRITING TO EXCEL
if existingLocation=="None":
    storeAnswer = input("Would you like to store your Combinations in an Ascii File or Excel File?(No,Ascii,Excel)")
    if storeAnswer.lower()=="excel":
        if (numberofpairs>65500):
            print("The number of pairs is over 65500. Therefore you can not create an excel file")
        else:
            print("Would you like to put your Combinations in an excel file?")
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
        l = [map(lambda x: x[0][0],sortedbestpairs)]
        r = [map(lambda x: x[0][1],sortedbestpairs)]
        lw = [map(lambda x: x[0][2],sortedbestpairs)]
        rw = [map(lambda x: x[0][3],sortedbestpairs)]
        std = [map(lambda x: x[1],sortedbestpairs)]
        whattocall = input("What would you like to call the Ascii file?")
        whattocall +=".asc"
        ascii.write(Table(l,r,lw,rw,std),whattocall)
    else:
        print("Pairs were not stored")

print("\n-----------------------------------------------------------\nSOSA has now ended!")