# Orange3 Musicology Data Exploration Application

Full stack data exploration and visualization tool used to discovery new facts and ideas about contemporary compositions. The data collected was obtained through a 360 degrees omni directional mic and was placed in the center of a concert hall during a live performance. The current version of the application is mainly used as a specialized plotting tool using plots like lambertian and mollweide to plot advanced data in three dimensional space. 
The program was built into Orange3, an open sourced data mining tool built for Python. The program allows seamless connection through multiple other varieties of widgets available in Orange. Although the datasets are intended to be complex musicology files, this program works with all data types, as the exploration aspect is set up in such a way where the type of data is irrelevant, the meaningfulness behind it is how it is used.

This progam was developed as part of a research opportunity at the University of Calgary under the direct supervision of professor Jeffrey Boyd from the Computer Science Department. Development started during the summer of 2021 and is planned to be continued at some point soon.

# Software / libraries used:
- Orange3 data mining software
- Python 3.9
- Matplotlib - _Python_
- Numpy - _Python_
- Pandas - _Python_
- PyQT5 - _Python_
- Audacity - _Open sourced Audio Library_ 


# ___USAGE___
To set up in Orange3:
1. Download and install Orange3 installation media --> http://orange.biolab.si/download/files/Orange3-3.2.dev0+e196459.win32-py3.4-install.exe
2. Follow wizard to install packages and dependencies.
3. Install Bioinformatics addon (optional).
4. Restart Orange3.
5. Navigate to the main file (gui.py)
6. Run "python -m Orange.canvas:.

Standalone Execution:
1. Navigate to the main file (gui.py)
2. Run "python gui.py".

Usage Basics:
1. Load data:
1.1 Drag a csv file widget from the Orange library, and then connect to plotting tool.
1.2 File -> import (from top left options bar)
2. Select the plotting selection you wish to use under plot.
3. Choose parameters and refresh plot as necessary.
4. Explore!


# Versions:
Currently in Beta version 1.0.

# Further implementation
Further implementation ideas include:
- More plotting features.
- Timeline visualization that goes across the plot with the composition playing in the background.
- Creating animations of the plots.
- More options along the top function bar.
- Host it on a website.
# Sources:
https://orangedatamining.com/
https://docs.python.org/3/
https://www.ucalgary.ca/future-students/undergraduate/explore-programs/computer-science
