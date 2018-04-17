import time
f = open("testing.txt", "w+")
for i in range(100):
    f.write("this is line %d\n" % i)
f.close()
