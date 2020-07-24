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
io = []
io1 = []
io2 = []
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
	if i>len(battery2)-1:
		ind = len(battery2)-1
	#if i>len(battery1)-1:
	#	ind = len(battery1)-1
	f = io[i]
	a = str(f)
	val = len(a)
	#print(val)
	if val <8:	
		b = convert2byte(val)
		a = b + a	

	if int(a[1]) == 1:
		io1.append(1)
	else : io1.append(0)
	temp = io1[i]
	if i>1 :
		#print count 
		count = flag(temp,io1[i-1],count,i)


	if int(a[0]) == 1:
		io2.append(1)
	else : io2.append(0)
	temp2= io2[i]

	
	
	if i>1 :
		#print count1
		#print(battery2)
		count1 = flag(temp2,io2[i-1],count1,i)
		x = count1
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
