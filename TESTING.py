import numpy as np
from os import path
import matplotlib.pyplot as plt
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

wav_bi94,flux_bi94=np.loadtxt(BinaryFileQuestion(),unpack=True) 
wav_bi86,flux_bi86=np.loadtxt(BinaryFileQuestion(),unpack=True) 

plt.plot(wav_bi94,flux_bi94,"b")
plt.plot(wav_bi86,flux_bi86,"y")
plt.show()
