#Testing only using one Synthetic Spectra txt file for both stars 
#   - In order for this to I need to make the code much faster
#   - Figure out how to get the user to pick the wavelength seperation between the two star
#            -One Idea is to just prompt them with the number 
#                - I need to figure out the transulation between their number and python graph
#                - Ask which temps they want to use for the left star and right star
#            -Second Idea: Just have SOSA do it



import numpy as np
import matplotlib.pyplot as plt

wav_binary,flux_binary=np.loadtxt("/home/jgussman/Research/Data/Binaries/HIP94034/94034a16.txt",unpack=True)
wav_binary=np.round(wav_binary,3)
plt.plot(wav_binary,flux_binary)
plt.xlim(6393.23,6396.86)
plt.show()





















