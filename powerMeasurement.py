from structureFiling import *
import matplotlib.pyplot as plt
import ivi
import time
import numpy as np
#master script that will run everything


def main():
	#somewhere I need a loop as we will do a few repetitions with the packet loss thing
	#as well as with the instrument measurements

	#Instruments:
	#switch = ivi.dicon.diconGP700("TCPIP::192.168.1.201::gpib0,3::INSTR")
	#att = ivi.agilent.agilent8156A("TCPIP::192.168.1.201::gpib0,29::INSTR")
	#osa = ivi.agilent.agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR")



	#measurement name
	fileName = "SampleTest" #to be changed accordingly 
	shelveName = creating_direc(fileName)
	shelv = shelve.open(shelveName)
	inputPortNum = -1;
	#osa._timeout = 30 #delaying the timeout 

	#list of things to be measured
	#must get all the osa peak readings
	#that consists of two values, one for the peak and one for the wavelength
	peakPower = [0] *4

	
	#setting things up for graphing
	ind = np.arange(16) #there is 16 possible combinations 
	allPowers = [0]*16


	inputVal = 0
	while(inputVal != "E"):
		inputVal = raw_input("Possible commands:(I)nput Configuration, (P)ort Output Selection, (E)xit: ")
		
		

		if inputVal == "I":
			print("Current inputPort: %i" %inputPortNum)
			inputPortNum = input ("What is the desired input port? ")
			fileN = fileName
			fileN += "_inPort%i" %inputPortNum
			fileOut = open(fileN, 'w')
		elif inputVal == "P":
			portNumber = input("Which port should be the output to OSA ? [1-4]: ")
			while(portNumber!=-1):
		
				#the number in the brackets is the module number
				#switch.switches[1].output = int(portNumber)

				time.sleep(1)

				#osa._write('calculate1:marker1:maximum')
				peakPower[portNumber-1] = input("any number: ")
				#peakPower[portNumber-1]= float(osa._ask(calculate1:marker1:Y?))
			
				fileOut.write("%f " %portNumber)
				fileOut.write("%f \n" %peakPower[portNumber-1])
				print ("Measurement taken and saved for in port: %i & output port:  %i"
			    %(inputPortNum, portNumber))
				portNumber = input("Which port should be the output? (-1 to exit): ")
			keyVal = "PowerOnPortInput[%i]" %inputPortNum
			shelv[keyVal] = peakPower
			for numb in range(0,4):
				allPowers[(inputPortNum-1)*4 + numb] = peakPower[numb]

			fig, ax = plt.subplots()
			rects = ax.bar(ind, allPowers , 0.25, color='r')
			ax.set_ylabel("dbs")
			ax.set_xlabel("Input Port *4  + Output Port ")
			plt.show()
			fileOut.close()
		elif inputVal == "E":
			break

	


	shelv.close()
	fileOut.close()
	

main()
