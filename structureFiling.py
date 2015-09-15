import time
import os
import ivi
import csv
#data file structure for this method
#will have the following structure:
''' experiment name
	date
	time
	.csv files for all the fields 
		- will have meta data 
		- real data
		- some note files


'''
	#Method to check and or make new directories for the test that is about to happen
def creating_direc(methodName):
	#look for experimentname + date folder 
	date = time.strftime("%Y_%m_%d")
	clock = time.strftime("%H:%M:%S")
	dire = "./%s/%s/trial_%s/" %(methodName, date, clock)
	
   	d = os.path.dirname(dire)
   	if not os.path.exists(d):
   		os.makedirs(d)

   	return dire




class DataCollector_agilent8156A:
	#will produce a file called agilent8156A-META or it will be a the head of the file
	#agilent8156A-data
	def __init__(self, address, direc):
		self.driver = ivi.agilent.agilent8156A(address)
		self.driver._interface.timeout = 30
		self.outputFiles = []
		self.directory = direc
   

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
		#debugprint ("ATT+ " + self.directory)

		return fileWriter


	def sendDataCommand(self, command, fileOutputWriter):
		data = self.driver._ask(command)
		fileOutputWriter.writerow(['%s- Command %s yielded: ' %(time.strftime("%H:%M:%S"),command), data])
	
	def closeOutputs(self):
		for writer in self.outputFiles:
			writer.close()

class DataCollector_agilent86142B:
	def __init__(self, address, direc):
		self.driver = ivi.agilent.agilent86142B(address)
		self.driver._interface.timeout=30
		self.outputFiles = []
		self.directory = direc

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

	def sendDataCommand(self, command, fileOutputWriter):
		data = self.driver._ask(command)
		fileOutputWriter.writerow(['%s- Command %s yielded: ' %(time.strftime("%H:%M:%S"),command), data])

	def closeOutputs(self):
		for writer in self.outputFiles:
			writer.close()