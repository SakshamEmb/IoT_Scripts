Data = "0x000000000000008c08010000013feb55ff74000f0ea850209a690000940000120000001e09010002000300040016014703f0001504c8000c0900730a00460b00501300464306d7440000b5000bb60007422e9f180000cd0386ce000107c700000000f10000601a46000001344800000bb84900000bb84a00000bb84c00000000024e0000000000000000cf00000000000000000100003fca" [2:]
#length = len(Data)
import itertools  
import collections 
head = Data[0:8]               # Data ---> AvlData <<<< gps_element and io element 
avl_len = Data[8:16] 
codec_id = Data[16:18]
Num_data = Data[18:20]
avl_len = int(avl_len,16)
avl_data = Data[20:avl_len*2+14]
timestamp = avl_data[0:16]
priority = avl_data[16:18]
gps_element = avl_data[18:48]
io_Element = avl_data[48:avl_len*2]
sl = avl_len*2+14
el = sl +2
Num_data2 = Data[sl:el]
CRC = Data[el:el+8]
##GPS_DATA
longitude = gps_element[0:8] 		#long_data = [ d,m,sec,msec,p]
#longitude = LatLongCalc(longitude)
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
io_pair_4byte = dict()
io_pair_8byte = dict()	
io_status = dict()
IO_Perm = dict()
IO_Perm = {239 : 'Ignition', 240 : 'Movement', 21:'Data Mode', 21: 'GSM Signal Strength', 200:'Sleep Mode',69:'GNSS Status',181:'PDOP',182:'PDOP',205:'Ext Voltage',42:'Speed',205:'GSM Cell ID'}
io_code = [] 
io_value = []
i=0
while(i < io_1byte*4):  
		io_code = int(io_Element[i+6:i+8],16)
		io_value = int(io_Element[i+8:i+10],16)
		io_pair_1byte[io_code]= io_value
		#print i
		#print io_code
		temp = i + 10                  #temp stores the last index of the io segment ( 1 byte 2 byte 4 byte ,8 byte )			
		i = i + 4
				
i = temp
#print "2 %s" %int(io_Element[i:i+2],16)
m = 0 	
io_2byte = int(io_Element[i:i+2],16)
#print io_Element
while(m < io_2byte*6) :  
		io_code = int(io_Element[m+i+2:m+i+4],16)
		io_value =int(io_Element[m+i+4:m+i+8],16)
		#print io_code
		#print io_value
		io_pair_2byte[io_code]= io_value
		temp2 = m+i+8
		m = m + 6
m = temp2 
io_4byte = int(io_Element[m:m+2],16)
#print io_4byte
n = 0 
while(n< io_4byte*10) :  
		io_code = int(io_Element[m+n+2:m+n+4],16)
		io_value = int(io_Element[m+n+4:m+n+12],16)
		#print io_code
		#print io_value
		io_pair_4byte[io_code]= io_value
		temp3 = n+m+12
		n = n + 10	
n = temp3 
io_8byte = int(io_Element[n:n+2],16)
#print "8byte %s" %(io_8byte)
p = 0 
while(p < io_8byte*18) :
		io_code = int(io_Element[p+n+2:p+n+4],16)
		io_value = int(io_Element[p+n+4:p+n+20],16)
		#print io_code
		#print io_value
		io_pair_8byte[io_code]= io_value
		temp4= p+n+8
		p = p + 18	
print "head ------- %s " %(head)   
print "avl_len ------%s" %(avl_len)
print "avl_data -------%s" %(avl_data)
print "timestamp -------%s" %(timestamp)
print "priority -------%s" %(priority)
print "gps_element-------%s" %(gps_element)
print "io_Element ------- %s" %(io_Element)
print"CRC-------%s" %(CRC)
print "longitude ------%s" %(longitude)
print "lattitude ------%s" %(lattitude)
print "alt------ %s" %(alt)
print "angle ------%s" %(angle)
print "speed----- %s" %(speed)
print "Satellites ------%s" %(Satellites)	
print "io_1byt----------%s" %(io_1byte)
print "io_pair_1byte -------%s" %(io_pair_1byte) 	
print "io_pair_2byte -------%s" %(io_pair_2byte)
print "io_pair_4byte -------%s" %(io_pair_4byte)
print "io_pair_8byte -------%s" %(io_pair_8byte)


def Merge(dict1, dict2,dict3,dict4): 
	dict1.update(dict2)
	dict1.update(dict4)
	dict1.update(dict3)

Merge(io_pair_1byte,io_pair_2byte,io_pair_4byte,io_pair_8byte)

io_status  = io_pair_1byte
#print "io_status------- %s" %(io_status) 
#io_status.update(IO_Perm)
#print io_status
from collections import defaultdict

dd = defaultdict(list)

for d in (io_status, IO_Perm): # you can list as many input dicts as you want here
    for key, value in d.items():
       dd[key].append(value)
io_status = dd 
print(io_status)

print "io_status------- %s" %(io_status) 
