print("SOSA means 'Synthetic & Observed Spectra  Analyzer'")
print('''                                       ******READ THIS******
      The purpose of this program is to find Synthetic Spectra (SS) pairs that match accurately with an observed 
binary"+str("'s")+" spectra.\n\n2.For this program to be successful you must run it using python 3!


                              *****Making Sure This Runs Smoothly***** 
     n0. H I highly suggest that you only have the SS you want to use in the file location. 
     1. The way this program chooses which SS is for the Left star in the binary and which is for the right star is by
     looking at the files"+str("'")+" name.\n       
     1.1 It looks if the file name has (l or L) as the first character signifing that it is the left star. Vis Versa 
     for the right analog. It also looks if the last 4 characters in the name is .txt        
     1.2 the second through fith characters need to be the Temperture of that SS. This means if your SS temp goes 
     above 9999 or below 1000 you will get a strange result.   
          An example of a good Left SS name is L6500.txt           
          An example of a good Right SS name is R5700.txt
     2. Make sure there is no header in the SS or the observed.''')
 
    
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
locationsComplete=""
print('''
-----------------------------------------------------------
Do you already have the excel file of possible combinations you want to work with? (Yes/No)''')
while not locationsComplete:
    haveCombinations=input("Your answer: ")
    excelLocationFound='' #This needs to be outside here so later in the SOSA it can see if there is a excel file or not.
    if haveCombinations.lower()=='yes':
        #Getting the excel file Location
        print('''
        -----------------------------------------------------------
              Enter the path to the excel file. 
              EXAMPLE:/home/jgussman/Research/Combinations/HIP86201SS.xls''')
        while not excelLocationFound:
            excelLocation=input("\nYours: ")
            if  not path.exists(excelLocation):
                print("This location does NOT exist! Try again!")
            else:
                excelLocationFound='\nExcel File Path: '+excelLocation
                
                
        #Getting the Synethic Spectra Location
        print('''
        -----------------------------------------------------------
        Enter the path to the folder that contains all your SS 
        EXAMPLE: /home/jgussman/Research/Binaries/Data/SS/''')
        ssLocationFound=''
        while not ssLocationFound:
            ssLocation=input("\nYours:  ")
            if ssLocation[len(ssLocation)-1]!='/': #In case the user forgets to put the \ at the end of the path 
                ssLocation=ssLocation+"/"
                if not path.exists(ssLocation):
                    print("This location does NOT exist! Try again!")
                else:
                    ssLocationFound="Synethic Spectra Folder Path: "+ssLocation
            elif not path.exists(ssLocation):
                    print("This location does NOT exist! Try again!")
            else:
                ssLocationFound="Synethic Spectra Folder Path: "+ssLocation
                
                
        #Getting the Binary Spectra Location
        print('''
        -----------------------------------------------------------
              Enter the path to your Observed Binary Spectra! 
              EXAMPLE: /home/jgussman/Research/Binaries/Data/Binaries/HIP86201.txt''')
        binaryLocationFound=''
        while not binaryLocationFound:
            binaryLocation=input("\nYours:  ")
            if not path.exists(binaryLocation):
                print("This location does NOT exist! Try again!")
            else:
                binaryLocationFound='Binary Star Spectra File Path: '+binaryLocation
                
                
            
        locationsComplete='''
        -----------------------------------------------------------
        All Locations have been found!'''
        print(locationsComplete)
        print(excelLocationFound)
        print(ssLocationFound)
        print(binaryLocationFound)
#If they are trying new combations of a binary and SS
    elif haveCombinations.lower()=='no':
         #Getting the Synethic Spectra Location
        print("\n-----------------------------------------------------------\nEnter the path to the folder that contains all your SS \nex: /home/jgussman/Research/Binaries/Data/SS/")
        ssLocationFound=''
        while not ssLocationFound:
            ssLocation=input("\nYours:  ")
            if ssLocation[len(ssLocation)-1]!='/': #In case the user forgets to put the \ at the end of the path 
                ssLocation=ssLocation+"/"
                if not path.exists(ssLocation):
                    print("This location does NOT exist! Try again!")
                else:
                    ssLocationFound="Synethic Spectra Folder Path: "+ssLocation
            elif not path.exists(ssLocation):
                    print("This location does NOT exist! Try again!")
            else:
                ssLocationFound="Synethic Spectra Folder Path: "+ssLocation
              
                
        #Getting the Binary Spectra Location
        print('''
        -----------------------------------------------------------
        Enter the path to your binary Spectra! 
        EXAMPLE: /home/jgussman/Research/Binaries/Data/Binaries/HIP86201.txt''')
        binaryLocationFound=''
        while not binaryLocationFound:
            binaryLocation=input("\nYours:  ")
            if not path.exists(binaryLocation):
                print("This location does NOT exist! Try again!")
            else:
                binaryLocationFound='Binary Star Spectra File Path: '+binaryLocation
                
                
            
        locationsComplete="\n-----------------------------------------------------------\nAll Locations have been found!"
        print(locationsComplete)
        print(excelLocationFound)
        print(ssLocationFound)
        print(binaryLocationFound)
    else:
        print("***Invalid Respose***\nPlease enter yes or no!")

