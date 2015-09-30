import time
import os
import ivi
import csv
#Date: Summer 2015
#Author: Luis Sanchez
#Email: lvsanche@ucsd.edu

"""Method that will make the directory for the day and the trial you are about to run
@param methodName should be the name of the method that is calling this function
@return returns a string of the directory that was fabricated based on the time
		if it already exists then then the full directory  is still returned 
"""
def creating_direc(methodName):
	#look for experimentname + date folder 
	date = time.strftime("%Y_%m_%d")
	clock = time.strftime("%H:%M:%S")
	dire = "./%s/%s/trial_%s/" %(methodName, date, clock)
	
   	d = os.path.dirname(dire)
   	if not os.path.exists(d):
   		os.makedirs(d)

   	return dire


"""This is a class wrapper building off from the IVI python library of drivers.
The Methods will help in the collection of the data when running tests
Meta data will automatically be collect during the initialization.
For this particular model, there is not much data collection but there will be logs
of all the methods that were sent to the instruments.
"""
class DataCollector_agilent8156A:
	"""init method to create the ivi driver and change the timeout interface 
	must pass in the string with the address to the instrument as well as the output
	from the creating_direc method 
	@param address is the string that is used for the ivi driver creator
	@param direc where output files will be placed 
	"""
	def __init__(self, address, direc):
		self.driver = ivi.agilent.agilent8156A(address)
		self.driver._interface.timeout = 30
		self.outputFiles = [] #there could be several files outputting things
		self.directory = direc
		f = open(self.directory+".agilent8156A_commandLog", 'ab')
		self.logFileWriter = csv.writer(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
		self.outputFiles.append(f)
   

	def configFromFile(self):
		attConF = open('atteConfig', 'r')
		attenuation = float(attConF.readline().split(' #')[0])
		wavelength = float(attConF.readline().split(' #')[0])
		offset = float(attConF.readline().split(' #')[0])
		attConf.close()
		self.driver._set_attenuation(attenuation)
		self.driver._set_wavelength(wavelength)
		self.driver._set_offset(offset)
		self.driver._set_disable(0) #this turns it on


	"""
	This method will create a new file in the directory that was passed in the
	constructor of this object.
	@param measurementToRecord is what you want to name the measurement being
		made with the instrument
	@return the return is a filewriter which you can letter send direct strings
		to or use to pass to other methods that automate the data gathering process
	""" 
	def openFile(self, measurementToRecord):
		nameOfFile = self.directory+"agilent8156A_"+measurementToRecord
		file = open(nameOfFile, 'ab')
		fileWriter = csv.writer(file, quotechar ='|', quoting=csv.QUOTE_MINIMAL)
		self.outputFiles.append(file)

		#time to gather metadata and put in the file:
		fileWriter.writerow(['ID: ', self.driver._load_id_string()])
		fileWriter.writerow(['Attenuation: ', self.driver._get_attenuation()])
		fileWriter.writerow(['Offset: ', self.driver._get_offset() ])
		fileWriter.writerow(['Wavelength: ', self.driver._get_wavelength()])
		fileWriter.writerow(['Enabled: ', self.driver._get_disable()])
		fileWriter.writerow(['END OF META DATA'])
		

		return fileWriter

	"""
	This method will help send a method using ._ask()
	and then gather the data and output with the use of the file writer
	@param command string of what needs to be sent to the ._ask function
	@param fileOutputWriter this is the csv writer for the measurement you are 
		trying to make, usually something that comes from the openFile method
	"""
	def sendDataCommand(self, command, fileOutputWriter):
		data = self.driver._ask(command)
		fileOutputWriter.writerow(['%s- Command %s yielded: ' %(time.strftime("%H:%M:%S"),command), data])

	"""
	This method will use ._write() to send a message to the driver
	and will also log the command that was passed into the instrument with a time
	@param command is what you want to send to the instrument
	"""
	def commandSender(self, command):
		self.driver._write(str(command))
		self.logFileWriter.writerow(['%s- Command: %s' %(time.strftime("%H:%M:%S"),str(command))])

	"""
	This simple method should be called at the end when the instrument is not to be used any longer
	as it closes out all the files which if done incorrectly might result in unwritten files
	AND NO ONE WANTS THAT
	"""
	def closeOutputs(self):
		for writer in self.outputFiles:
			writer.close()

class DataCollector_agilent86142B:

	"""init method to create the ivi driver and change the timeout interface 
	must pass in the string with the address to the instrument as well as the output
	from the creating_direc method 
	@param address is the string that is used for the ivi driver creator
	@param direc where output files will be placed 
	"""
	def __init__(self, address, direc):
		self.driver = ivi.agilent.agilent86142B(address)
		self.driver._interface.timeout=30
		self.outputFiles = []
		self.directory = direc
		f = open(self.directory+".agilent8156A_commandLog", 'ab')
		self.logFileWriter = csv.writer(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
		self.outputFiles.append(f)

	def configFromFile(self):
		#OSA Configuration:
		osaConF =  open("osaConfig", 'r')
		startSweep = int(osaConF.readline().split(' #')[0])
		endSweep = int(osaConF.readline().split(' #')[0])
		#will add other things here
		osaConF.close()


	def findPeaks(self):
		self.logFileWriter.writerow(['%s- Command %s' %(time.strftime("%H:%M:%S"),"Peaks Found")])
		self.driver._write('CALCulate1:MARKer1:MAXimum')
		peaksY = [0]*4
		peaksX = [0]*4
		for i in range(0,4):
			peaksX[i] =self.driver._ask('calculate1:marker1:X?') 
			peaksY[i] = self.driver._ask('calculate1:marker1:Y?')
			if (i != 3):
				self.driver._write('CALCulate1:MARKer1:MAXimum:NEXT')
			time.sleep(1)
		results = zip(peaksX,peaksY)
		return results

	#def saveSet(self, nameForSet):
		#self.driver._write(*)
	"""
	This method will create a new file in the directory that was passed in the
	constructor of this object.
	@param measurementToRecord is what you want to name the measurement being
		made with the instrument
	@return the return is a filewriter which you can letter send direct strings
		to or use to pass to other methods that automate the data gathering process
	"""
	def openFile(self, measurementToRecord):
		nameOfFile = self.directory+'agilent86142B_'+measurementToRecord
		file = open(nameOfFile, 'wb')
		fileWriter = csv.writer(file, quotechar ='|', quoting=csv.QUOTE_MINIMAL)
		self.outputFiles.append(file)

		#time to gather metadata and put in the file:
		fileWriter.writerow(['ID: ', self.driver._load_id_string()])
		fileWriter.writerow(['Acquisition Detector type', self.driver._get_acquisition_detector_type() ])
		fileWriter.writerow(['Start Wavelength', self.driver._get_wavelength_start() ])
		fileWriter.writerow(['Stop Wavelength', self.driver._get_wavelength_stop() ])
		fileWriter.writerow(['Wavelength Offset', self.driver._get_wavelength_offset() ])
		fileWriter.writerow(['Level Reference', self.driver._get_level_reference() ])
		fileWriter.writerow(['Level Reference Offset', self.driver._get_level_reference_offset() ])
		fileWriter.writerow(['Sweep Coupling Resol. Bandwidth', self.driver._get_sweep_coupling_resolution_bandwidth() ])
		fileWriter.writerow(['Sweeping Continously', self.driver._get_acquisition_sweep_mode_continuous() ])
		fileWriter.writerow(['Sweep Coupling Sweep time', self.driver._get_sweep_coupling_sweep_time() ])
		fileWriter.writerow(['Acquisition Vertical Scale', self.driver._get_acquisition_vertical_scale()])
		fileWriter.writerow(['Sweep Coupling Video Bandwidth', self.driver._get_sweep_coupling_video_bandwidth() ])
		fileWriter.writerow(['END OF META DATA'])

		#debugprint ("ok: " + self.directory)
		return fileWriter



	"""
	This method will help send a method using ._ask()
	and then gather the data and output with the use of the file writer
	@param command string of what needs to be sent to the ._ask function
	@param fileOutputWriter this is the csv writer for the measurement you are 
		trying to make, usually something that comes from the openFile method
	"""
	def sendDataCommand(self, command, fileOutputWriter):
		data = self.driver._ask(command)
		fileOutputWriter.writerow(['%s- Command %s yielded: ' %(time.strftime("%H:%M:%S"),command), data])

	"""
	This method will use ._write() to send a message to the driver
	and will also log the command that was passed into the instrument with a time
	@param command is what you want to send to the instrument
	"""
	def commandSender(self, command):
		self.driver._write(str(command))
		self.logFileWriter.writerow(['%s- Command: %s' %(time.strftime("%H:%M:%S"),str(command))])


	"""
	This simple method should be called at the end when the instrument is not to be used any longer
	as it closes out all the files which if done incorrectly might result in unwritten files
	AND NO ONE WANTS THAT
	"""
	def closeOutputs(self):
		for writer in self.outputFiles:
			writer.close()




class DataCollector_agilentDSA91304A:
	"""init method to create the ivi driver and change the timeout interface 
	must pass in the string with the address to the instrument as well as the output
	from the creating_direc method 
	@param address is the string that is used for the ivi driver creator
	@param direc where output files will be placed 
	"""
	def __init__(self, address, direc):
		self.driver = ivi.agilent.agilentDSA91304A(address)
		self.driver._interface.timeout=30
		self.outputFiles = []
		self.directory = direc
		f = open(self.directory+".agilentDSA91304A_commandLog", 'ab')
		self.logFileWriter = csv.writer(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
		self.outputFiles.append(f)




	"""
	This method will create a new file in the directory that was passed in the
	constructor of this object.
	@param measurementToRecord is what you want to name the measurement being
		made with the instrument
	@return the return is a filewriter which you can letter send direct strings
		to or use to pass to other methods that automate the data gathering process
	""" 
	def openFile(self, measurementToRecord, channelValue):
		nameOfFile = self.directory+'agilentDSA91304A'+measurementToRecord
		file = open(nameOfFile, 'wb')
		fileWriter = csv.writer(file, quotechar ='|', quoting=csv.QUOTE_MINIMAL)
		self.outputFiles.append(file)

		#Time to list all the things to appear in the meta data header,
		#This will include the name of the .set file that will include the whole config
		self.driver._write(':disk:save:setup %s' %measurementToRecord)
		fileWriter.writerow(["NAME OF .SET FILE %s.set" %measurementToRecord])
		fileWriter.writerow(["TimeBase Range:", self.driver._ask(':TIMebase:RANGe?') ])
		fileWriter.writerow(["Channel Range:", self.driver._ask(':channel%s:range?' %channelValue)])
		fileWriter.writerow(["END OF META DATA"])
		

		return fileWriter



	"""
	This method will read in the config file for the Scope and will make the adjustments
	"""
	def setFromConfig(self):
		self.driver._write(':waveform:srate max')
		conf = open('DSAScopeConfig', 'r')#this name should be the name of the
		timeRange = conf.readline().split(' #')[0]
		self.driver._write(':timebase:range %s' %timeRange)
		conf.close()

		

	"""
	This method will make sure that the image is centered and will then take a screenshot
	and save it in the directory, with a specific name
	"""
	def captureScreenShot(self, titleOfScreenshot):
		img = self.driver._display_fetch_screenshot()
		filePic = open(titleOfScreenshot,'w')
		filePic.write(img)
		filePic.close()
		print("Screen shot captured")

	"""
	This method will set the wavelength to be as big as possible in the screen
	in the Y axis orientation

	"""
	def autoScaling(self, channelNumber, percent): 
		vPP = self.driver._ask(':measure:vpp? channel%s' %channelNumber)
		self.driver._write(':channel%s:range 5' %channelNumber) #start small window
		currentRange = long(self.driver._ask(':channel%s:"range?' %channelNumber))
		
		while(vPP/currentRange < percent) or (vPP/currentRange > .95):
			self.driver._write(':channel%s:range  %s' %(channelNumber, str((currentRange*(currentRange/vPP)))))
			vPP = int(self.driver._ask(':measure:vpp? channel%s' %channelNumber))
			newRange = int(self.driver._ask(':channel%s:range?' %channelNumber))
			if (vPP/newRange > .95):
				self.driver._write(':channel#%s:range %s' %(channelNumber, str(currentRange)))
				break;
			else:
				currentRange = newRange



	"""
	This method will help send a method using ._ask()
	and then gather the data and output with the use of the file writer
	@param command string of what needs to be sent to the ._ask function
	@param fileOutputWriter this is the csv writer for the measurement you are 
		trying to make, usually something that comes from the openFile method
	"""
	def sendDataCommand(self, command, fileOutputWriter):
		data = self.driver._ask(command)
		fileOutputWriter.writerow(['%s- Command %s yielded: ' %(time.strftime("%H:%M:%S"),command), data])

	"""
	This method will use ._write() to send a message to the driver
	and will also log the command that was passed into the instrument with a time
	@param command is what you want to send to the instrument
	"""
	def commandSender(self, command):
		self.driver._write(str(command))
		self.logFileWriter.writerow(['%s- Command: %s' %(time.strftime("%H:%M:%S"),str(command) )])


	def getTrace(self, inputChannel, nameOfFile):
		trace = self.driver._measurement_fetch_waveform(inputChannel)
		f = open(nameOfFile, 'w')
		f.write(trace)
		f.close()
	"""
	This simple method should be called at the end when the instrument is not to be used any longer
	as it closes out all the files which if done incorrectly might result in unwritten files
	AND NO ONE WANTS THAT
	"""
	def closeOutputs(self):
		for writer in self.outputFiles:
			writer.close()
