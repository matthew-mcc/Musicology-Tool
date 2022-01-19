
'''I think the problem with way too many points is that it is not just plotting one recording lol'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.collections import RegularPolyCollection
from matplotlib import colors as mcolors, path
from matplotlib.widgets import Lasso

class LassoManager:
    def __init__(self, ax, data):
        self.axes = ax
        self.canvas = ax.figure.canvas
        self.data = data
        xys = []
        for i in range(len(self.data)):
            hold = self.data[i]
            tup = (hold[0], hold[1])
            xys.append(tup)
        self.xys = xys
        self.Npts = len(self.xys)
        
        self.collection = RegularPolyCollection(
            6, sizes=(100,),
            offsets=self.xys)
            
        self.xys = self.collection.get_offsets()
        self.fc = self.collection.get_facecolors()
        self.fc = np.tile(self.fc, (self.Npts, 1))
        ax.add_collection(self.collection)  
        self.ind = []
        self._highlights = ax.scatter([], [], s=200, color='red', zorder=10, alpha=0.25)
        self.cid = self.canvas.mpl_connect('button_press_event', self.on_press)
    
    def callback(self, verts):
        self.collection.set_facecolors(self.fc)
        p = path.Path(verts)
        self.ind = p.contains_points(self.xys)
        test = self.xys[self.ind]
        self._highlights.set_offsets(test)
        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)
        del self.lasso

    def on_press(self, event):
        if self.canvas.widgetlock.locked():
            return
        if event.inaxes is None:
            return
        self.lasso = Lasso(event.inaxes,
                           (event.xdata, event.ydata),
                           self.callback)
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)
   
    
    
        
def laeap( lmbda, phi, lmbda0 = 0.0, phi1 = 0.0 ):
    kPrime = np.sqrt( 2.0 / ( 1.0 + np.sin(phi1) * np.sin(phi) + \
                        np.cos(phi1) * np.cos(phi) * np.cos(lmbda - lmbda0)  + 1e-12 ) )

    x = kPrime * np.cos(phi) * np.sin(lmbda - lmbda0)
    y = kPrime * ( np.cos(phi1) * np.sin(phi) - \
                    np.sin(phi1) * np.cos(phi) * np.cos(lmbda - lmbda0) )
                    
    return x,y

def latLongGridLambert( nLatStep, nLongStep, nSteps = 100 ) :
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

    for index in range( nLongStep ) :
        lon = ( index / float(nLongStep) ) * 2.0 * np.pi * np.ones(half.shape)
        grid.append( np.hstack( (lon, half) ) )
    
    return grid


def main():
    bellData = pd.read_csv('dataFiles/touch-all-bells-single-1.csv')
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

    phi1 = 0.0
    lambda0 = 0.0
    fig = plt.figure(figsize=(11.0, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('square')
    ax.set_xlim( [-2, 2.25] )
    ax.set_ylim( [-2, 2.25] )

    grid = latLongGridLambert( 8, 16 )
    for gridLine in grid :
        xGrid, yGrid = laeap( gridLine[:,0], gridLine[:,1], lambda0, phi1 )
        ax.plot( xGrid, yGrid, color = [0.8, 0.8, 0.8] )
    #create the latlon grid
    
   
    

    xvals, yvals = [], []
    index_list = []
    for bellIndex, bellType in enumerate(bellTypes):
        
        x0 = bellData.x0[bellData.type == bellType]
        print(x0)
        y0 = bellData.y0[bellData.type == bellType]
        z0 = bellData.z0[bellData.type == bellType]
        lmbda = np.arctan2(y0, x0)
        phi = np.arctan2(z0, np.sqrt(x0**2 + y0**2))
        x,y = laeap(lmbda, phi, lambda0, phi1)
        xvals.append(x)
        yvals.append(y)
        index_list.append(x.index)
        plt.scatter( x, y, s= 100, marker=markerStyle[bellIndex], 
                        edgecolors='0.0', color=markerColor[bellIndex], label=bellType, alpha=0.5 )
        
    
    x_flat, y_flat = [], []
    index_flat = []
    data = []
    for sublist in xvals:
        for item in sublist:
            x_flat.append(item)
    for sublist in yvals:
        for item in sublist:
            y_flat.append(item)
    for sublist in index_list:
        for item in sublist:
            index_flat.append(item)
    
    data_dic_x = {}
    for i in range(len(index_flat)):
        #data_dic[index_flat[i]] = (x_flat[i], y_flat[i])
        data_dic_x[x_flat[i]] = index_flat[i]
    
    
    data = np.column_stack((x_flat, y_flat))
    
    #print(test_tup)
    selector = LassoManager(ax, data)
    def accept(event):
        if event.key == "enter":
            vals = selector.xys[selector.ind]
            print("Selected points:")
            
            val_list = vals.tolist()
            key_list = []
            for i in range(len(val_list)):
                #print(val_list[i][0])
                xval = val_list[i][0]
                key = data_dic_x[xval]
                print('key', key)
                key_list.append(key)
            print(key_list)
            fig.canvas.draw()

    fig.canvas.mpl_connect("key_press_event", accept)
 
    
    plt.legend()
  
    plt.show()
    


if __name__ == '__main__':
    main()
