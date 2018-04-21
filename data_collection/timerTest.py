#!/usr/bin/python
#This program is to see how fast our timer works 


import math
import time


startTime=time.time()
f=open("TimeTest.txt","w+")

while True: 
	programStart=time.time()
	finishtime=time.time()-programStart
	tRunTime=time.time()-startTime 
	print ("Program Run Time: %r"%(tRunTime))
	f.write("%r\r\n"%(finishtime))