#Loading Data.
print("\n-----------------------------------------------------------\nLoading Data...")
#SOSA will not work if the the starting and ending wavelengths of the SS are different. So this fixes that.  
foundAleftss=0
foundArightss=0
while (foundAleftss+foundArightss)!=2: 
    for data in listdir(ssLocation):
            if ((data[0]=='L') or (data[0]=='l')) and (data[len(data)-4:]=='.txt') and (foundAleftss!=1):
                Left=np.loadtxt(ssLocation+data,unpack=True)[0]
                foundAleftss=1
            elif ((data[0]=='R') or (data[0]=='r')) and (data[len(data)-4:]=='.txt') and (foundArightss!=1):
                Right=np.loadtxt(ssLocation+data,unpack=True)[0]
                foundArightss=1
diffWavLeft=np.where(Left==Right[0])[0][0]
decimalplaces=len(str(Left[0]))-1-str(Left[0]).find('.') #Assuming the SS have less decimal places than the observed 

#Putting the SS into a dictionary so they can be called 
LeftSS={} #KEY: Temp of SS, ITEM: ['wavelength','flux'] 
RightSS={} #KEY: Temp of SS, ITEM: ['wavelength','flux'] 

for data in listdir(ssLocation): 
    if ((data[0]=='L') or (data[0]=='l')) and (data[len(data)-4:]=='.txt'): #If you have the same temp but a different paramter is changed. This is where you can come into the code and change what the code looks for in the title. 
        LeftSS[int(data[1:5])]=[np.loadtxt(ssLocation+data,unpack=True)[0][diffWavLeft:],
                                np.loadtxt(ssLocation+data,unpack=True)[1][diffWavLeft:]]
    elif ((data[0]=='R') or (data[0]=='r')) and (data[len(data)-4:]=='.txt'):
        diffWavRight=len(Right)-diffWavLeft
        RightSS[int(data[1:5])]=[np.loadtxt(ssLocation+data,unpack=True)[0][:diffWavRight],
                                np.loadtxt(ssLocation+data,unpack=True)[1][:diffWavRight]]
print('Hope you are having a great day! :D')

#Loading the Binary Spectra
wav_binary,flux_binary=np.loadtxt(binaryLocation,unpack=True)
wav_binary=np.round(wav_binary,decimalplaces)

#Loading Data from Excel (If there was a an excel file) and if not it will begin finding the possible combinations
#If there is a excel file then assigning its' results to possibleCombinations and asigning it to the 
delta_weight=0
if excelLocationFound:
    possiblecombinations={}
    exceldataframe=pd.read_excel(excelLocation)
    for i in range(len(exceldataframe)):
        possiblecombinations[(float(exceldataframe.loc[i][0]),float(exceldataframe.loc[i][1]),float(exceldataframe.loc[i][2]),float(exceldataframe.loc[i][3]))]=float(exceldataframe.loc[i][4])
    #To see what is the incridments
    #if 
    delta_weight=((exceldataframe.loc[2][2])*100-(exceldataframe.loc[1][2])*100)
print("DATA LOADED\n-----------------------------------------------------------\n")

possibleCombinations={}
def MakingCombinations(LeftSS,RightSS,wav_binary,delta_weight):
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
                possibleCombinations[((l,r,weight/100.,(100.-weight)/100))]=(flux_sum[indexINTOsum]/flux_binary[indexINTObinary]).std()  

if delta_weight==0:
    delta_weight=float(input('''Enter the incredment for the weights: 
    Common weight is: 0.001'''))
print("Making All Possible Pairs! Depending on how many possible combinations there are this could take awhile")    
print("SOSA is currently making "+str(float(len(LeftSS))*float(len(RightSS))*100./delta_weight)+" Different Pairs!")
if excelLocationFound:
    MakingCombinations(LeftSS,RightSS,wav_binary,delta_weight)
else:
    
    MakingCombinations(LeftSS,RightSS,wav_binary,delta_weight)
stdvalues=sorted([value for value in possibleCombinations.values()],key=float)
pairs=[pair for value in stdvalues for pair in possibleCombinations if possibleCombinations[pair]==value]

####WRITING TO EXCEL
#DONT DONE WORKING ON 
if not excelLocationFound:
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
                        sheet1.write(row, 4, possibleCombinations[(l,r,weight/100.,(100-weight)/100.)]) #******the the rounding to 3 decimals wont work for everything Jude 
                        row+=1

            whattocalltheexcelfile=input("\n This file will be created where this code is running.What you you like to call this excel file?\n")+'.xls'
            print("\n Excel File Name: "+whattocalltheexcelfile)
            wb.save(whattocalltheexcelfile)
        elif makeAnExcelFile.lower()=='no':
            print('No excel file will be made!')
        else:
            print("***Invalid Response***")
            makeAnExcelFile=''
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
    whattosay="Which pair do you want to look at overplotted with the binary's spectra?\nThere are "+str(len(pairs))+" to choose from.\n1 being the best and "+str(len(pairs))+" being the worse pair. "
    pairnumber=int(input(whattosay))
    leftStartemp=pairs[pairnumber-1][0]
    rightStartemp=pairs[pairnumber-1][1]
    lw=pairs[pairnumber-1][2]
    rw=pairs[pairnumber-1][3]
    wav_sum=(LeftSS[leftStartemp][0]+RightSS[rightStartemp][0])/2
    flux_sum=(LeftSS[leftStartemp][1]*lw+RightSS[rightStartemp][1]*rw)
    title='Left Star:'+str(leftStartemp)+'K  Weight: '+str(lw*100)+"%\nRight Star: "+str(rightStartemp)+"K  Weight: "+str(rw*100)+"%"
    plt.title(title)
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
print("\n-----------------------------------------------------------\nSOSA has now ended!")
