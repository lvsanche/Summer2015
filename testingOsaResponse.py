import ivi
import visa
import time
def fastTest():
	number = 1
	osa = ivi.agilent.agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR")
	while (number < 100):
		osa._write('calculate1:marker1:maximum')
		osa._write('calculate1:marker1:X?')
		osa_wavelength1 = float(osa._read())
		osa._write('calculate1:marker1:Y?')
		osa_amp1 = float(osa._read())
		osa._write('calculate1:marker1:maximum:next')
		osa._write('calculate1:marker1:X?')
		osa_wavelength2 = float(osa_read())
		osa._write('calculate1:marker1:Y?')
		osa_amp2 = float(osa._read())
		print "The number of times the loop worked: %i in fastTest" %number
		number = number +1

def sleepAllTest(timeToWait):
	number = 1
	osa = ivi.agilent.agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR")
	while (number < 100):
		osa._write('calculate1:marker1:maximum')
		time.sleep(timeToWait)
		osa._write('calculate1:marker1:X?')
		time.sleep(timeToWait)
		osa_wavelength1 = float(osa._read())
		time.sleep(timeToWait)
		osa._write('calculate1:marker1:Y?')
		time.sleep(timeToWait)
		osa_amp1 = float(osa._read())
		time.sleep(timeToWait)
		osa._write('calculate1:marker1:maximum:next')
		time.sleep(timeToWait)
		osa._write('calculate1:marker1:X?')
		time.sleep(timeToWait)
		osa_wavelength2 = float(osa_read())
		time.sleep(timeToWait)
		osa._write('calculate1:marker1:Y?')
		time.sleep(timeToWait)
		osa_amp2 = float(osa._read())
		time.sleep(timeToWait)
		print "The number of times the loop worked: %i in sleepAll" %number
		number = number + 1
def sleeAfterRead(sleepTime):
	number = 1
	osa = ivi.agilent.agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR")
	while (number < 100):
		osa._write('calculate1:marker1:maximum')
		osa._write('calculate1:marker1:X?')
		osa_wavelength1 = float(osa._read())
		time.sleep(sleepTime)
		osa._write('calculate1:marker1:Y?')
		osa_amp1 = float(osa._read())
		time.sleep(sleepTime)
		osa._write('calculate1:marker1:maximum:next')
		osa._write('calculate1:marker1:X?')
		osa_wavelength2 = float(osa_read())
		time.sleep(sleepTime)
		osa._write('calculate1:marker1:Y?')
		osa_amp2 = float(osa._read())
		time.sleep(sleepTime)
		print "The number of times the loop worked: %i in sleepAfter" %number
		number = number + 1

def sleepB4Read(sleepTime):
	number = 1
	osa = ivi.agilent.agilent86142B("TCPIP::192.168.1.201::gpib0,27::INSTR")
	while (number < 100):
		osa._write('calculate1:marker1:maximum')
		osa._write('calculate1:marker1:X?')
		time.sleep(sleepTime)
		osa_wavelength1 = float(osa._read())
		
		osa._write('calculate1:marker1:Y?')
		time.sleep(sleepTime)
		osa_amp1 = float(osa._read())
		
		osa._write('calculate1:marker1:maximum:next')
		osa._write('calculate1:marker1:X?')
		time.sleep(sleepTime)
		osa_wavelength2 = float(osa_read())
		
		osa._write('calculate1:marker1:Y?')
		time.sleep(sleepTime)
		osa_amp2 = float(osa._read())
		
		print "The number of times the loop worked: %i in sleep before" %number
		number = number + 1

def master():
	timer = 1;
	while (timer<10):
		fastTest()
		sleepAllTest(timer)
		sleeAfterRead(timer)
		sleepB4Read(timer)

master()
