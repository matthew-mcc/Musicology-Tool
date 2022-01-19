'''https://stackoverflow.com/questions/62335385/animating-a-line-plot-over-time-in-python
https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot
https://www.tutorialspoint.com/how-to-animate-a-scatter-plot-in-matplotlib'''

from mollweide_implement import mollweide, latLongGridMollweide
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

markerColor = [ 'b', 'g', 'r', 'c', 'm', 'y', 'dimgray' ]
markerStyle = [ 'o', 'v', 'P', '*', 'D', 'X', '2' ]
bellData = pd.read_csv("dataFiles/touch-all-bells-single-1.csv")
print(bellData)
t0, t1 = 45, 146
fig = plt.figure(figsize=(11.0, 8.5))
ax = fig.add_subplot(111)
for t in range(t0, t1, 2):
    
    bData = bellData[ bellData.time >= t-25 ]
    
    #bData = bData[ bData.time < t+25 ]
    
    lambda0 = 0.0
    plt.gca().cla()
    plt.axis( 'equal' )
    plt.xlim( [-2, 2] )
    plt.ylim( [-1, 1.15] )
    grid = latLongGridMollweide( 4, 8 )
    for gridLine in grid :
        xGrid, yGrid = mollweide( gridLine[:,0], gridLine[:,1], lambda0 )
        plt.plot( xGrid, yGrid, color = [0.8, 0.8, 0.8] )



    bellTypes = list( bellData.type.value_counts().index )
    bellTypes.sort()
    for bellIndex, bellType in enumerate(bellTypes) :
        x0 = bData.x0[ bData.type == bellType ]
        y0 = bData.y0[ bData.type == bellType ]
        z0 = bData.z0[ bData.type == bellType ]
        
        
        lmbda = np.arctan2( y0, x0 )                        
        phi = np.arctan2( z0, np.sqrt( x0**2 + y0**2) )
        
        x, y = mollweide( lmbda, phi, lambda0 )
        
        ax.scatter( x, y, s= 100, marker=markerStyle[bellIndex], edgecolors='0.0', 
                color=markerColor[bellIndex], label=bellType, alpha=0.5 )
    
    ax.legend( )
    
    ax.axis( 'off' )
    plt.show()
    
    

#plt.show()