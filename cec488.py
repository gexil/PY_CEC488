#-*- encoding: ISO-8859-1 -*-

'''
    File name: cec488.py
    Author: Gaston EXIL
    Date created: 22/03/2016
    Date last modified: 23/03/2016
    Python Version: 2.7
'''

from ctypes import *

class CEC488():
	__libgpib = None
	__gbo_IeeeOn = False

	""" Private methods """
	def __init__(self):
		self.__libgpib = cdll.LoadLibrary("ieee_32m.dll")

	def __ieenter(self, buffer, bufferlen, address):
		self.__libgpib.ieee488_enter.argtypes=[c_char_p, c_int, POINTER(c_int), c_int, POINTER(c_int)] 
		ln = c_int()
		status = c_int()
		result = self.__libgpib.ieee488_enter(buffer, bufferlen, byref(ln), address, byref(status))
		return result

	def __iesend(self, address, query):
		self.__libgpib.ieee488_send.argtypes=[c_int, c_char_p, c_int, POINTER(c_int)]
		status = c_int()
		result = self.__libgpib.ieee488_send(address, query, -1, status)
		return result

	def __ietrans(self, cmd):
		self.__libgpib.ieee488_transmit.argtypes=[c_char_p, c_int, POINTER(c_int)] 
		status = c_int()
		result = self.__libgpib.ieee488_transmit(cmd, -1, byref(status))
		return result

	def __ierarray(self, element, slen, rlen):
		self.__libgpib.ieee488_rarray.argtypes=[POINTER(c_ubyte), c_int, POINTER(c_int), POINTER(c_int)] 
		rlen = c_int()
		status = c_int()
		result = self.__libgpib.ieee488_rarray(element, slen, byref(rlen), byref(status))
		return result

	def __ietarray(self, element, count, eoi):
		self.__libgpib.ieee488_tarray.argtypes=[POINTER(c_ubyte), c_int, c_int, POINTER(c_int)] 
		status = c_int()
		result = self.__libgpib.eee488_tarray(element, count, eoi, byref(status))
		return result
		
	""" Public methods """

	def board_present(self):
		return bool(self.__libgpib.ieee488_board_present())

	def init(self, timeout=10000, outputEOS1=13, outputEOS2=0, intputEOS=13):
		# initialisation du peripherique gpib
		self.__libgpib.ieee488_setport(0, 5120) # 5120 = &H1400
		self.__libgpib.ieee488_initialize(21, 0)
		self.__libgpib.ieee488_dmachannel(3)
		self.__libgpib.ieee488_settimeout(timeout) #timeout
		self.__libgpib.ieee488_setoutputEOS(outputEOS1, outputEOS2)
		self.__libgpib.ieee488_setinputEOS(intputEOS)
		
	def launch(self, adress, command):
		status = self.__iesend(adress, command)
		reponse = " " * 255
		status = self.__ieenter(reponse, 255, adress)
		return reponse

	def read(self, address, status):
		ln = 0
		reponse = " " * 255
		status = self.__ieenter(reponse, 255, adress)
		return reponse

	def getArray(self, address, command, element, slen, rlen):
		status = self.__iesend(address, command)
		if not status:
			dum = "UNL UNT MLA TALK " + str(address)
			status = self.__ietrans(dum)
			if (not status):
				status = self.__ierarray(element, slen, rlen)
			status = self.__ietrans("UNL UNT")
			
		return status

	def sendArray(self, address, command, element, count):
		status = self.__iesend(address, command)
		if not status:
			dum = "UNL UNT MTA LISTEN " + str(address)
			status = self.__ietrans(dum)
			status = self.__ietarray(element, count, 1)
		status = self.__iesend("UNL UNT")

	
