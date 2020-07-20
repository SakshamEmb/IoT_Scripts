import pandas as pd
import sys

s1 = sys.argv
csvfile = s1.pop()
data = pd.read_csv(csvfile)
d1 = data["ioState"].to_numpy()
#print d1
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
# filter out A packets from the file ----TASK1
# filter out speed = 0 packets 
def flag(x,b,count):   # detects fluctuating output 
	x = int(x)
	b = int(b)
	d = count
	#print a,b
	if x != b:
		d = d + 1
		#print 'here'
		return d
	else :
		return d	
 	
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
	f = io[i]
	a = str(f)
	val = len(a)
	#rint val
	if val <8:	
		b = convert2byte(val)
		a = b + a	
	if int(a[1]) == 1:
		io1.append(1)
	else : io1.append(0)
	temp = io1[i]
	if i>1 :
		#print count 
		count = flag(temp,io1[i-1],count)
	if int(a[0]) == 1:
		io2.append(1)
	else : io2.append(0)
	temp2= io2[i]
	if i>1 :
		#print count1 
		count1 = flag(temp2,io2[i-1],count1)
	if io1[i]==1 & io2[i]==1 : check  = check + 1
	

	if io1[i]==0 & count3<=1000 : 
		count3 = count3 + 1 
		#print count3
	elif count3>=1000 or io2[i]==1:
		if count3>=1000:
			print("panic") 
			panic = 1 
		else: count3 = 0 	
	i = i+1 
	
print("Ignition toggled this many times ===== %d"  % count)
print("Tamper Bit toggled this many times ===== %d" % count1)
print("Check ===== %d" %check)
print("Installation Issue ==== %d" % panic)
#print "-----------------------------------------ROUGH WORK-------------------------------------"
