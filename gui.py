'''importing python libs'''
import sys
import pandas as pd
import numpy as np
import os
import time
import json
'''-----------------------'''

'''importing custom classes'''
from lambert_implement import laeap, latLongGridLambert
from mollweide_implement import mollweide, latLongGridMollweide
from _plot_classes import MollweideScatter, LambertScatter, LassoManager, MplCanvasScatter, TimeLinePlot
from _table_classes import TableModel
'''-----------------------'''

'''importing matplotlib things'''
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
'''-----------------------'''

'''importing PyQt5 things'''
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
'''-----------------------'''


'''Main Window Class'''
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #initializing basic GUI properties
        self.df = pd.DataFrame().fillna(0)
        self.filepath = ''
        self.setWindowTitle("My GUi")
        self.resize(4000, 1000)
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.createMenuBar()
        
        
        #setting and adding layouts
        self.table_layout = QVBoxLayout()
        self.input_layout = QHBoxLayout() 
        self.mainLayout.addLayout(self.table_layout)
        self.plot_layout = QVBoxLayout()
        self.mainLayout.addLayout(self.plot_layout)
    
    def getAudioFile(self):
        try:
            self.filepath = QFileDialog.getOpenFileName()
            self.audacityPort()
        except Exception as e:
            print(e)
    '''function to import data for scatter plot'''
    def getCSVScatter(self):
        try:
           self.filepath = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
           self.readDataScatter()
        except Exception as e:
            print(e)
            pass
    
    '''function to read scatter plot data'''
    def readDataScatter(self):
        #self.df is where the data is contained.
        self.df = pd.read_csv(self.filepath, encoding='utf-8').fillna(0)
        self.scatterTable() 
        self.plot_scatter()  
    
    '''function to import data for lambertian plot'''
    def getCSVLambert(self):
        try:
           self.filepath = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
           self.readDataLambert()
        except Exception as e:
            print(e)
            pass
    '''function to read lambertian plot data'''
    def readDataLambert(self):
        #self.df is where the data is contained.
        self.df = pd.read_csv(self.filepath, encoding='utf-8').fillna(0)
        
        self.t0, ok = QInputDialog.getInt(self,"time selection","enter initial time")
        self.t1, ok = QInputDialog.getInt(self,"time selection","enter final time")
        
       
        self.table_lamb() 
        self.lambert()
    
    '''function to import data for mollweide plot'''
    def getCSVMollweide(self):
        try:
           self.filepath = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
           self.readDataMollweide()
        except Exception as e:
            print(e)
            pass
    '''function to read mollweide plot data'''
    def readDataMollweide(self):
        #self.df is where the data is contained.
        self.df = pd.read_csv(self.filepath, encoding='utf-8').fillna(0)
        self.t0, ok = QInputDialog.getInt(self,"time selection","enter initial time")
        self.t1, ok = QInputDialog.getInt(self,"time selection","enter final time")
        self.table_lamb() 
        self.mollweide_func()

    '''function to import data for timeline'''
    def getCSVTimeline(self):
        try:
            self.filepath = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
            self.readDataTimeline()
        except Exception as e:
            print(e)
            pass
    def readDataTimeline(self):
        self.df = pd.read_csv(self.filepath, encoding='utf-8')
        #self.table_timeline()
        self.t0, ok = QInputDialog.getInt(self,"time selection","enter initial time")
        self.t1, ok = QInputDialog.getInt(self,"time selection","enter final time")
        self.timeline_table()
        self.timeline_func()
    '''function to create the menu bar'''
    def createMenuBar(self):
        menuBar = QMenuBar()
        #file Menu
        fileMenu = menuBar.addMenu('&File')
        #import action
        import_action = QAction("Import", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self.getCSVScatter)
        fileMenu.addAction(import_action)
        #exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(lambda :QApplication.quit())
        fileMenu.addAction(exit_action)
        #plot Menu
        plotMenu = menuBar.addMenu('&Plot')
        scatterAction = QAction("Scatter Plot", self)
        scatterAction.triggered.connect(self.getCSVScatter)
        #lambertian action
        lambertAction = QAction("Lambert", self)
        lambertAction.triggered.connect(self.getCSVLambert)
        #mollweide action
        mollweideAction = QAction("Mollweide", self)
        mollweideAction.triggered.connect(self.getCSVMollweide)
        #adding the actions to the plot menu tab
        #timeline action
        timeLineAction = QAction("TimeLine", self)
        timeLineAction.triggered.connect(self.getCSVTimeline)
        plotMenu.addAction(lambertAction)
        plotMenu.addAction(scatterAction)
        plotMenu.addAction(mollweideAction)
        plotMenu.addAction(timeLineAction)
        #audio menu
        audioMenu = menuBar.addMenu("Audio")
        audacityAction = QAction("Audacity", self)
        audacityAction.triggered.connect(self.getAudioFile)
        audioMenu.addAction(audacityAction)
        #help menu
        helpMenu = menuBar.addMenu("Help")
        readMeAction = QAction("ReadMe", self)
        helpMenu.addAction(readMeAction)
        self.mainLayout.setMenuBar(menuBar)

    '''function to create the table for the scatter plot'''
    def scatterTable(self):
        #removes previous table
        self.input_layout.setParent(None)
        for i in reversed(range(self.table_layout.count())):
            self.table_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.input_layout.count())):
            self.input_layout.itemAt(i).widget().deleteLater()
        #creating table
        table = TableModel(self.df)
        self.x_selection = QComboBox()
        self.y_selection = QComboBox()
        self.plot_button = QPushButton("Refresh", self)

        self.input_layout.addWidget(self.x_selection)
        self.input_layout.addWidget(self.y_selection)
        self.input_layout.addWidget(self.plot_button)
        #adding the data
        for col in self.df.columns:
            self.x_selection.addItem(col)
            self.y_selection.addItem(col)
            
        
        #connecting to scatter plot function when button is pressed
        self.plot_button.clicked.connect(lambda:self.plot_scatter(x=self.x_selection.currentIndex(), y=self.y_selection.currentIndex()))
        #adding layouts
        self.table_layout.addLayout(self.input_layout)
        self.table_layout.addWidget(table)
    '''function to create the table for the lambertian plot'''
    def table_lamb(self, ind=[]):
        #remove previous table
        self.input_layout.setParent(None)
        for i in reversed(range(self.table_layout.count())):
            self.table_layout.itemAt(i).widget().setParent(None)
        #formatting data
        bellData = self.df
        bellTypes = list(bellData.type.value_counts().index)
        bellTypes.sort()
        #t0, t1 = 0, 146
        t0 = self.t0
        t1 = self.t1
        recordingSet = ['mic_121617_103906']
        recordingFrames = []
        for recordingName in recordingSet :
            recordingFrames.append( bellData[ bellData.recording == recordingName ] )
        bellData = pd.concat( recordingFrames )
        del recordingFrames

        t0, t1 = min(t0,t1), max(t0,t1)

        t0 = int( t0 * 100.0 )
        t1 = int( t1 * 100.0 )
        bellData = bellData[ t0 <= bellData.time ]
        bellData = bellData[ bellData.time <= t1 ]
        
        self.table = TableModel(bellData)
        self.highlight_row(ind)
        
        self.table_layout.addWidget(self.table)
    '''function to highlight row based on selection'''

    def timeline_table(self):
        self.input_layout.setParent(None)
        for i in reversed(range(self.table_layout.count())):
            self.table_layout.itemAt(i).widget().setParent(None)
        bellData = self.df
        bellTypes = list(bellData.type.value_counts().index)
        bellTypes.sort()
        t0 = self.t0
        t1 = self.t1
        t0,t1 = min(t0,t1), max(t0, t1)
        t0 = int(t0*100.0)
        t1 = int(t1 * 100.0)
        bellData = bellData[t0 <= bellData.time]
        bellData = bellData[bellData.time <= t1]
        self.table = TableModel(bellData)
        self.table_layout.addWidget(self.table)
    def highlight_row(self, index):
            cols = self.table.columnCount()
            for i in range(0, cols):
                for j in range(0, len(index)):
                    self.table.item(index[j], i).setBackground(QtGui.QColor('red'))    

    '''scatter plot function'''
    def plot_scatter(self, x=0, y=1):
        
        # for i in reversed(range(self.plot_layout.count())):
        #     self.plot_layout.itemAt(i).widget().setParent(None)
        xval = self.df.iloc[:,x] 
        yval = self.df.iloc[:,y] 
        
        sc = MplCanvasScatter(self, x=xval, y=yval)
        x_head = self.df.columns[x]
        y_head = self.df.columns[y]
        title = str(x_head) + ' vs ' + str(y_head)
        sc.ax.set_title(title)
        sc.ax.set_xlabel(x_head)
        sc.ax.set_ylabel(y_head)

        toolbar = NavigationToolbar(sc, self)
        
        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(sc)

  
    '''main function for creating lambertian plot'''  
    def lambert(self):
        #removing previous plot
        for i in reversed(range(self.plot_layout.count())):
            self.plot_layout.itemAt(i).widget().setParent(None)
        #formatting data
        bellData = self.df
        bellTypes = list(bellData.type.value_counts().index)
        bellTypes.sort()
        #t0, t1 = 0, 146
        t0 = self.t0
        t1 = self.t1
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
        grid = latLongGridLambert(8,16)  
        phi1, lambda0 = 0.0, 0.0   

        sc = LambertScatter(self, x=None, y=None, color=None, marker=None,
        label=None, alpha=None)
        #creating gridlines
        for gridLine in grid :
            xGrid, yGrid = laeap( gridLine[:,0], gridLine[:,1], lambda0, phi1 )
            sc.ax.plot( xGrid, yGrid, color = [0.8, 0.8, 0.8] )
        #plotting bells
        xvals, yvals = [],[]
        index_list = []
        for bellIndex, bellType in enumerate(bellTypes):
            x0 = bellData.x0[bellData.type == bellType]
            y0 = bellData.y0[bellData.type == bellType]
            z0 = bellData.z0[bellData.type == bellType]
            lmbda = np.arctan2(y0, x0)
            phi = np.arctan2(z0, np.sqrt(x0**2 + y0**2))
            x,y = laeap(lmbda, phi, lambda0, phi1)
            xvals.append(x.values)
            yvals.append(y.values)
            index_list.append(x.index)
            sc.ax.scatter(x, y, s=100, marker=markerStyle[bellIndex],
            color=markerColor[bellIndex], label=bellType, alpha=0.5)
        #some python list comprehension to format data for other classes
        x_flat, y_flat = [],[]
        index_flat = []
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
            data_dic_x[x_flat[i]] = index_flat[i]
        data = np.column_stack((x_flat, y_flat))
        self.selector = LassoManager(sc.ax, data)
        #function to accept selection
        def accept(event):
            if event.key == "f":
                vals = self.selector.xys[self.selector.ind]
                val_list = vals.tolist()
                key_list = []
                for i in range(len(val_list)):
                    xval = val_list[i][0]
                    key = data_dic_x[xval]
                    print('key', key)
                    key_list.append(key)

                sc.fig.canvas.draw()
                self.table_lamb(ind=key_list)
        
        sc.ax.legend()
        #creating toolbar and setting layouts
        toolbar = NavigationToolbar(sc, self)
        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(sc)
        #set the focus policy onto the plot
        sc.fig.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        sc.fig.canvas.setFocus()
        sc.fig.canvas.mpl_connect("key_press_event", accept)
        
    '''main function for the mollweide plot'''
    def mollweide_func(self):
        #removing previous plot
        for i in reversed(range(self.plot_layout.count())):
            self.plot_layout.itemAt(i).widget().setParent(None)
        #formatting data
        bellData = self.df
        bellTypes = list(bellData.type.value_counts().index)
        bellTypes.sort()
        #t0, t1 = 0, 146
        t0 = self.t0
        t1 = self.t1
        recordingSet = ['mic_121617_103906']
        recordingFrames = []
        for recordingName in recordingSet:
            recordingFrames.append(bellData[bellData.recording == recordingName])
        bellData = pd.concat(recordingFrames)
        del recordingFrames
        markerColor = [ 'b', 'g', 'r', 'c', 'm', 'y', 'dimgray' ]
        markerStyle = [ 'o', 'v', 'P', '*', 'D', 'X', '2' ]
        t0, t1 = min(t0, t1), max(t0, t1)
        t0 = int(t0*100)
        t1 = int(t1*100)
        bellData = bellData[t0 <= bellData.time]
        bellData = bellData[bellData.time <= t1]
        lambda0 = 0.0
        #creating gridlines and plot object
        grid = latLongGridMollweide(8, 16)
        sc = MollweideScatter(self, x=None, y=None, marker=None,
        edgecolors=None, label=None, alpha=None)
        #creating gridlines
        for gridLine in grid:
            XGrid, YGrid = mollweide(gridLine[:,0], gridLine[:,1], lambda0)
            sc.ax.plot(XGrid, YGrid, color=[0.8, 0.8, 0.8])
        #plotting bells
        xvals, yvals = [], []
        index_list = []
        for bellIndex, bellType in enumerate(bellTypes):
            x0 = bellData.x0[ bellData.type == bellType ]
            y0 = bellData.y0[ bellData.type == bellType ]
            z0 = bellData.z0[ bellData.type == bellType ]            
            lmbda = np.arctan2( y0, x0 )      
            phi = np.arctan2(z0, np.sqrt(x0**2 + y0**2))
            x,y = mollweide(lmbda, phi, lambda0)
            xvals.append(x)
            yvals.append(y)
            index_list.append(x.index)
            sc.ax.scatter(x, y, s=100, marker=markerStyle[bellIndex],
            edgecolors='0.0', color=markerColor[bellIndex], label=bellType, alpha=0.5)
        #python list comprehension to format data for other classes
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
            data_dic_x[x_flat[i]] = index_flat[i]
        data = np.column_stack((x_flat, y_flat))
        self.selector = LassoManager(sc.ax, data)
        #function for accepting selected points
        def accept(event):
            if event.key == 'f':
                vals = self.selector.xys[self.selector.ind]
                val_list = vals.tolist()
                key_list = []
                for i in range(len(val_list)):
                    xval = val_list[i][0]
                    key = data_dic_x[xval]
                    key_list.append(key)
                sc.fig.canvas.draw()
                self.table_lamb(ind=key_list)
        sc.ax.legend()
        #creating toolbar and setting layouts
        toolbar = NavigationToolbar(sc, self)
        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(sc)
        #set focus policy on the plot
        sc.fig.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        sc.fig.canvas.setFocus()
        sc.fig.canvas.mpl_connect("key_press_event", accept)
    
    def timeline_func(self):
        #remove previous plot
        for i in reversed(range(self.plot_layout.count())):
            self.plot_layout.itemAt(i).widget().setParent(None)
        bellData = self.df
        bellTypes = list(bellData.type.value_counts().index)
        bellTypes.sort()
        t0 = 10
        t1 = 40
        t0,t1 = min(t0,t1), max(t0, t1)
        t0 = int( t0 * 100.0 )
        t1 = int( t1 * 100.0 )
        bellData = bellData[ t0 <= bellData.time ]
        bellData = bellData[ bellData.time <= t1 ]
        markerColor = [ 'b', 'g', 'r', 'c', 'm', 'y', 'dimgray' ]
        markerStyle = [ 'o', 'v', 'P', '*', 'D', 'X', '2' ]

        sc = TimeLinePlot(self, x=None, y=None, marker=None,
        label=None, color=None, alpha=None)
        for bellIndex, bellType in enumerate(bellTypes):
            x = bellData.time[bellData.type == bellType] / 100.0
            y = bellData.pitch[bellData.type == bellType]
            sc.ax.scatter(x, y, s=100, marker=markerStyle[bellIndex], \
                color=markerColor[bellIndex], label=bellType, alpha=0.5)
        
        #sc.ax.axis([t0/100.0, t1/100.0, 45, 105])
        sc.ax.legend()
        
        #creating toolbar and setting layouts
        toolbar = NavigationToolbar(sc, self)
        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(sc)

    def audacityPort(self):
        print("Found audacity port")
        print(self.filepath[0])
        test = self.filepath[0].replace("/", '\\')
        split = test.split("\\")
        infile_wav = split[-1]
        split.pop(-1)
        pathtest = "\\".join([str(item) for item in split]) #final path
        infiletest = infile_wav[:len(infile_wav) - 4]
        path = pathtest
        infile = infiletest
        from audacity_methods import import_method
        import_method(PATH=path, INFILE=infile)
        

'''allowing for standalone execution'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

