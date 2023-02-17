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

def n_f(freqs):
    return math.fsum(freqs)

def sx_f(freqs):
    return math.fsum((x+1)*freqs[x] for x in range(len(freqs)))

def ssx_f(freqs):
    return math.fsum((x+1)*(x+1)*freqs[x] for x in range(len(freqs)))

def mean_f(freqs):
    return sx_f(freqs)/n_f(freqs)

def stdev_f(freqs):
    n = n_f(freqs)
    return math.sqrt((ssx_f(freqs)-(sx_f(freqs)**2/n))/n)

def stats_f(freqs):
    n = n_f(freqs)
    sx = sx_f(freqs)
    return n, sx/n, math.sqrt((ssx_f(freqs)-(sx*sx/n))/n)
