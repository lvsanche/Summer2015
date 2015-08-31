from structureFiling import *
import matplotlib.pyplot as plt
import ivi
import time

#master script that will run everything


def main():
	#somewhere I need a loop as we will do a few repetitions with the packet loss thing
	#as well as with the instrument measurements

	#Instruments:
	#switch = ivi.dicon.diconGP700("TCPIP::192.168.1.201::gpib0,3::INSTR")
	#att = ivi.agilent.agilent8156A("TCPIP::192.168.1.201::gpib0,29::INSTR")
	#osa = ivi.agilent.agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR")



	#measurement name
	fileName = "Test" #to be changed accordingly 

	#osa._timeout = 30 #delaying the timeout 
	#making the file Structure and the shelve
	shelveName = creating_direc("crosstalOnChip")
	shelv = shelve.open(shelveName)

	#list of things to be measured
	#must get all the osa peak readings
	#that consists of two values, one for the peak and one for the wavelength
	peakPower = [None] *4

	portNumber = input("Which port should be the output to OSA ? (-1 to exit)")
	fileOut = open(fileName, 'w')
	while(portNumber!=-1):
		
		#the number in the brackets is the module number
		#switch.switches[1].output = int(portNumber)

		time.sleep(1)

		#osa._write('calculate1:marker1:maximum')
		
		#peakPower[portNumber-1]= float(osa._ask(calculate1:marker1:Y?))
			
		fileOut.write("%f " %portNumber)
		fileOut.write("%f \n" %peakPower[portNumber-1])
		
		portNumber = input("Which port should be the output? (-1 to exit)")


	shelv["PowerOnPorts[]"] = peakPower


	shelv.close()
	fileOut.close()
	#list of things to be ultimately graphed 
	plt.plot([1,2,3,4], peakPower)
	plt.show()

main()
