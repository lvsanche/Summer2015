import ivi
import time
import visa
#date: August 19th 2015

osa =0 #this will be a global variable 
outputFileTrace = ""
outputFileTraceNote = ""

def main():
	


	#VARIABLES:
	attenuation_Main = 0 #in dB MAX=  MIN= 
	attMin_Main = 0
	attMax_Main = 0#0
	offset_Main = 0 #in dB MAX= MIN= 
	wavelength_Main = 0 #0 # in meters MAX= MIN=
	attenuationStep_Main= 1 #0 #in dB, to be the increment

	attenuation_sec = 0
	attMin_sec = 0
	attMax_sec = 0
	offset_sec = 0
	wavelength_sec = 0
	attenuationStep_sec = 0

	#READING VARIABLES
	osa_wavelength1 = 0 
	osa_wavelength2 = 0
	osa_amp1 = 0
	osa_amp2 = 0
	#format_output1= "Wavelength Peak 1: %l Amp: %l " %(osa_wavelength1, osa_amp1)
	#format_output2= "Wavelength Peak 2: %l Amp: %l " %(osa_wavelength2, osa_amp2)




	#READING IN CONFIG:
	fileObj = open( "config_cross.txt", 'r')
	#file will be in the same sequence as in the variables
	attenuation_Main = float(fileObj.readline().rstrip())
	attMin_Main = float(fileObj.readline().rstrip())
	attMax_Main = float(fileObj.readline().rstrip())
	offset_Main = float(fileObj.readline().rstrip())
	wavelength_Main = float(fileObj.readline().rstrip())
	attenuationStep_Main = float(fileObj.readline().rstrip())

	attenuation_sec = float(fileObj.readline().rstrip())
	attMin_sec = float(fileObj.readline().rstrip())
	attMax_sec = float(fileObj.readline().rstrip())
	offset_sec = float(fileObj.readline().rstrip())
	wavelength_sec = float(fileObj.readline().rstrip())
	attenuationStep_sec = float(fileObj.readline().rstrip())
	fileObj.close()


	#INSTRUMENTS
	"""att_combination = ivi.agilent.agilent8156A("TCPIP::192.168.1.201::gpib0,28::INSTR") #this will attenuate the combined signal
	att_second_signal = ivi.agilent.agilent8156A("TCPIP::192.168.1.201::gpib0,29::INSTR")
	osa = ivi.agilent.agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR")#this is the osa
"""

	#CONFIGURING INSTRUMENTS

	if attenuation_Main > attMin_Main:
		if attenuation_Main < attMax_Main:
			att_combination._set_attenuation(attenuation_Main)

	if attenuation_sec > attMin_sec:
		if attenuation_sec < attMax_sec:
			att_second_signal._set_attenuation(attenuation_sec)

	"""
	att_combination._set_offset(offset_Main)
	att_combination._set_wavelength(wavelength_Main)
	att_combination._set_disable(0)

	att_second_signal._set_offset(offset_sec)
	att_second_signal._set_wavelength(wavelength_sec)
	att_second_signal._set_disable(0)
	"""

	#SETTING UP THE PACKET SENDER
	number = 1
	#fileHeader = "This file contains the run #%i, with the packetless line being attenuated at %i dB" %(,)
	#EVERYTHING COMING TOGETHER
	while(attenuation_sec<attMax_sec):
		
		fileHeader = "This file contains the run #%i, with the packetless line being attenuated at %i dB" %(number, attenuation_sec)
		fileName = "Trial%i_att%i.txt" %(number, attenuation_sec)
		fileObjW = open (fileName, 'w')
		fileObjW.write(fileHeader)
		#going to loop through attenuations on the second signal and then on the smaller one
		attenuation_Main = attMin_Main
		while(attenuation_Main<attMax_Main):
			"""#send the method to the packet maker and return a count of that
 			osa._write('calculate1:marker1:maximum')
			osa._write('calculate1:marker1:X?')
			#osa._read(markx)
			osa._write('calculate1:marker1:Y?')
			#osa._read(marky)
			osa._write('calculate1:marker1:maximum:next')
			osa._write('calculate1:marker1:X?')
			#osa_wavelength2 = osa_read(markx)
			osa._write('calculate1:marker1:Y?')
			#osa_amp2 = osa._read(marky)

			#sending the packets here 

			fileObjW.write("%f %f %f %f %f %f\n") %(attenuation_Main, packetsReceived, osa_wavelength1, osa_amp1, osa_wavelength2, osa_amp2 )
			#combined signal att level, #of packets received, peak1 wv, peak1 amp, peak2 wv, peak 2 amp

			"""
			print "Inner loop: mainAtt: %f SecAtt: %f" %(attenuation_Main, attenuation_sec)
  			
 			attenuation_Main = attenuation_Main+attenuationStep_Main
			#att_combination._set_attenuation(attenuation_Main)
			


		fileObjW.close()
		attenuation_sec = attenuation_sec+attenuationStep_sec
		#att_second_signal._set_attenuation(attenuation_sec)
		number = number +1
		
		
		



main()



	

