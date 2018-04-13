#-*- encoding: ISO-8859-1 -*-

'''
    File name: testEUROPSD.py
    Author: Gaston EXIL
    Date created: 22/03/2016
    Date last modified: 23/03/2016
    Python Version: 2.7
'''

from cec488 import *
import numpy as np
import sys
import time


import matplotlib.cm as cm
import matplotlib.pyplot as plt

def genMir():
	ibuff = np.ones((128,128), dtype=np.int32)
	xcenter = 63
	ycenter = 63
	radius = 20
	LI_Length = 128 * 128
	for i in range(0, 128):
		LI_pix = 1
		for j in range(0, 128):
			test = np.power((i - xcenter), 2) + np.power((j-ycenter), 2) <= np.power(radius, 2)
			if(test):
				ibuff[i][j] = LI_pix
				LI_pix = LI_pix + 1
			else:
				ibuff[i][j] = 0
	return ibuff

def loadMirImage(gpib):
	intensite_buff = genMir()
	reponse = gpib.launch (6, "D=00")
	#Selection du set 0
	reponse = gpib.launch (6, "S=0")
	#RAZ aux adresses $00000 à $0FFFF
	reponse = gpib.launch (6, "Z0")
	
	index = 0
	LI_len = 128*128
	barLength = 50
	percent = 0
	file = open("pdata.txt", "w+")
	ok = True
	print "sum of mir image ", np.sum(intensite_buff)
	for i in range(0, 128):
		for j in range(0, 128, 2):
			com = "$" + ("%05x" % index) + "=" + ("%08x" % intensite_buff[i][j]) + "," + ("%08x" % intensite_buff[i][j + 1])
			com = com.upper()
			# On ecrit
			reponse = gpib.launch (6, com)
			index = index + 2
			log = str(i) + ", " + str(j) + ", " + com + ", " + reponse + "\r\n"
			file.write(log)
			if("OK" in reponse):
				percent = (index * 100) / LI_len
				block = int(round(barLength*percent/100))
				sys.stdout.write("\rPercent: [{0}] {1}%".format( "|"*block + " "*(barLength-block), percent))
				sys.stdout.flush()
			else:
				ok = False
				break
			if(not ok):
				break
	file.close()
	
def getImage(gpib):
	reponse = gpib.launch (6, "D=00")
	#Selection du set 0
	reponse = gpib.launch (6, "S=0")
	com = "T0," + str((128 * 128) - 1)
	NbBytes = (128 * 128) * 4
	intensite = (c_ubyte * NbBytes)()
	NbBytesRead = 0
	status = gpib.getArray(6, com, intensite, NbBytes, NbBytesRead)
	width = 128
	height = 128
	image = np.frombuffer(intensite, dtype=np.uint32)
	image.shape = (width, height)
	print "\t- sum : " + str(np.sum(intensite))
	print "\t- width : " + str(width)
	print "\t- height : " + str(height)
	print "\t- min : " + str(image.min())
	print "\t- max : " + str(image.max())
	print "\t- mean : " + str(image.mean())
	print "- display Image.."
	im = plt.imshow(image)
	plt.show()
	
if __name__ == "__main__":
	print "Test EuroPSD"
	gpib = CEC488()
	boardpresent =  gpib.board_present()
	print "gpib board present : " + str(boardpresent)
	if(boardpresent):
		gpib.init()
		loadMirImage(gpib)
		getImage(gpib)
		