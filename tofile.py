import time
f = open("testing.txt", "w+")
for i = 1:500
	f.write("this is line %d", i)
f.close()
	
