# encoding: utf-8
'''
Created on 2016��9��14��

@author: ruanhuabin
'''
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from _functools import partial

import tkMessageBox
import time
from threading import Thread
from Logger2 import MyLogger
import os
from LipidProcessor import *

def getCurrTime():    
    st = time.localtime()
    year = st.tm_year
    month = st.tm_mon
    day = st.tm_mday
    hour = st.tm_hour
    miniute = st.tm_min
    sec = st.tm_sec
    
    strTime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + "-" + str("%02d" % hour) + ":" + str("%02d" % miniute) + ":" + str("%02d" % sec)
    
    return strTime
class LipidFrame:
    def __init__(self, master):
        frame = Frame(master,width=400,height=600)
        frame.pack()   
        
        self.inputFolderPath =StringVar()
        self.labelFolder = Label(frame,textvariable=self.inputFolderPath).grid(row=0,columnspan=2)
        
        self.log_file_btn = Button(frame, text="Select Lipid File", command=self.selectInputFile).grid(row=1, columnspan=2)
        
        self.outputFolderPath = StringVar()
        self.labelImageFile = Label(frame,textvariable = self.outputFolderPath).grid(row = 2, columnspan = 2)
        self.output_folder_btn = Button(frame, text="Output Folder", command=self.selectOutputFolder,width=40).grid(row=3, columnspan=2)
        
        self.blankText = StringVar()
        self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 4, columnspan = 2)
        
        self.output_filename_label = Label(frame, text="Output File Name:          ")#.grid(row=5, columnspan=2)
        self.output_filename_label.grid(row=5, columnspan=2)
       
        self.output_filename_entry = Entry(frame, width=30, bd = 4)
        self.output_filename_entry.grid(row=6, column=0, columnspan=2)
        
        
        f = frame
        xscrollbar = Scrollbar(f, orient=HORIZONTAL)
        xscrollbar.grid(row=12, column=0, sticky=N+S+E+W)
 
        yscrollbar = Scrollbar(f)
        yscrollbar.grid(row=11, column=1, sticky=N+S+E+W)
 
        self.text_field = Text(f, wrap=NONE,
                    xscrollcommand=xscrollbar.set,
                    yscrollcommand=yscrollbar.set)
        self.text_field.grid(row=11, column=0)
 
        xscrollbar.config(command=self.text_field.xview)
        yscrollbar.config(command=self.text_field.yview)
        
        self.blankText = StringVar()
        self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 14, columnspan = 2)
        self.thresholdFolderPath =StringVar()
        self.conditionFolder = Label(frame,textvariable=self.thresholdFolderPath).grid(row=16,columnspan=2)
        
        self.log_file_btn = Button(frame, text="Select Threshold File", command=self.selectThresHoldFile).grid(row=17, columnspan=2)
        
        self.isFolderPath =StringVar()
        self.isFolder = Label(frame,textvariable=self.isFolderPath).grid(row=19,columnspan=2)
        
        self.log_file_btn = Button(frame, text="      Select IS File      ", command=self.selectISFile).grid(row=20, columnspan=2)
      

        
        
        self.blankText = StringVar()
        self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 7, columnspan = 2)
        
        self.start_run_btn = Button(frame, text="Start Processing", command=partial(self.startProcessing, self.text_field), width=40)
        self.start_run_btn.grid(row=8, columnspan=2)
        
        self.blankText = StringVar()
        self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 9, columnspan = 2)
        self.counter = 0
        
        self.inputDataBook = {}
        self.outputDataBook = {}
        self.inputFilename = ""
        
        self.logger = MyLogger(logFileName='lipid_processor.log').getLogger()
        
        
    def selectISFile(self):
        filename = askopenfilename()
        self.isFolderPath.set(filename)
        self.isFileName = filename
        
       
    def selectThresHoldFile(self):
        filename = askopenfilename()
        self.thresholdFolderPath.set(filename)
        self.thresHoldFileName = filename    

  

    def selectInputFile(self):
        filename = askopenfilename()
        self.inputFolderPath.set(filename)
        self.inputFilename = filename
        
       
        dirName = os.path.dirname(filename)
        baseName = os.path.basename(filename)
        
        baseNamePrefix = baseName.split(".")[0]
        baseNamePrefix = baseNamePrefix + "-filter"
        
        outputFilename = baseNamePrefix + ".xlsx"
        
#         self.logger.info("dir name = " + dirName)
#         self.logger.info("base name = " + baseName)
        self.outputFolderPath.set(dirName)
        self.output_filename_entry.delete(0, END)
        self.output_filename_entry.insert(0, outputFilename)  
       

    def selectOutputFolder(self):
        imageFolder = askdirectory()
        self.outputFolderPath.set(imageFolder)
        
    def run_thread(self, text_field, inputFileName, thresholdFileName, isFileName, outputFileName):
        
        text_field.insert(INSERT, "[%s]: Start to Process file: %s\n" % (getCurrTime(), self.inputFolderPath.get()))
        self.logger.info( "Start to Process file:" + self.inputFolderPath.get())     
        
        
        runFilter(inputFileName, thresholdFileName, isFileName, outputFileName)
        
        
        text_field.insert(INSERT, "[%s]: Job Complete Successfully, Output File Name: %s!!! \n" %(getCurrTime(), outputFileName))
        text_field.see("end")
        time.sleep(1)
        
        
        self.logger.info("Job Complete Successfully, Output File Name: %s!!! \n" %(outputFileName))
        self.start_run_btn.configure(state=NORMAL)
        
    
    def startProcessing(self, text_field):
        if(self.inputFolderPath.get() == ""):
            tkMessageBox.showerror("Error", "Please select a lipid file to be processed")
            return
        
        if(self.thresholdFolderPath.get() == ""):
            tkMessageBox.showerror("Error", "Please select a threshold file to be processed")
            return
        
        if(self.isFolderPath.get() == ""):
            tkMessageBox.showerror("Error", "Please select a IS file to be processed")
            return
        if(self.outputFolderPath.get() == ""):
            self.outputFolderPath.set("./")

        if(self.output_filename_entry.get() == ""):           
            tkMessageBox.showerror("Error", "Please enter a filename for the output file" )
            return
            
        outputFolderPath = self.outputFolderPath.get()
        if(outputFolderPath[-1] != '/'):
            outputFolderPath = outputFolderPath + "/"
            
        outputFilename = outputFolderPath + self.output_filename_entry.get()
        
        filenameExtension = outputFilename.split(".")[-1]
        if(filenameExtension != "xlsx"):
            outputFilename = outputFilename + ".xlsx"
        
        
        self.start_run_btn.configure(state=DISABLED)
        newThread = Thread(target = self.run_thread, args=(text_field, self.inputFilename, self.thresHoldFileName, self.isFileName, outputFilename))
        newThread.start()

def run_lipid_processor():  
    mainFrame = Tk()
    mainFrame.title("Lipid Data Processor")
    mainFrame.geometry("600x800")
    mainFrame.resizable(False, False)
    app = LipidFrame(mainFrame)
    mainFrame.mainloop()


if __name__ == '__main__':
    run_lipid_processor()

    pass