from PyQt5.QtWidgets import *
from PyQt5 import QtGui
class TableModel(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df

        # set table dimension
        nRows, nColumns = self.df.shape
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)
        self.setHorizontalHeaderLabels(df)
        
        self.cellClicked.connect(self.onClick)
        
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
              self.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))
    
    def onClick(self, row, col):
        vals = row, col
        self.item(row, col).setBackground(QtGui.QColor('red'))
        print(vals)
        
