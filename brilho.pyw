#!/usr/bin/env python3
#coding: UTF-8
import tkinter as tk
from tkinter import ttk
import subprocess as sub
import os

class Display:
	def __init__(self, name, brightness=100):
		self.name = name
		self.brightness = brightness

	def getBrightness(self):
		return self.brightness
	def setBrightness(self, brightness):
		self.brightness = brightness

	def getName(self):
		return self.name
	def setName(self, name):
		self.name = name

class App:
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("300x200")
		self.root.title("Ajuste de Brilho")
		self.root.resizable(False, False)

		self.displays = []
		self.getDisplays()
		self.numOfDisplays = len(self.displays)
		self.displayNameslist = []
		for i in range(self.numOfDisplays):
			self.displayNameslist.append(self.displays[i].getName())

		self.loadWidgets()
		self.setDisplayBrightness(self.displays[0].getBrightness())
		self.root.mainloop()

	def loadWidgets(self):
		# first frame
		frame1 = tk.LabelFrame(self.root, text="Saída", width=280, height=70)
		frame1.pack_propagate(0)
		frame1.place(x=10, y=0)

		# displays list menu
		self.displaybox = ttk.Combobox(frame1, values=self.displayNameslist, width=20)
		self.displaybox.current(0)
		self.displaybox.bind("<<ComboboxSelected>>", self.setSliderToValue)
		self.displaybox.pack(pady=10)

		# second frame
		frame2 = tk.LabelFrame(self.root, text="Nível de brilho", width=280, height=70)
		frame2.pack_propagate(0)
		frame2.place(x=10, y=70)

		# bright slider
		self.brightnessSlider = tk.Scale(frame2, from_=10, to=100)
		self.brightnessSlider.set(self.displays[0].getBrightness())
		self.brightnessSlider.config(orient=tk.HORIZONTAL, length=250)
		self.brightnessSlider['command'] = self.setDisplayBrightness
		self.brightnessSlider.pack()

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
		output = sub.getoutput("xrandr --verbose| grep 'connected\\|brightness' -w -i")
		output = output.split("\n")
		counter = 0
		while counter < len(output):
			if 'brightness' in output[counter + 1].lower():
				newDisplay = output[counter].split(" ")[0]
				newBrightness = float(output[counter + 1].split(" ")[-1]) * 100
				self.displays.append(Display(newDisplay, int(newBrightness)))
				counter += 2
			else:
				counter += 1

	def setDisplayBrightness(self, brightnessLevel):
		selectedDisplay = self.displaybox.current()
		self.displays[selectedDisplay].setBrightness(int(brightnessLevel))
		for i in range(self.numOfDisplays):
			print(self.displays[i].getName(), "brightness:", self.displays[i].getBrightness())
			command = "xrandr --output " + self.displays[i].getName() + " --brightness " + str(self.displays[i].getBrightness() / 100)
			os.system(command)

	def setSliderToValue(self, event):
		displayIndex = self.displayNameslist.index(self.displaybox.get())
		self.brightnessSlider.set(self.displays[displayIndex].getBrightness())

	def restoreBrightnessValues(self):
		for i in range(self.numOfDisplays):
			self.displays[i].setBrightness(100)
		self.setDisplayBrightness(100)
		self.brightnessSlider.set(100)

	def saveConfig(self):
		confFile = open(".conf", "w")
		for i in range(self.numOfDisplays):
			confFile.write(self.displays[i].getName() + " " + str(int(self.displays[i].getBrightness())) + "\n")
		confFile.close()

	def readConfFile(self):
		try:
			confFile = open(".conf", "r")
		except FileNotFoundError:
			return

		confDisplays = confFile.read().split("\n")
		for i in range(len(confDisplays)):
			if confDisplays[i].split(" ")[0] in self.displayNameslist:
				indexDisplay = self.displayNameslist.index(confDisplays[i].split(" ")[0])
				self.displays[indexDisplay].setBrightness(int(confDisplays[i].split(" ")[1]))
				
		return 1

main = App()