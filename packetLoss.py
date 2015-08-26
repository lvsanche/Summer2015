import visa
import ivi
import time
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
	"""inputArgs = str(sys.argv)
	fileObj = open( inputArgs[1], 'r')
	#file will be in the same sequence as in the variables
	attenuation = float(fileObj.readline())
	attMin = float(fileObj.readline())
	attMax = float(fileObj.readline())
	offset = float(fileObj.readline())
	wavelength = float(fileObj.readline())
	attenuationStep = float(fileObj.readline())
	fileObj.close()"""

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


main()
#still need to send out the scapy information into some background saving system

