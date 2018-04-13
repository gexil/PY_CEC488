#-*- encoding: ISO-8859-1 -*-

'''
    File name: testgpib.py
    Author: Gaston EXIL
    Date created: 22/03/2016
    Date last modified: 23/03/2016
    Python Version: 2.7
'''


import time
from cec488 import *
            

def main():
    print "test gpib"
    gpib = CEC488()
    boardpresent =  gpib.board_present()
    print "gpib board present : " + str(boardpresent)
    if(boardpresent):
        gpib.init()
        print 'Enter your commands below.\r\n"gpib adress:cmd"\r\nInsert "exit" to leave the application.'
        input=1
        finish = False
        
        while not finish :
            # get keyboard input
            input = raw_input(">> ")
                # Python 3 users
                # input = input(">> ")
            if input == 'exit':
                finish = True
            else:
                # send command
                args = input.split(':')
                adress = int(args[0])
                cmd = args[1]
                out = gpib.launch(adress, cmd)
                out = out.replace('\r\n', '')
                if out != '':
                    print ">>" + out
    
if __name__ == "__main__":
    main()




