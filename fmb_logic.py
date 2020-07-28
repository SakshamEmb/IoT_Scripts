import pandas as pd
import sys
a=1
s1 = sys.argv
csvfile = s1.pop()
data = pd.read_csv(csvfile)
# filter out A packets from the file ----TASK1
filtered = data[data['locationReliable']==True]
d1 = filtered["ioState"].to_numpy()
speed = filtered["speed"].to_numpy()
battery1 = filtered[filtered['speed']==0] # speed = 0 
battery2 = filtered[filtered['speed']!=0]
battery1 = battery1["vehicleBatteryLevel"].to_numpy()
battery2 = battery2["vehicleBatteryLevel"].to_numpy()
io_s = filtered[filtered['speed']!=0]
io_s = io_s["ioState"].to_numpy()
io = []
io1 = []
io2 = []
io3 = []
io4 = []
io = d1
n = len(io)
i = 0 
count = 0
count1 = 0 
count3 = 0 
panic = 0
check =0  
y = 0 
num = 10
#for result in data.LocationReliable:
#	if re.search('TRUE',result):
# filter out speed = 0 packets 
battcheck = 0
error = 0  
cnt = 0  # battery voltage over 13.2 count
previous_v = 0 
mcb = 0 
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
			battcheck = batterycheck(ix,battery1)
		return d
	else :
		return d
def toggle_0_1(xp,xn,zp,zn):
	xp = int(xp)
	xp = int(xn)
	zp = int(zp)
	zn= int(zn)

	if xp == 0  and xn == 1 and yn == 1 and yp == 0 and mcb == 0 :
		mcb = 1 

def battcnt(voltage,i):
	volt = voltage[i]
	if volt>13.2:
		cnt=cnt+1
		return 1 
	else :
		return 0	
def batterycheck(index,battery1):
	i1 = index
	batt = battery1
	if batt[i1]>=24.5 & batt[i1]<=26 :# check for trucksr
		return 1  
	elif batt[i1]>=12.5 & batt[i1]<=13:
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

while i < n :
	ind = i
	i1 = i
	if i>len(battery2)-1:
		ind = len(battery2)-1
	if i1>len(io_s)-1:
		i1 = len(io_s) -1 
	#if i>len(battery1)-1:
	#	ind = len(battery1)-1
	f = io[i] # All A packets 
	a = str(f)
	val = len(a)

	if val <8:	
		b = convert2byte(val)
		a = b + a	

	g = io_s[i1]  # A packets with speed >0
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
		battbit = battcnt(battery2,ind)
		if i>num:
			if x-y > 4 and error == 0:
				print(" x-y == %s" %(x-y))
				print(" Loose Connection with battery")
				error = 1  
			elif error == 0:
				#CHECK BATTERY VOLTAGE 
				if battcheck == 1 :
					print(" Mark threshold voltage change required to 25.2 V")
					error = 1
				elif battcheck == 2 :
					print(" Mark threshold voltage change required to 13.2 V")
					error = 1
				elif battcheck==0:
				#CHECK VEHICLE BATTERY MISBEHAVIOUR	
					if battbit == 1 and cnt-previous_v>5: 
							sensor = input("Is sensor connected ? ")
							if sensor == "yes":
								print("Mark sensor connected ")
							else :
								if mcb == 1 :
									print("Mark Ignition Wire Connected")
								else :
									print (" Ignition Wire to be Connected")	
					else :
						print(" TO MANUAL CHECK ")
						error = 1 	
			previous_v = cnt			
			y = x
			num = num + 10  

	if io1[i]==0 & count3<=1000 : 
		count3 = count3 + 1 
		#print count3
	elif count3>=1000 or io2[i]==1:
		if count3>=1000:
			#print("panic") 
			panic = 1 
		else: count3 = 0 	
	i = i+1 	

#LOGIC
	
print("Ignition toggled this many times ===== %d"  % count)
print("Tamper Bit toggled this many times ===== %d" % count1)
print("Check ===== %d" %check)
print("Installation Issue ==== %d" % panic)
#print "-----------------------------------------ROUGH WORK-------------------------------------"
