# first of all import the socket library 
import socket			 

# next create a socket object 
s = socket.socket()		 
print "Socket successfully created"

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 20050			

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('', port))		 
print "socket binded to %s" %(port) 

# put the socket into listening mode 
s.listen(5)	 
print "socket is listening"			

# a forever loop until we interrupt it or 
# an error occurs 
def LatLongCalc(D):
	d = int( D[0:2],16)
	m = int(D[2:4],16)
	sec = int(D[4:6],16)
	msec = int(D[6:8],16)
	p = 100000 #precision'
	matrix = [d,m,sec,msec]
	print matrix
	result  = float(d + float(m/60) + float(sec/3600) + float(msec/3600000))*1
	return result 
#IO_Perm = dict()
IO_Perm = {'Ignition' : '239', 'Movement' : '240', 'Data Mode':'80', 'GSM Signal Strength' : '21', 'Sleep Mode':'200','GNSS Status':'69','PDOP':'181','DOP':'182','Ext Voltage24':'205','Speed':'24','GSM Cell ID':'205','GSM Area Code':'206'}

while True: 
# Establish connection with client. 
	c, addr = s.accept()	 
	print 'Got connection from', addr 
# send a thank you message to the client. 
	c.send('Send Data') 
	Data = c.recv(1024) 
	print Data
	length = len(Data)
	head = Data[0:8]               # Data ---> AvlData <<<< gps_element and io element 
	avl_len = Data[8:16] 
	codec_id = Data[16:18]
	Num_data = Data[18:20]
	avl_len = int(avl_len,16)
	avl_data = Data[20:avl_len+20]
	timestamp = avl_data[0:16]
	priority = avl_data[16:18]
	gps_element = avl_data[18:48]
	io_Element = avl_data[48:avl_len]
	##GPS_DATA
	longitude = gps_element[0:8] 		#long_data = [ d,m,sec,msec,p]
	longitude = LatLongCalc(longitude)
	lattitude = gps_element[8:16]
	alt = gps_element[16:20]
	angle = gps_element[20:24]
	Satellites = int(gps_element[24:26],16)	
	speed = gps_element[26:30]
	#IO_DATA
	io_event = io_Element[0:2]
	io_num = int(io_Element[2:4],16)
	io_1byte = int(io_Element[4:6],16)  #number 1byte io data
	io_pair_1byte = dict()
	io_pair_2byte = dict()
	io_code = [] 
	io_value = []
	i=0
	while(i < io_1byte*4):  
			io_code = int(io_Element[i+6:i+8],16)
			io_value = int(io_Element[i+8:i+10],16)
			io_pair_1byte[io_code]= io_value
			print i
			print io_code
			temp = i + 10			
			i = i + 4
					
	i = temp
	print "2 %s" %int(io_Element[i:i+2],16)
	m = 0 	
	io_2byte = int(io_Element[i:i+2],16)
	print io_Element
	while(m <=io_2byte*6-2) :  
			io_code = io_Element[m+i+2:m+i+4]
			io_value = io_Element[m+i+4:m+i+8]
			io_pair_2byte[io_code]= io_value
			m = m + 8		
	print "head ------- %s " %(head)   
	print "avl_len ------%s" %(avl_len)
	print "avl_data -------%s" %(avl_data)
	print "timestamp -------%s" %(timestamp)
	print "priority -------%s" %(priority)
	print "gps_element-------%s" %(gps_element)
	print "longitude ------%s" %(longitude)
	print "lattitude ------%s" %(lattitude)
	print "alt------ %s" %(alt)
	print "angle ------%s" %(angle)
	print "speed----- %s" %(speed)
	print "Satellites ------%s" %(Satellites)	
	print "io_1byt----------%s" %(io_1byte)
	print "io_pair_1byte -------%s" %(io_pair_1byte) 	
	print "io_pair_2byte -------%s" %(io_pair_2byte)

# Close the connection with the client 
	c.close()

print Data[100]

