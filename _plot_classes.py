from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import mplcursors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import RegularPolyCollection
from matplotlib import colors as mcolors, path
from matplotlib.widgets import Lasso
class MplCanvasScatter(FigureCanvasQTAgg):
    def __init__(self, parent, x, y):
        fig, self.ax = plt.subplots(figsize=(5,4), dpi=120)
        
        super().__init__(fig)
        self.setParent(parent)

        """matplotlib script"""
        
        mplcursors.cursor(self.ax.scatter(x,y))

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
        
class LambertScatter(FigureCanvasQTAgg):
    fig = plt.figure(figsize=(11.0, 8.5))
    def __init__(self, parent, x, y, marker, color, label, alpha):
        
        
        
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('square')
        self.ax.set_xlim([-2, 2.25])
        self.ax.set_ylim([-2, 2.25])
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.ax.scatter(x, y, color=color, marker=marker, label=label, alpha=alpha)

class MollweideScatter(FigureCanvasQTAgg):
    fig = plt.figure(figsize=(11.0, 8.5))
    def __init__(self, parent, x, y, marker, edgecolors, label, alpha):
        
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('equal')
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-1, 1])
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax.scatter(x, y, edgecolors=edgecolors, marker=marker, label=label, alpha=alpha)

class TimeLinePlot(FigureCanvasQTAgg):
    fig = plt.figure(figsize=(11.0, 8.5))
    def __init__(self, parent, x, y, marker, color, label, alpha ):
        self.ax = self.fig.add_subplot(111)
        #self.ax.axis( [ t0/100.0, t1/100.0, 45, 105 ] )
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax.scatter(x, y, marker=marker, color=color, label=label, alpha=alpha)