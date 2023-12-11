import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

app = QApplication([])
mainW = QWidget()

mainLay = QVBoxLayout()
mainW.setLayout(mainLay)
#company/phase1/level1
buffer = None
path = 0

Xsize = 0
Ysize = 0

def QtMapEditor():
    
    mainW.resize(100, 100)
    
    lay = QVBoxLayout()
    button1 = QPushButton("Нова карта")
    button2 = QPushButton("Редактувати карту")
    button3 = QPushButton("Відміна")
    button4 = QPushButton("default")
    ELine = QLineEdit()

    Box = QGroupBox()


    Box.setLayout(lay)
    lay.addWidget(button1)
    lay.addWidget(button2)
    lay.addWidget(ELine)
    lay.addWidget(button3)
    lay.addWidget(button4)

    mainLay.addWidget(Box)

    def OpenMap(p = False):
        global buffer
        global path

        buffer = None

        if p == False:
            path = ELine.text()
        else:
            path = p
        
        try:

            with open("bin/maps/" + path + ".json", "r") as map:
                map_data = json.load(map)

                buffer = map_data

                map.close()

        except FileNotFoundError:
            pass

        Close()
    
    def CreateMap(def_ = False):
        global path

        if not def_:
            path = ELine.text()

        try:

            with open("bin/maps/" + path + ".json", "x") as m:
                json.dump({}, m)
                m.close()

        except FileExistsError:
            pass

        OpenMap(path)
    
    def Close():
        Box.hide()
        mainW.hide()
        app.quit()
    
    def Default():
        global path

        path = "company/phase1/" + ELine.text()
        CreateMap(1)
    
    button1.clicked.connect(CreateMap)
    button2.clicked.connect(OpenMap)
    button3.clicked.connect(Close)
    button4.clicked.connect(Default)

    Box.show()
    mainW.show()
    app.exec()
    Box.hide()

    return path, buffer

def QtSizeWin():
    
    mainW.resize(100, 100)

    mainLayout = QVBoxLayout()
    Box = QGroupBox()

    ELine1 = QLineEdit("Xsize")
    ELine2 = QLineEdit("Ysize")

    OKbutton = QPushButton("OK")

    mainW.setLayout(mainLayout)

    mainLayout.addWidget(ELine1)
    mainLayout.addWidget(ELine2)
    mainLayout.addWidget(OKbutton)

    Box.setLayout(mainLayout)
    mainLay.addWidget(Box)

    def Check():
        global Xsize
        global Ysize

        Xsize = ELine1.text()
        Ysize = ELine2.text()

        try:
            Xsize = int(Xsize)
            Ysize = int(Ysize)

            Box.hide()
            mainW.hide()
            app.quit()
    
        except BaseException:
            ELine1.setText("error")
            ELine2.setText("error")
                
    OKbutton.clicked.connect(Check)

    Box.show()
    mainW.show()
    app.exec()
    Box.hide()
    
    return Xsize, Ysize

flow = 0

def QtSetTrigerFlow():
    mainW.resize(100, 100)

    mainLayout = QVBoxLayout()
    Box = QGroupBox()

    ELine1 = QLineEdit("TrigerFlow")

    OKbutton = QPushButton("OK")

    mainW.setLayout(mainLayout)

    mainLayout.addWidget(ELine1)
    mainLayout.addWidget(OKbutton)

    Box.setLayout(mainLayout)
    mainLay.addWidget(Box)

    def Check():
        global flow

        flow = ELine1.text()

        try:
            flow = int(flow)

            Box.hide()
            mainW.hide()
            app.quit()

        except BaseException:
            ELine1.setText("error")
            
    OKbutton.clicked.connect(Check)

    Box.show()
    mainW.show()
    app.exec()
    Box.hide()
    
    return ["TrigB", "door", flow]

TelFlow = 0
LocationCor = 0

def QtSetTeleport_A_PointSettings():
        
    mainW.resize(100, 100)

    mainLayout = QVBoxLayout()
    Box = QGroupBox()

    ELine1 = QLineEdit("FinalLocarion")
    ELine2 = QLineEdit("TeleportFlow")

    OKbutton = QPushButton("OK")

    mainW.setLayout(mainLayout)

    mainLayout.addWidget(ELine1)
    mainLayout.addWidget(ELine2)
    mainLayout.addWidget(OKbutton)

    Box.setLayout(mainLayout)
    mainLay.addWidget(Box)

    def Check():
        
        global TelFlow, LocationCor

        LocationCor = ELine1.text()
        TelFlow = ELine2.text()

        try:
            LocationCor = int(LocationCor)
            TelFlow = int(TelFlow)

            Box.hide()
            mainW.hide()
            app.quit()
    
        except BaseException:
            ELine1.setText("error")
            ELine2.setText("error")
                
    OKbutton.clicked.connect(Check)

    Box.show()
    mainW.show()
    app.exec()
    Box.hide()
    
    return ["GTa", LocationCor, TelFlow]

def QtSetTeleport_B_PointSettings():
        
    mainW.resize(100, 100)

    mainLayout = QVBoxLayout()
    Box = QGroupBox()

    ELine2 = QLineEdit("TeleportFlow")

    OKbutton = QPushButton("OK")

    mainW.setLayout(mainLayout)

    mainLayout.addWidget(ELine2)
    mainLayout.addWidget(OKbutton)

    Box.setLayout(mainLayout)
    mainLay.addWidget(Box)

    def Check():
        
        global TelFlow

        TelFlow = ELine2.text()

        try:
            TelFlow = int(TelFlow)

            Box.hide()
            mainW.hide()
            app.quit()
    
        except BaseException:
            ELine2.setText("error")
                
    OKbutton.clicked.connect(Check)

    Box.show()
    mainW.show()
    app.exec()
    Box.hide()
    
    return ["GTb", 0, TelFlow]

def QtSetDoorSettings():
        
    mainW.resize(100, 100)

    mainLayout = QVBoxLayout()
    Box = QGroupBox()

    ELine2 = QLineEdit("TeleportFlow")
    button1 = QCheckBox("Enable")
    button2 = QCheckBox("Horizontal door")

    OKbutton = QPushButton("OK")

    mainW.setLayout(mainLayout)
    
    mainLayout.addWidget(ELine2)
    mainLayout.addWidget(button1)
    mainLayout.addWidget(button2)
    mainLayout.addWidget(OKbutton)

    Box.setLayout(mainLayout)
    mainLay.addWidget(Box)

    def Check():
        
        global TelFlow, LocationCor

        TelFlow = ELine2.text()

        try:
            TelFlow = int(TelFlow)

            Box.hide()
            mainW.hide()
            app.quit()
    
        except BaseException:
            ELine2.setText("error")
                
    OKbutton.clicked.connect(Check)

    Box.show()
    mainW.show()
    app.exec()
    Box.hide()
    
    return ["door", TelFlow, not button1.isChecked(), button2.isChecked()]    


if __name__ == "__main__":
    QtSetDoorSettings()
    pass