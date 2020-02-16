import numpy as np
import matplotlib.pylab as plt
from PyAstronomy import pyasl


# Create data with a Gaussian absoprtion line

wvl,flux = np.loadtxt("C:\\Users\\pirat\\Research\\SOSA\\Testing\\6700.txt",unpack= True)
bwvl, bflux = np.loadtxt("C:\\Users\\pirat\\Research\\SOSA\\Binaries\\HIP109303\\109303a16.txt",unpack = True)

# Apply the fast algorithm and ...
bfast = pyasl.fastRotBroad(wvl, flux, 0.0, 50)


plt.xlabel("Wvl [A]")
plt.ylabel("Flux [au]")
plt.title("Initial spectrum (black), fast (blue), slow (red, shifted)")
plt.plot(bwvl, bflux, 'k.-')
plt.plot(wvl, bfast, 'b.-')
plt.show()


def LineBroadening(SSwav,SSflux):
    '''
    Input: Synethic Spectra's wavelength (Make sure they are evenly spaced,numpy array), Synethic Spectra's flux (numpy array)
    Output: Line Broadened wav, flux (Both numpy array) 
    '''
    