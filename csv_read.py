import pandas as pd
data = pd.read_csv("test.csv")
d1 = data["ioState"].to_numpy()
print d1
io = []
io1 = []
io = d1
n = len(io)
i = 0 
io[1]
count = 0
def flag(a,b,count):   # detects fluctuating output 
	a = int(a)
	b = int(b)
	d = count
	print a,b
	if a != b:
		d = d + 1
		print 'here'
		return d
	else :
		return d	



while i < n :
	f = io[i]
	# = int(f)
	a = str(f)
	print a[0]
	if len(a) < 7:
		#print 'here'
		io1.append(0) 
	else :
		if len(a) == 8 :
			if a[1] == '1' :
				io1.append(1) 
			else :
				io1.append(0)
		elif a[0] == '1' :
			io1.append(1) 
		else :
			io1.append(0)
	temp = io1[i]
	if i>1 :
		print count 
		count = flag(temp,io1[i-1],count)

	i = i+1 
print io1 
print "-----------------------------------------ROUGH WORK-------------------------------------"
print "COUNT is ===== %s"  %(count)


