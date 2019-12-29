import numpy as np
import sys
import pandas as pd 
from astropy.table import Table, Column, MaskedColumn
from astropy.io import ascii


# o = np.array([6500,6700,.10,.90,0.0025,4400,5200,.50,.50,0.00243])
# l = np.array([6500,4400])
# r = np.array([6700,5200])
# lw = np.array([0.1,0.5])
# rw = np.array([0.9,0.5])
# std = np.array([0.0025,0.00243])
# data = Table([l,r,lw,rw,std])
# ascii.write(data,"test.asc")


l = [map(lambda x: x[0][0],sortedbestpairs)]
r = [map(lambda x: x[0][1],sortedbestpairs)]
lw = [map(lambda x: x[0][2],sortedbestpairs)]
rw = [map(lambda x: x[0][3],sortedbestpairs)]
std = [map(lambda x: x[1],sortedbestpairs)]
ascii.write(Table(l,r,lw,rw,std),"name.asc")
l,r,lw,rw,std = np.loadtxt("test.asc",unpack=True)
possibleCombinations=dict(list(map(lambda l,r,lw,rw,std: ((l,r,lw,rw),std),l,r,lw,rw,std)))
delta_weight = float(lw[1]-lw[0])

print(possibleCombinations)
print(delta_weight)
