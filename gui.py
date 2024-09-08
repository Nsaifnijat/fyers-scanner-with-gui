
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from IndianMarkets.TheFinalversionOfCode.finalCode.final.main import *
import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QThread,QObject
from PyQt5.QtWidgets import QListWidgetItem, QDialog, QApplication, QWidget,QMainWindow
import pandas as pd
from PyQt5.QtGui import QIcon


class start_signal(QObject):
  
    def __init__(self,symbols,ui,candl1,candl2,candl3,dayha):
        super().__init__()
        self.symbols = symbols
        self.ui = ui
        self.candl1 = candl1
        self.candl2 = candl2
        self.candl3 = candl3
        self.dayha = dayha
    def start_event(self):
        QApplication.sendPostedEvents()
        run_once(self.symbols,self.ui,self.candl1,self.candl2,self.candl3,self.dayha)
        QApplication.processEvents()
    def contin_start(self):
        QApplication.sendPostedEvents()
        run_multiple(self.symbols,self.ui,self.candl1,self.candl2,self.candl3,self.dayha)
        QApplication.processEvents()

class home_page(QMainWindow):
    def __init__(self):
        super(home_page,self).__init__()
        self.ui=loadUi('req/appp.ui',self)
        self.signals.sortItems(Qt.DescendingOrder)
        self.startbtn.clicked.connect(self.startter)
        self.restartbtn.clicked.connect(self.loop_starter)
    def refresher(self):
        self.candl1 = self.candle1.text()
        if not(self.candl1):
            self.candl1 ='None'
        self.candl2 = self.candle2.text()
        if not(self.candl2):
            self.candl2 ='None'
        self.candl3 = self.candle3.text()
        if not(self.candl3):
            self.candl3 ='None'
        self.dayha = self.dayha.text()
        if not(self.dayha):
            self.dayha = 5
        #print('candlha',self.candl1,self.candl2,self.candl3,type(self.dayha))
        self.symbol = pd.read_excel('symbols\symbols.xlsx')
        self.symbols = list(self.symbol['symbols'])
        #self.symbols = [ 'ABFRL', 'ALKEM', 'AMARAJABAT', 'APOLLOHOSP', 'APOLLOTYRE']
    def loop_starter(self):
        self.refresher()
        self.start_signal  = start_signal(self.symbols,self.ui,self.candl1,self.candl2,self.candl3,self.dayha)
        self.Thread_object = QThread(parent=self)
        self.start_signal.moveToThread(self.Thread_object)
        self.Thread_object.started.connect(self.start_signal.contin_start)
        self.Thread_object.start()
    
    def startter(self):
        self.refresher()
        #self.candl1= timeframes[self.candl1]
        #print(self.candl1)
        #print(self.candl2,self.candl3)
        #starting(self.symbols,self.ui,self.candl1,self.candl2,self.candl3)
        self.start_threads()
    def start_threads(self):
        self.start_signal  = start_signal(self.symbols,self.ui,self.candl1,self.candl2,self.candl3,self.dayha)
        self.Thread_object = QThread(parent=self)
        self.start_signal.moveToThread(self.Thread_object)
        #self.Thread_object.stop_signal.connect(self.stopper)
        self.Thread_object.started.connect(self.start_signal.start_event)
        self.Thread_object.start()
app=QApplication(sys.argv)
app.setWindowIcon(QIcon('req\iconn.png'))        
welcome=home_page()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setWindowTitle('PSAR Signals')
widget.setMinimumHeight(620)
widget.setMinimumWidth(1000)
widget.show()

try:
    sys.exit(app.exec())
except:
    print('there is a problem')

