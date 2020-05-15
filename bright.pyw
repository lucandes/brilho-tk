#!/usr/bin/env python3
#coding: UTF-8
import tkinter as tk
from tkinter import ttk
import subprocess as sub
import os

class App:
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("300x200")
		self.root.title("Ajuste de Brilho")
		self.root.resizable(False, False)

		self.displays = []
		self.getDisplays()
		self.displaysCurrentValue = []
		self.getDisplaysDefaultValue()
		self.numOfDisplays = len(self.displays)

		self.loadWidgets()
		self.setBrightness(self.displaysCurrentValue[0])
		self.root.mainloop()

	def loadWidgets(self):
		# first frame
		frame1 = tk.LabelFrame(self.root, text="Saída", width=280, height=70)
		frame1.pack_propagate(0)
		frame1.place(x=10, y=0)

		# displays list menu
		self.displaybox = ttk.Combobox(frame1, values=self.displays, width=20)
		self.displaybox.current(0)
		self.displaybox.bind("<<ComboboxSelected>>", self.setSliderToValue)
		self.displaybox.pack(pady=10)

		# second frame
		frame2 = tk.LabelFrame(self.root, text="Nível de brilho", width=280, height=70)
		frame2.pack_propagate(0)
		frame2.place(x=10, y=70)

		# bright slider
		self.brightSlider = tk.Scale(frame2, from_=10, to=100)
		self.brightSlider.set(self.displaysCurrentValue[0])
		self.brightSlider.config(orient=tk.HORIZONTAL, length=250)
		self.brightSlider['command'] = self.setBrightness
		self.brightSlider.pack()

		# buttons frame
		frame3 = tk.Frame(self.root, width=280, height=70)
		frame3.place(x=10, y=150)

		# buttons
		self.saveBtn = tk.Button(frame3, text="Salvar", width=7)
		self.saveBtn['command'] = self.saveConfig
		self.saveBtn.pack(side=tk.LEFT, padx=5)
		
		self.restoreBtn = tk.Button(frame3, text="Restaurar", width=7)
		self.restoreBtn['command'] = self.restoreBrightnessValues
		self.restoreBtn.pack(side=tk.LEFT, padx=3)

		self.exitBtn = tk.Button(frame3, text="Fechar", width=7)
		self.exitBtn['command'] = self.root.quit
		self.exitBtn.pack(side=tk.LEFT, padx=5)

	def getDisplays(self):
		outputList = sub.getoutput("xrandr --query | grep connected -w")
		outputList = outputList.split("\n")
		for output in outputList:
			self.displays.append(output.split(" ")[0])

	def getDisplaysDefaultValue(self):
		outputCurValue = sub.getoutput("xrandr --verbose | grep -i brightness")
		outputCurValue = outputCurValue.split("\n")
		for output in outputCurValue:
			self.displaysCurrentValue.append(float(output.split(' ')[-1]) * 100)

		self.readConfFile()

	def setBrightness(self, brightnessLevel):
		self.displaysCurrentValue[self.displaybox.current()] = int(brightnessLevel)
		for i in range(self.numOfDisplays):
			command = "xrandr --output " + self.displays[i] + " --brightness " + str(self.displaysCurrentValue[i] / 100)
			os.system(command)

	def setSliderToValue(self, event):
		displayIndex = self.displays.index(self.displaybox.get())
		self.brightSlider.set(self.displaysCurrentValue[displayIndex])

	def restoreBrightnessValues(self):
		for i in range(self.numOfDisplays):
			self.displaysCurrentValue[i] = 100
		self.setBrightness(100)
		self.brightSlider.set(100)

	def saveConfig(self):
		confFile = open(".conf", "w")
		for i in range(self.numOfDisplays):
			confFile.write(self.displays[i] + " " + str(int(self.displaysCurrentValue[i])) + "\n")
		confFile.close()

	def readConfFile(self):
		try:
			confFile = open(".conf", "r")
		except FileNotFoundError:
			return

		confDisplays = confFile.readlines()

		for i in range(len(confDisplays)):
			confDisplays[i] = confDisplays[i].replace("\n", "")
			if confDisplays[i].split(" ")[0] in self.displays:
				indexDisplay = self.displays.index(confDisplays[i].split(" ")[0])
				self.displaysCurrentValue[indexDisplay] = int(confDisplays[i].split(" ")[1])
				
		return 1

main = App()