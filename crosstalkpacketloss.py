#Packetloss measurement with the FPGA + OSA crosstalk reading on new switch
from structureFiling import *
import LivePCAPReader as PCAPReader
from sys import argv

script, filename = argv;

def main():

	

	#now time to read in some of the initial configurations
	
	#might not need this since we can save the configuration of the osa

	#now time to make the file system:
	directory = creating_direc('crosstalk&packetloss')

	

	#first making the driver wrappers
	Atte = DataCollector_agilent8156A("TCPIP::192.168.1.201::gpib0,29::INSTR", directory)
	Osa = DataCollector_agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR", directory)

	#Now the driver for everything else:
	D_sw = ivi.dicon.diconGP700("TCPIP::192.168.1.201::gpib0,3::INSTR")#this is the dicon switch
	Oscope = DataCollector_agilentDSA91304A("TCPIP::192.168.1.202::INSTR", directory) #oscope


	#atte will not collect data so it will just be meta data
	atteFile = Atte.openFile('NoData')
	qfactorFile = Oscope.openFile('Color_QFactor')
	osaFile4Peaks = Osa.openFile('4Peaks_data')

	#make the measurements for the four peaks
	inputVal = "G"
	while(inputVal != "E"):
		inputVal = raw_input("To (G)o, To (E)xit: ")
		att = 0
		Atte.commandSender('input:attenuation %i' %att)

		if (inputVal == "G"):
			port = raw_input("What channel is the data input? (1-4)")
			print "Getting the four peaks..."
			peaks = Osa.findPeaks()
			osaFile4Peaks.writerow(['Attenuation level: %i Port Num: %i Peaks: '%(att, port) , peaks ])

			
			while(att < 23):
				Oscope.driver._write('display:cgrade on') #turns on the color grading, resetting in some cases
				#Both histogram box
				Oscope.setHistogram("1.01589 E-9", "1.02478 E-9", "355.16 E-6", "-351.29 E-6")
				Oscope.captureScreenShot("hist_both_att_%i" %att)
				#For the top Box now
				Oscope.setHistogram("1.01589 E-9", "1.02478 E-9", "355.16 E-6", "222.90 E-6")
				Oscope.captureScreenShot("hist_top_att_%i" %att)
				#For the bottom box now
				Oscope.setHistogram("1.01589 E-9", "1.02478 E-9", "-212.58 E-6", "-351.29 E-6")
				Oscope.captureScreenShot("hist_bottm_att_%i" %att)

				#now to get the qfactor
				Oscope.saveQFactor(att, qfactorFile)


				
				#insert the bert things here 
				att = att + 3
				Atte.commandSender('input:attenuation %i' %att)

	Osa.closeOutputs()
	Oscope.closeOutputs()
	Atte.closeOutputs()


main()