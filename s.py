#!/usr/bin/env python

from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import copy
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as Tk
from tkinter.ttk import Frame


class serialPlot:
    def __init__(self, serialPort='/dev/ttyUSB0', serialBaud=38400, plotLength=100, dataNumBytes=2, numPlots=1):
        self.port = serialPort
        self.baud = serialBaud
        self.plotMaxLength = plotLength
        self.dataNumBytes = dataNumBytes
        self.numPlots = numPlots
        self.rawData = bytearray(numPlots * dataNumBytes)
        self.dataType = None
        if dataNumBytes == 2:
            self.dataType = 'h'  # 2 byte integer
        elif dataNumBytes == 4:
            self.dataType = 'f'  # 4 byte float
        self.data = []
        for i in range(numPlots):  # give an array for each type of data and store them in a list
            self.data.append(collections.deque([0] * plotLength, maxlen=plotLength))
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
        # self.csvData = []

        print('Intentando conectar en: ' + str(serialPort) + ' a ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(serialPort, serialBaud, timeout=4)
            print('Conectado en' + str(serialPort) + ' a ' + str(serialBaud) + ' BAUD.')
        except:
            print("Error al conectar con " + str(serialPort) + ' a ' + str(serialBaud) + ' BAUD.')

    def readSerialStart(self):
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)

    def getSerialData(self, frame, lines, lineValueText, lineLabel, timeText):
        currentTimer = time.perf_counter()
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)  # the first reading will be erroneous
        self.previousTimer = currentTimer
        timeText.set_text('t = ' + str(self.plotTimer) + 'ms')
        privateData = copy.deepcopy(
            self.rawData[:])  # so that the 3 values in our plots will be synchronized to the same sample time
        for i in range(self.numPlots):
            data = privateData[(i * self.dataNumBytes):(self.dataNumBytes + i * self.dataNumBytes)]
            value, = struct.unpack(self.dataType, data)
            self.data[i].append(value)  # we get the latest data point and append it to our array
            lines[i].set_data(range(self.plotMaxLength), self.data[i])
            lineValueText[i].set_text('[' + lineLabel[i] + '] = ' + str(value))
        # self.csvData.append([self.data[0][-1], self.data[1][-1], self.data[2][-1]])

    def backgroundThread(self):  # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
        self.serialConnection.reset_input_buffer()
        while (self.isRun):
            self.serialConnection.readinto(self.rawData)
            self.isReceiving = True
            # print(self.rawData)

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Desconectado...')
        # df = pd.DataFrame(self.csvData)
        # df.to_csv('data.csv')


class Window(Frame):
    def __init__(self, figure, master, SerialReference):
        Frame.__init__(self, master)
        self.entry = None
        self.setPoint = None
        self.master = master  # a reference to the master window
        self.serialReference = SerialReference  # keep a reference to our serial connection so that we can use it for bi-directional communicate from this class
        self.initWindow(figure)  # initialize the window with our settings

    def initWindow(self, figure):
        self.master.title("Ventilador Oxygen")
        canvas = FigureCanvasTkAgg(figure, master=self.master)
        toolbar = NavigationToolbar2Tk(canvas, self.master)
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        # create out widgets in the master frame
        lbl1 = Tk.Label(self.master, text="Flujo")
        #lbl1.pack(padx=1, pady=1)
        lbl1.place(x=10, y=10)
        self.entry1 = Tk.Entry(self.master, width=5)
        self.entry1.insert(0, '60')  # (index, string)
        self.entry1.place(x=100, y=10)
        DownButton = Tk.Button(self.master, text='«', width=2, command=self.down_flow)
        DownButton.place(x=50, y=8)
        UpButton = Tk.Button(self.master, text='»', width=2, command=self.up_flow)
        UpButton.place(x=150, y=8)

        # create out widgets in the master frame
        lbl2 = Tk.Label(self.master, text="Presion")
        # lbl1.pack(padx=1, pady=1)
        lbl2.place(x=210, y=10)
        self.entry2 = Tk.Entry(self.master, width=5)
        self.entry2.insert(0, '60')  # (index, string)
        self.entry2.place(x=320, y=10)
        DownButtonP = Tk.Button(self.master, text='«', width=2, command=self.down_flow_p)
        DownButtonP.place(x=270, y=8)
        UpButtonP = Tk.Button(self.master, text='»', width=2, command=self.up_flow_p)
        UpButtonP.place(x=370, y=8)


    def up_flow(self):
        new_val = int(self.entry1.get()) + 1
        print(new_val)
        self.entry1.delete(0, 3)
        self.entry1.insert(0, str(new_val))
        return

    def down_flow(self):
        new_val = int(self.entry1.get()) - 1
        print(new_val)
        self.entry1.delete(0, 3)
        self.entry1.insert(0, str(new_val))
        return
    def up_flow_p(self):
        new_val = int(self.entry2.get()) + 1
        print(new_val)
        self.entry2.delete(0, 3)
        self.entry2.insert(0, str(new_val))
        return

    def down_flow_p(self):
        new_val = int(self.entry2.get()) - 1
        print(new_val)
        self.entry2.delete(0, 3)
        self.entry2.insert(0, str(new_val))
        return

    def sendFactorToMCU(self):
        self.serialReference.sendSerialData(self.entry1.get() + '%')  # '%' is our ending marker


def main():
    # portName = 'COM5'
    portName = '/dev/ttyUSB0'
    baudRate = 115200
    maxPlotLength = 120  # number of points in x-axis of real time plot
    dataNumBytes = 4  # number of bytes of 1 data point
    numPlots = 2  # number of plots in 1 graph
    s = serialPlot(portName, baudRate, maxPlotLength, dataNumBytes, numPlots)  # initializes all required variables
    s.readSerialStart()  # starts background thread

    # plotting starts below
    # plotting starts below
    pltInterval = 20  # Period at which the plot animation updates [ms]
    xmin = 0
    xmax = maxPlotLength
    ymin = -30
    ymax = 120
    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes(xlim=(xmin, xmax), ylim=(float(ymin - (ymax - ymin) / 10), float(ymax + (ymax - ymin) / 10)))
    #ax.set_title('Arduino Accelerometer')
    #ax.set_xlabel("Time")
    #ax.set_ylabel("Accelerometer Output")

    # put our plot onto Tkinter's GUI
    root = Tk.Tk()
    app = Window(fig, root, s)

    lineLabel = ['F', 'P']
    style = ['r-', 'c-']  # linestyles for the different plots
    timeText = ax.text(0.30, -0.1, '', transform=ax.transAxes)
    lines = []
    lineValueText = []
    for i in range(numPlots):
        lines.append(ax.plot([], [], style[i], label=lineLabel[i])[0])
        lineValueText.append(ax.text(0.10 + i * 0.4 , 0.10, '',bbox=dict(facecolor='red', alpha=0.5), fontsize=15, transform=ax.transAxes))
    plt.rcParams['toolbar'] = 'None'
    anim = animation.FuncAnimation(fig, s.getSerialData, fargs=(lines, lineValueText, lineLabel, timeText),
                                   interval=pltInterval)  # fargs has to be a tuple

    plt.legend(loc="lower right")
    ax.set_xticks([])
    plt.box()

    root.mainloop()  # use this instead of plt.show() since we are encapsulating everything in Tkinter

    s.close()


if __name__ == '__main__':
    main()
