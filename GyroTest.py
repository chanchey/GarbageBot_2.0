char filename[20];
sprintf(filename, "/dev/i2c-%d",1); 
file= open(filename, O_RDWR); 
if (file&lt;0) { 
	print "unable to open I2C bus!"); 
	exit (1); 
} 
