import pylab as plt
#import matplotlib.pyplot as plt

mySamples = []
myLinear = []
myQuadratic = []
myCubic = [] 
myExponential = []
for i in range(0, 30): 
    mySamples.append(i) 
    myLinear.append(i) 
    myQuadratic.append(i**2) 
    myCubic.append(i**3) 
    myExponential.append(1.5**i)

''''
plt.plot(mySamples, myLinear)
plt.plot(mySamples, myQuadratic)
plt.plot(mySamples, myCubic)
plt.plot(mySamples, myExponential)
'''

plt.figure('lin quad')
plt.clf()
plt.plot(mySamples, myLinear, 'b-', label = 'linear') 
plt.plot(mySamples, myQuadratic,'ro', label = 'quadratic') 
plt.legend(loc = 'upper left')
plt.title('Linear vs. Quadratic')
plt.figure('cube exp')
plt.clf()
plt.plot(mySamples, myCubic, 'g^', label = 'cubic') 
plt.plot(mySamples, myExponential, 'r--',label = 'exponential') 
plt.legend()
plt.title('Cubic vs. Exponential')

plt.show()