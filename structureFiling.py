import time
import os
import shelve
#data file structure for this method
#will have the following structure:
''' date_experimentName
	|
	trialnumber(maybe time based)
	|
	config.txt, some notes on the experiment
	and metadata
	|
	############## this becomes a unique to this situation structure
	PortNumber
	|
	OSA data file
	Packetloss data file
	bit error occurance data
	bit error location data
	extra trace and noted files 


'''
	#Method to check and or make new directories for the test that is about to happen
def creating_direc(methodName):
	#look for experimentname + date folder 
	date = time.strftime("%m%d%Y")
	clock = time.strftime("%H%M%S")
	dire = "./SummerExperiments/%s_%s/trial_%s/trial%s_shelve" %(date, methodName, clock, clock)
	
   	d = os.path.dirname(dire)
   	if not os.path.exists(d):
   		os.makedirs(d)

   	shelv = shelve.open(dire)
   	shelv.close()
   	return dire
