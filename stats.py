import math

def mean(list):
	sum = 0
	for i in list:
		sum += i
	return float(sum)/float(len(list))

def stdev(list):
	SSD = 0
	m = mean(list)
	for i in list:
		SSD += abs(float(i-m)*float(i-m))
	var = SSD/len(list)
	return math.sqrt(var)
