import pylab as plt

def retire(monthly, rate, terms):
	savings = [0]
	base = [0]
	mRate = rate/12
	for i in range(terms):
		base += [i]
		savings += [savings[-1]*(1+mRate)+monthly]
	return base, savings

def displayRetireWMothlies(monthlies,rate,terms):
	plt.figure('retireMonth')
	plt.clf()
	for monthly in monthlies:
		xvals, yvals = retire(monthly, rate, terms)
		plt.plot(xvals, yvals, label = 'retire:'+str(monthly))
		plt.legend(loc = 'upper left')


def displayRetireWRates(monthly,rates,terms):
	plt.figure('retireRate')
	plt.clf()
	for rate in rates:
		xvals, yvals = retire(monthly, rate, terms)
		plt.plot(xvals, yvals, label = 'retire:'+str(monthly)+':'+\
str(int(rate*100)))
		plt.legend(loc = 'upper left')


if __name__ == "__main__":
    #base, save = retire(100,0.3,60)
    #print(f"{base=}")
    #print(f"{save=}")
    #displayRetireWMothlies([500,600,700,800,900,1000,1100],.05, 40*12)
    displayRetireWRates(800,[.03,.05,.07], 40*12)
    plt.show()