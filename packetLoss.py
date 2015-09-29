import visa
import ivi
import time
from structureFiling import *
#import the scapy module

def main():
	#will read the settings for the agilent attinuator

	#VARIABLES:
	attenuation = 0 #in dB MAX=  MIN= 
	attMin = 0
	attMax = 20#0
	offset = 0 #in dB MAX= MIN= 
	wavelength = 1550 #0 # in meters MAX= MIN=
	attenuationStep= 1 #0 #in dB, to be the increment

	#READING IN CONFIG:
	
	fileObj = open( "config.txt", 'r')
	#file will be in the same sequence as in the variables
	attenuation = float(fileObj.readline())
	attMin = float(fileObj.readline())
	attMax = float(fileObj.readline())
	offset = float(fileObj.readline())
	wavelength = float(fileObj.readline())
	attenuationStep = float(fileObj.readline())
	fileObj.close()

	#once done it is time to set up the attunuator with the driver
	att = ivi.agilent.agilent8156A("TCPIP::192.168.1.201::gpib0,28::INSTR") 
	if attenuation > attMin:
		if attenuation < attMax:
			att._set_attenuation(attenuation)
	
	att._set_offset(offset)
	att._set_wavelength(wavelength)
	att._set_disable(0)


	#will have to loop through the whole set up, and then calling in the 
	while True:
		if attenuation+attenuationStep < attMax:
			attenuation = attenuation+attenuationStep
			att._set_attenuation(attenuation)
			#here we have the ten second wait and the calls for the scapy thing
			time.sleep(2) # delays for 5 seconds
		else:
			break


#main()
#still need to send out the scapy information into some background saving system


def packetloss_2015_9_28():


	#VARIABLES:
	attMin = 0
	attMax = 20#0
	attenuationStep= 1 #0 #in dB, to be the increment


	#making the directory:
	directory = creating_direc("packetloss_2015_9_28+attenuation")

	att = DataCollector_agilent8156A("TCPIP::192.168.1.201::gpib0,28::INSTR", directory) 
	oscop = DataCollector_agilent91304A("TCPIP::192.168.1.202::INSTR", directory)	
	
	att.configFromFile()
	att.openFile("METADATA")


	for atten in range(attMin, attMax, attenuationStep):
		att.commandSender("set:attenuation %i" %atten)

		outputWriter = oscop.openFile("att_%i_trace" %atten, 0 )
		oscop.getTrace(0,outputWriter)

		#bit error rate thing after we get a trace 
		#might need to have some csv writer here to get a file with the bit error numbers just to keep

		oscop.closeOutputs() #so that the file is closed correctly 

	att.closeOutputs()
	

