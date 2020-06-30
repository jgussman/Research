import numpy as np
import matplotlib.pylab as plt
from PyAstronomy import pyasl



##Create data with a Gaussian absoprtion line

wvl1,flux1 = np.loadtxt("C:\\Users\\pirat\\Research\\SOSA\\SS\\6700.txt",unpack= True)
wvl2,flux2 = np.loadtxt("C:\\Users\\pirat\\Research\\SOSA\\SS\\6800.txt",unpack= True)
bwvl, bflux = np.loadtxt("C:\\Users\\pirat\\Research\\SOSA\\Binaries\\HIP109303\\109303a16.txt",unpack = True)
plt.plot(bwvl,bflux,label="Binary")
plt.legend()
plt.title("Write down what the ranges you want to try for \n each star's vsini and epsilon")
plt.show()
SS  = {6700:[wvl1,flux1]}


#Where to put the vsini in SOSA: 1) Inside the possible combinations function
#All the SS need to be broadened before the go into possible combinations 

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
            
    
    
    


    #return SSwav, pyasl.fastRotBroad(SSwav, SSflux , epsilon , vsini)
 
 
lineBroadSS,rLineBroadSS = CreateLineBroadening({6700:[wvl1,flux1]},{6800:[wvl2,flux2]},bwvl,bflux)
plt.plot(lineBroadSS[(6700,0.2,50.0)][0],lineBroadSS[(6700,0.2,50.0)][1])
plt.show()



#Goals: 
# Try to find a way to cut down of brute forcing the vsini and epislons as much as possible
# Get the PossibleCombinations to run all cores if I want 

#How about before I get he model up and running I get the vsini Stuff done and intorgrated into the model. Because I know that is pivital.



# wvl, bfast = LineBroadening(wvl1,flux1,0.2,50.)



# plt.xlabel("Wvl [A]")
# plt.ylabel("Flux [au]")
# plt.title("Initial spectrum (black), fast (blue), slow (red, shifted)")
# plt.plot(bwvl, bflux, 'k.-')
# plt.plot(wvl-2, bfast, 'b.-')
# plt.show()



