import sys
import time
import random as rand
import math

def burstnumber(input):
    input = input * 100
    input = math.trunc(input)
    input += 1
    return input

print("Testing")
r = rand.random()
print(r)


bursttest = 0.0856756876765
bursttest = burstnumber(bursttest)
print(bursttest, "This should be 9")
min = 0
max = 0
sum = 0
#replace l with argv[3]
#replace upperbound with argv[4]
iterations = 10000000
l = 0.001
upperbound = 3000

for i in range(iterations):
    #replace random() with drand48
    r = rand.random() #/ * uniform # dist[0.00, 1.00) -- also check out random() * /
    x = -math.log(r) / l# / lambda; / * log() is natural log * /
    # / * avoid values that are far down the "long tail" of the distribution * /
    if (x > upperbound):
        i -= 1
        continue
    if (i < 20):
        print("x is ", x)
    sum += x
    if (i == 0 or x < min):
        min = x
    if ( i == 0 or x > max ):
        max = x

    avg = sum / iterations
    print( "minimum value: ", min)
    print( "maximum value: ", max)
    print( "average value: ", avg)

