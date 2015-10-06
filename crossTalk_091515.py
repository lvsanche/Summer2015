#new crosstalk measurement
#date 15th september 2015

from structureFiling import *

def main():
	directory = creating_direc('crossTalk_091515') #change this to be the name of the directory, perhaps just the method name

	portName = "port_"


	osa = DataCollector_agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR", directory)
	switch = ivi.dicon.diconGP700("TCPIP::192.168.1.201::gpib0,3::INSTR")

	osaFileCrossPeaks = osa.openFile('Peaks') #call this so you know what measurement was made with this instrument
	osaFileCrossPeaks.writerow(['# Outputs: 1 2 3 4'])
		
	inputVal = 0
	inputPortNum = -1
	while(inputVal != "E"):
		inputVal = raw_input("Possible commands:(I)nput Configuration, (O)utput sweep, (E)xit: ")
		
		

		if inputVal == "I":
			print("Current inputPort: %i" %inputPortNum)
			inputPortNum = input ("What is the desired input port? ")
			portPeaks = [0] *4
			portnam = portName + str(inputPortNum) +"# "
		elif inputVal == "O":
			print "Now sweeping..."
			for port in range(4):
				p = port + 1
				print "Port %d is being checked..." %p
				
				switch.switches[1].output = p 

				time.sleep(5) 

				osa.driver._write('calculate1:marker1:maximum')
				
				portPeaks[port]= float(osa.driver._ask('calculate1:marker1:Y?'))
				time.sleep(5)

			osaFileCrossPeaks.writerow([portnam, portPeaks])

		elif inputVal == "E":
			break

	osa.closeOutputs()

main()
