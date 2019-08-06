from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.Qt import *
import PIL
from PIL import  Image
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtCore import QFileInfo
import numpy as np
from matplotlib import pyplot as plt
from tkinter import*
import math
import copy
import random
import qimage2ndarray
#===========================================functions==============================================
def distance(a_point,a_center):
    return ((a_center.position[0]-a_point.position[0])**2+(a_center.position[1]-a_point.position[1])**2+(a_center.position[2]-a_point.position[2])**2)**0.5
def rand_position():
    return [random.randint(1,255),random.randint(1,255),random.randint(1,255)]
def color(value):
    digit = list(map(str, range(10))) + list("ABCDEF")
    if isinstance(value, tuple):
        string = '#'
        for i in value:
            a1 = i // 16
            a2 = i % 16
            string += digit[a1] + digit[a2]
        return string
    elif isinstance(value, str):
        a1 = digit.index(value[1]) * 16 + digit.index(value[2])
        a2 = digit.index(value[3]) * 16 + digit.index(value[4])
        a3 = digit.index(value[5]) * 16 + digit.index(value[6])
        return (a1, a2, a3)
def hsv2rgb(hsv):
    h = float(hsv[0])
    s = float(hsv[1])
    v = float(hsv[2])
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return (r,g,b)
def rgb2hsv(rgb):
    r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return [h,s,v]
#=========================================== classes  =============================================
class Center(object):
    def __init__(self,centerposition=[0,0,0]):
        self.position=centerposition
        self.buddies=[]

class Point(object):
    def __init__(self,pointposition=[0,0,0]):
        self.position=pointposition
        self.boss=None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(966, 559)
        self.filename=None
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 300, 400))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(224, 224, 224))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(97, 97, 97))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 129, 129))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(224, 224, 224))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(224, 224, 224))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(97, 97, 97))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 129, 129))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(224, 224, 224))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(97, 97, 97))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(224, 224, 224))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(97, 97, 97))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 129, 129))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(97, 97, 97))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(97, 97, 97))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.label.setPalette(palette)
        self.label.setAutoFillBackground(True)
        self.label.setText("")
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(370, 70, 541, 41))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(370, 170, 541, 41))
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName("progressBar_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(370, 30, 111, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(370, 140, 131, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(370, 250, 111, 16))
        self.label_4.setObjectName("label_4")


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 440, 131, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 966, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.choose_file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "反色得分"))
        self.label_3.setText(_translate("MainWindow", "副色占比得分"))
        self.label_4.setText(_translate("MainWindow", "主题色"))
        self.pushButton.setText(_translate("MainWindow", "Select Pic"))

    def choose_file(self):
        self.filename= QFileDialog.getOpenFileName(None, "Select Pic", '/', "All Files (*)")[0]
        #print(self.filename)
        img = PIL.Image.open(self.filename)
        #print('loaded')
        img_to_show=copy.deepcopy(img)
        img_to_show=img_to_show.resize((300, 400), PIL.Image.ANTIALIAS)
        data_matrix = np.array(img_to_show)
        img_to_show = qimage2ndarray.array2qimage(data_matrix)
        img_to_show = QPixmap(img_to_show)
        self.label.setPixmap(img_to_show)

        img = img.resize((200, 200), PIL.Image.ANTIALIAS)
        img_array = np.array(img)
        arr1 = img_array[:]
        #print(arr1.shape)
        points = []
        for x in range(1, arr1.shape[0]):
            for y in range(1, arr1.shape[1]):
                a = img_array[x, y][0]
                b = img_array[x, y][1]
                c = img_array[x, y][2]
                points.append(Point([a, b, c]))
        centers = []
        #for i in range(0, 6):
            #centers.append(Center(rand_position()))
        centers.append(Center([0, 0, 0]))
        centers.append(Center([0, 0, 255]))
        centers.append(Center([0, 255, 0]))
        centers.append(Center([255, 0, 0]))
        centers.append(Center([255, 255, 0]))
        centers.append(Center([0, 255, 255]))
        centers.append(Center([255, 0, 255]))
        centers.append(Center([255, 255, 255]))


        for i in range(0, 8):

            for apoint in points:
                mindist = 99999
                for acenter in centers:
                    present_dist = distance(apoint, acenter)
                    if present_dist <= mindist:
                        mindist = present_dist
                        apoint.boss = acenter

            for acenter in centers:
                acenter.buddies = []
                for apoint in points:
                    if apoint.boss == acenter:
                        acenter.buddies.append(apoint)

            for acenter in centers:
                new_x_total, new_y_total, new_z_total = 0, 0, 0
                for apoint in acenter.buddies:
                    new_x_total += apoint.position[0]
                    new_y_total += apoint.position[1]
                    new_z_total += apoint.position[2]
                total_number = len(acenter.buddies)
                if total_number == 0:
                    continue
                else:
                    acenter.position = [new_x_total / total_number, new_y_total / total_number,
                                        new_z_total / total_number]

        print('-2')
        copyofcenters = []
        for i in centers:
            copyofcenters.append(i)  # copy of centers, just don't wanna use copy.deepcopy

        minbuddynum = 999999
        for acenter in copyofcenters:
            if len(acenter.buddies) == 0:
                continue
            else:
                if len(acenter.buddies) <= minbuddynum:
                    minbuddynum = len(acenter.buddies)

        total_major_color = [[0, 0, 0], 0]
        for acenter in copyofcenters:
            if len(acenter.buddies) == 0:
                continue
            elif len(acenter.buddies) == minbuddynum:
                minorcolor = acenter.position
                minorcolornum = len(acenter.buddies)
            else:
                total_major_color[0][0] += len(acenter.buddies) * acenter.position[0]
                total_major_color[0][1] += len(acenter.buddies) * acenter.position[1]
                total_major_color[0][2] += len(acenter.buddies) * acenter.position[2]
                total_major_color[1] += len(acenter.buddies)
        majorcolor = [total_major_color[0][0] / total_major_color[1], total_major_color[0][1] / total_major_color[1],
                      total_major_color[0][2] / total_major_color[1]]

        minorcolor = rgb2hsv(minorcolor)
        majorcolor = rgb2hsv(majorcolor)
        # print(minorcolor,majorcolor)
        minorcolornum = minorcolornum
        majorcolornum = total_major_color[1]

        degree_of_180 = (180 - abs(abs(minorcolor[0] - majorcolor[0]) - 180)) / 180 * 100
        degree_of_85percent = (1 - abs(minorcolornum / majorcolornum - 0.15)) * 100
        print('-1')
        self.progressBar.setValue(degree_of_180)
        self.progressBar_2.setValue(degree_of_85percent)
        print(0)
        #show all theme colors
        total_pixels_num=200*200  #self.progressBar_2.setGeometry(QtCore.QRect(370, 270, 541, 41))
        x_start=370
        for acenter in copyofcenters:
            color=acenter.position
            buddyamount=len(acenter.buddies)
            barlenth=int(buddyamount/total_pixels_num*515)

            color_label = QLabel(self.centralwidget)   #!!!!!!!!!!!!!! wow !!!!!!!!!!!!!!1
            color_label.setText("")
            color_label.setAutoFillBackground(True)
            palette = QPalette()
            palette.setColor(color_label.backgroundRole(), QColor(color[0], color[1], color[2]))
            color_label.setPalette(palette)
            color_label.setGeometry(x_start, 270, barlenth, 41)
            color_label.show()
            x_start+=barlenth



app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
