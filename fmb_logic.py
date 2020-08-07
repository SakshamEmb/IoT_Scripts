import pandas as pd
import sys
import logging 

CmdArgument = sys.argv
csvFile = CmdArgument.pop()
data = pd.read_csv(csvFile)
# filter out A packets from the file ----TASK1
filtered = data[data['locationReliable']==True]
io = filtered["ioState"].to_numpy()
speed = filtered["speed"].to_numpy()
battery1 = filtered[filtered['speed']==0] # speed = 0 
battery2 = filtered[filtered['speed']!=0] # speed > 0 
battery1 = battery1["vehicleBatteryLevel"].to_numpy()
battery2 = battery2["vehicleBatteryLevel"].to_numpy()
timestamp = filtered["gpsTime"].to_numpy()
ioSpeed0 = filtered[filtered['speed']!=0]
ioSpeed0 = ioSpeed0["ioState"].to_numpy()
io1 = []
io2 = []
io3 = []
io4 = []
n = len(io)
i = 0 
count = 0
count1 = 0 
count2 = 0 
count3 = 0  #battery voltage over 13.2 count
panic = 0
check =0  
y = 0 
num = 10 
batch = 10 
#for result in data.LocationReliable:
#	if re.search('TRUE',result):
# filter out speed = 0 packets 
batteryCheck = 0
error = 0  
previousV = 0 
wireFlag = 0 

def flag(x,b,count,index):   # detects fluctuating output # present value , previous value
	x = int(x)
	b = int(b)
	d = count
	ix = index
	#print a,b
	if x != b:
		d = d + 1
		#print 'here'
		if x==1 & b==0:
			batteryCheck = batteryFunction(ix,battery1)
		return d
	else :
		return d
def toggle_0_1(xp,xn,zp,zn):
	xp = int(xp)
	xp = int(xn)
	zp = int(zp)
	zn= int(zn)
	global wireFlag

	if xp == 0  and xn == 1 and yn == 1 and yp == 0 and mcb == 0 :
		wireFlag = 1 

def batteryCount(voltage,i):
	volt = voltage[i]
	global count3
	if volt<13.2:
		count3=count3+1
		return 1 
	else :
		return 0	
def batteryFunction(index,battery):
	if battery[index]>=24.5 & battery[index]<=26 :# check for trucksr
		return 1  
	elif battery[index]>=12.5 & battery[index]<=13:
		return 2 
	else :
		return 0  
		 			
def convert2byte(argument):
	switcher = {
		1: '0000000',
		2: '000000',
		3: '00000',
		4: '0000',
		5: '000',
		6: '00',
		7: '0'							
	}
	return switcher.get(argument)

sensor = input("Is sensor connected ? ")
# How many sets do you want to check ?
while i < n :
	ind = i
	i1 = i
	# avoid index error
	if i>len(battery2)-1:
		ind = len(battery2)-1
	if i1>len(ioSpeed0)-1:
		i1 = len(ioSpeed0) -1

	f = io[i] # All A packets 
	a = str(f)
	val = len(a)

	if val <8:	
		b = convert2byte(val)
		a = b + a	

	g = ioSpeed0[i1]  # A packets with speed >0
	a1 =str(g)
	val1 = len(a1)
	if val1 <8:	
		b1 = convert2byte(val1)
		a1 = b1 + a1	

	if int(a[1]) == 1:
		io1.append(1)
	else : io1.append(0)
	temp = io1[i]

	if int(a[0]) == 1:
		io2.append(1)
	else : io2.append(0)
	temp2= io2[i]

	if int(a1[2]) == 1 :
		io3.append(1)
	else : io3.append(0)
	temp3 = io3[i1]

	if int(a1[1])==1:
		io4.append(1)
	else : io4.append(0)	
	temp4 = io4[i1]

	if i>1 :
		#print count1
		#print(battery2)

		count = flag(temp,io1[i-1],count,i)
		count1 = flag(temp2,io2[i-1],count1,i)
		x = count1
		toggle_0_1(io3[i-1],temp3,io4[i-1],temp4)

		#print(" x === %s" %(x)) 
		batteryFlag = batteryCount(battery2,ind)

		if i>num: # Time Stamp needed , availability , ioState`
			if x-y > 4 and error == 0:
				print(" x-y == %s" %(x-y))
				print(" Loose Connection with battery")
				#logging.basicConfig(format='%s %(message)s' %(timestamp[i]) )
				print(timestamp[i])
				logging.warning('   %s -------- Speed is %d  -------- batch number is %d ' %(timestamp[i],speed[i],num/10))
				error = 0
			elif error == 0:
				#CHECK BATTERY VOLTAGE 
				if batteryCheck == 1 :
					print(" Mark threshold voltage change required to 25.2 V")
					error = 1
				elif batteryCheck == 2 :
					print(" Mark threshold voltage change required to 13.2 V")
					error = 1
				elif batteryCheck==0:
				#CHECK VEHICLE BATTERY MISBEHAVIOUR	
					if batteryFlag == 1 and count3-previousV>5: 
							if sensor == "yes":
								print("Mark sensor connected ")
							else :
								if wireFlag == 1 :
									print("Mark Ignition Wire Connected")
								else :
									print (" Ignition Wire to be Connected")	
					else :
						print(" TO MANUAL CHECK ")
						
			previousV = count3						
			y = x
			num = num + batch  

	if io1[i]==0 & count2<=1000 : 
		count2 = count2 + 1 
		#print count2
	elif count2>=1000 or io2[i]==1:
		if count2>=1000:
			#print("panic") 
			panic = 1 
		else: count2 = 0 	
	i = i+1 	

#LOGIC
size = len(filtered)
size1 = len(data)
print(" Number of A packets ====> %s " %size)
print(" Total Number of packets ====> %s" %size1)
print("Ignition toggled this many times ===== %d"  % count)
print("Tamper Bit toggled this many times ===== %d" % count1)
#print("Check ===== %d" %check)
#print("Installation Issue ==== %d" % panic)
#print "-----------------------------------------ROUGH WORK-------------------------------------"
