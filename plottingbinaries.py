import matplotlib.pyplot as plt 
import numpy as np
from sklearn import preprocessing
sharedPath = "C:/Users/pirat/Research/SOSA/Binaries/"

wvl1,flux1 = np.loadtxt("C:\\Users\\pirat\\Research\\SOSA\\SS\\6700.txt",unpack= True)
wvl2,flux2 = np.loadtxt("C:\\Users\\pirat\\Research\\SOSA\\SS\\6800.txt",unpack= True)

# HIP10644 = np.loadtxt(sharedPath+'HIP10644/10644a16.txt',unpack=True)
# plt.plot(HIP10644[0],HIP10644[1],label="HIP10644")
# plt.show()


#Does not work because it just normailizes all the points to a value of 1. Which makes sense but that is not what I want
HIP17076 = np.loadtxt(sharedPath+"HIP17076/17076a16.txt",unpack=True)
# HIP17076Flux = HIP17076[1].reshape(-1,1)
# HIP17076Flux = preprocessing.normalize(HIP17076Flux,axis=1)
# plt.plot(HIP17076[0],HIP17076Flux,label="HIP17076")
# plt.show()
# plt.plot(HIP17076[0]+0.21,HIP17076[1],label="HIP17076")
plt.plot(wvl1,flux1,label="SS")
plt.plot(wvl1,flux1)
plt.legend()
plt.show()


# HIP86201=np.loadtxt(sharedPath+"HIP86201\86201a16.txt",unpack=True)
# plt.plot(HIP86201[0],HIP86201[1],label="HIP86201")
# plt.legend()
# plt.show()