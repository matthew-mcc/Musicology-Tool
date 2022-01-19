import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def mollweide( lmbda, phi, lmbda0 = 0.0 ) :

    """
    Compute Mollweide equal area project for az/el (long/lat, lmbda/phi)
    
    parameters:
    lambda  -   array of longitude (azimuth)
    phi     -   array latitude (elevation from equator)
    lambda0 -   central longitude - optional if phi1 not provided - default = 0.0

    returns:
    (x, y)     -   x, y tuple of arrays of coordinates in projection space,
                    array size matches input lmbda and phi"""


    theta = phi
    for i in range(10) :
        theta = theta - (2.0*theta + np.sin(2.0*theta) - math.pi *np.sin(phi)) / \
                        (2.0 + 2.0*np.cos(2.0*theta) + 1e-12)
    
    # catch the theta values that squeak past the poles
    theta[ phi >=  0.5 * math.pi ] =  0.5 * math.pi
    theta[ phi <= -0.5 * math.pi ] = -0.5 * math.pi   
    
    # adjust for centre longitude
    dlmbda = lmbda - lmbda0
    
    dlmbda[ dlmbda >  math.pi ] =  dlmbda[ dlmbda >  math.pi ] - 2.0 * math.pi
    dlmbda[ dlmbda < -math.pi ] =  dlmbda[ dlmbda < -math.pi ] + 2.0 * math.pi

    x = 2.0 * dlmbda * np.cos(theta) / math.pi
    y = np.sin(theta)
    
    return x,y
def latLongGridMollweide( nLatStep, nLongStep, nSteps = 100 ) :
    """
    parameters:
        nLatStep    -   number of latitude steps from equator to pole
        nLongStep   -   number of longitude steps around sphere
        nSteps      -   integer number of steps to take around a full circle (resolution)
                           optional (default = 100)
    outputs: 
        grid   -   list with arrays of angles for latitude and longitude circles
                            units radians
                   arrays have longitude (azimuth) in first column, latitude (elevation)
                            in second column

    """
    
    full = np.reshape( np.linspace( -np.pi, np.pi, nSteps ), (nSteps, 1) )
    half = np.reshape( np.linspace( -0.5 * np.pi, 0.5 * np.pi, nSteps//2 ), (nSteps//2, 1) )

    grid = []

    for index in range( -nLatStep, nLatStep + 1 ) :
        lat = ( index / float(nLatStep) ) * 0.5 * np.pi * np.ones(full.shape)
        grid.append( np.hstack( (full, lat) ) )

    for index in range( -nLongStep//2, nLongStep//2 + 1 ) :
        lon = ( index / float(nLongStep) ) * 2.0 * np.pi * np.ones(half.shape)
        grid.append( np.hstack( (lon, half) ) )
    
    return grid

def main():
    bellData = pd.read_csv('touch-all-bells-single-1.csv')
    bellTypes = list( bellData.type.value_counts().index )
    bellTypes.sort()

    t0 = 0
    t1 = 146


    venues = {  'mic_121617_103906' : 'egh',
                'mic_121617_111202' : 'egh',
                'mic_121817_105432' : 'nmc',
                'mic_121817_115851' : 'nmc'   }

    recordingNames = [ rName for rName in venues ]
    recordingNames.sort()

    '''recording'''
    #recordingSet = [ recordingNames[ int(nStr.strip()) ] for nStr in argdict['recording'].strip().split(',') ]
    recordingSet = ['mic_121617_103906']
    recordingFrames = []
    for recordingName in recordingSet :
        recordingFrames.append( bellData[ bellData.recording == recordingName ] )
    bellData = pd.concat( recordingFrames )
    del recordingFrames
    markerColor = [ 'b', 'g', 'r', 'c', 'm', 'y', 'dimgray' ]
    markerStyle = [ 'o', 'v', 'P', '*', 'D', 'X', '2' ]

    t0, t1 = min(t0,t1), max(t0,t1)

    t0 = int( t0 * 100.0 )
    t1 = int( t1 * 100.0 )
    bellData = bellData[ t0 <= bellData.time ]
    bellData = bellData[ bellData.time <= t1 ]
    #  Mollweide Equal Area Projection
    lambda0 = 0.0
    markerColor = [ 'b', 'g', 'r', 'c', 'm', 'y', 'dimgray' ]
    markerStyle = [ 'o', 'v', 'P', '*', 'D', 'X', '2' ]

    fig = plt.figure( figsize = (11.0, 8.5) )
    ax = fig.add_subplot( 111 )
    ax.axis( 'equal' )
    ax.set_xlim( [-2, 2] )
    ax.set_ylim( [-1, 1] )

    grid = latLongGridMollweide( 8, 16 )
    for gridLine in grid :
        xGrid, yGrid = mollweide( gridLine[:,0], gridLine[:,1], lambda0 )
        ax.plot( xGrid, yGrid, color = [0.8, 0.8, 0.8] )

    # bellTypes = list( bellData.type.value_counts().index )
    # bellTypes.sort()

    for bellIndex, bellType in enumerate(bellTypes) :
        x0 = bellData.x0[ bellData.type == bellType ]
        y0 = bellData.y0[ bellData.type == bellType ]
        z0 = bellData.z0[ bellData.type == bellType ]
        
        lmbda = np.arctan2( y0, x0 )                        # longitude/azimuth
        phi = np.arctan2( z0, np.sqrt( x0**2 + y0**2) );    # latitude/elevation

        x, y = mollweide( lmbda, phi, lambda0 )
        plt.scatter( x, y, s= 100, marker=markerStyle[bellIndex], \
                    edgecolors='0.0', color=markerColor[bellIndex], label=bellType, alpha=0.5 )
        
        
    plt.legend( )
    plt.title('mollweide')
    plt.axis( 'off' )
    plt.show()

if __name__ == '__main__':
    main()