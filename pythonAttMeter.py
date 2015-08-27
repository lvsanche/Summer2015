import Tkinter
from Tkinter import *


#gui things

def meter():
	osaAmpPeak1 = 0
	osaAmpPeak2 = 0
	osaWvPeak1=0
	osaWvPeak2=0


	window = Tkinter.Tk()
	#osa is the driver and will be used to get some values
	#SETTING UP GUI
	variableString1 = Tkinter.StringVar()
	variableString2 = Tkinter.StringVar()
	
	ampText1 = Tkinter.Label(window, bd= 5, textvariable=variableString1, state='active')
	ampText2 = Tkinter.Label(window, bd= 5, textvariable=variableString2, state='active')
	
	variableString1.set("Peak 1 Amps: %f, Wavelength: %f " %(osaAmpPeak1, osaWvPeak1))
	variableString2.set("Peak 2 Amps: %f, Wavelength: %f " %(osaAmpPeak2, osaWvPeak2))
	ampText1.pack()
	ampText2.pack()
	butt =  Tkinter.Button(window, text="Get Trace", command=getTrace )
	butt.pack()
	window.mainloop()

	while True:
		#make the updating ever second or so
		#osa.get everything
		variableString1.set("Peak 1 Amps: %f, Wavelength: %f " %(osaAmpPeak1, osaWvPeak1))
		variableString2.set("Peak 2 Amps: %f, Wavelength: %f " %(osaAmpPeak2, osaWvPeak2))
		


def getTrace():
	traceWindow = Tkinter.Tk()
	label2 = Tkinter.Label(traceWindow, text="File to Save to", anchor='w', state='active')
	entry2 = Tkinter.Entry(traceWindow, bd=5)
	label2.pack()
	entry2.pack()
	label = Tkinter.Label(traceWindow, text="Note on trace:", anchor='w',state='active')
	label.pack()
	entry = Tkinter.Entry(traceWindow, bd =5)
	entry.pack()
	button = Tkinter.Button(traceWindow, text="SaveTrace", command=saveTrace)
	button.pack()
	traceWindow.mainloop()

def saveTrace():
	outputFileTrace = entry2.get()
	outputFileTraceNote = entry.get()
	print outputFileTraceNote
	print outputFileTrace
	#will call the trace getting function in the osa and save the trace to a file
	"""trace = []
	trace = osa.read_y(0)
	outFileObj = open(outputFileTrace, 'w')
	outFileObj.write(outputFileTraceNote)
	for traceValue in trace:
		outFileObj.write("%f \n", %traceValue)
	outFileObj.close()"""

meter()