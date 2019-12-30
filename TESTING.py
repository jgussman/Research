#3D plotting
print("\n-----------------------------------------------------------\n")
eachpairsbeststd=[]
xpos=[]
ypos=[]
dz=[]
print("DELTA WEIGHT")
print(delta_weight)
print(type(delta_weight))
for l in LeftSS:
    for r in RightSS:
        #teffspair=[]
        weightschanging=[]
        for weight in np.arange(delta_weight,100.,delta_weight):
            weight =float(weight)
            weightschanging.append(possibleCombinations[(l,r,weight,(100.-weight))])
            #teffspair.append(str(l)+" "+str(r))
        minstd=min(weightschanging)
        index=weightschanging.index(minstd)
        #split=teffspair[index].split(' ')
        #eachpairsbeststd.append([teffspair[index],minstd])
        xpos.append(l)
        ypos.append(r)
        dz.append(minstd)
        
eachpairsbeststd.sort()