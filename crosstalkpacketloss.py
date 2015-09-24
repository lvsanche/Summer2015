#Packetloss measurement with the FPGA + OSA crosstalk reading on new switch
from structureFiling import *
import LivePCAPReader as PCAPReader
from sys import argv

script, filename = argv;

def main():

	

	#now time to read in some of the initial configurations
	
	#might not need this since we can save the configuration of the osa

	#Atte Configuration
	


	#now time to make the file system:
	directory = creating_direc('crosstalk&packetloss')

	

	#first making the driver wrappers
	Atte = DataCollector_agilent8156A("TCPIP::192.168.1.201::gpib0,29::INSTR", directory)
	Osa = DataCollector_agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR", directory)

	#Now the driver for everything else:
	D_sw = ivi.dicon.diconGP700("TCPIP::192.168.1.201::gpib0,3::INSTR")#this is the dicon switch
	Oscope = DataCollector_agilentDSA91304A("TCPIP::192.168.1.202::INSTR", directory) #oscope


	#Now to set the configurations 
	

	#Osa.driver._write('*RCL setup.set') #this needs to be changed to the name of the config settings

	#Oscop.driver._write(':disk:load snapshot.set') #will also need to change

	#time to open files for the different instruments and the measurements 

	#atte will not collect data so it will just be meta data
	atteFile = Atte.openFile('NoData')

	osaFile4Peaks = Osa.openFile('4Peaks_data')

	oscopeTraces = Oscope.openFile('Scope_Traces', "1")
	#make the measurements for the four peaks

	for i in range(0,1):

		att = 0
		#now to get a picture in the oscope without any att
		Atte.commandSender('input:attenuation %i' %att)
		Oscope.driver._write(':disk:load pictureSample.set')
		#Oscope.commandSender(':disk:load pictureSample.set') #to make sure we use a consitent setting when getting the shot
		for nm in range(1,5):
			D_sw.switches[1].output = nm
			Oscope.captureScreenShot(directory+"0dB_port%i.png" %nm)
			time.sleep(1)

			#time to actually attenuate
		while(att < 11): #this will iterate though the attenuator
			Atte.commandSender('input:attenuation %i' %att)

			for port in range(1,5): # will iterate through the 4 outputs
				D_sw.switches[1].output = port

				#first we get the osa readings:
				peaks = Osa.findPeaks()
				osaFile4Peaks.writerow(['Attenuation level: %i Port Num: %i Peaks: '%(att, port) , peaks ])

				#second we get a trace of the data, so configure from the config file or a different .set file
				Oscope.commandSender(':disk:load "snapshotSample.set"')
				Oscope.getTrace(0, directory+"att_%i_port_") #here goes the channel we need to get a trace from
				#oscopeTraces.writerow(['Attenuation level: %i Port Num: %i Trace:'%(att, port) , otrace ])


				#here will go the packetloss things
				PCAPReader.StartPCAPReadDaemon(filename);



			att = att+5
		break
	Osa.closeOutputs()
	Oscope.closeOutputs()
	Atte.closeOutputs()


main()