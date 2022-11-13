import matplotlib.pyplot as plt
import functools
import math

# data cleaning
headers = ["co2", "year&month", 'year', 'month']
data = []
for line in open('./data.txt').readlines():
  if not line:
    continue
  line = [ele for ele in line.strip().split(' ') if ele]
  item = {}
  for i, ele in enumerate(line):
    item[headers[i]] = ele
  data.append(item)
data = [ele for ele in data if ele.get('co2')]

# lags
lags = [i for i in range(40)]

# co2 series by month
months = [ele['month'] for ele in data]
series = [float(ele['co2']) for ele in data]

# stats
total = functools.reduce(lambda a, b:  a + b, series)
total = round(total, 2)
mean = round((total/len(series)), 2)

# ACF calculation
def get_covar(lag, series, mean, total):
  covar = 0
  for ele1, ele2 in zip(series, series[lag:]):
     covar += (ele1 - mean) * (ele2 - mean)
  covar = covar/total
  return covar
  
def get_correlation(lag, series, mean, total, covar0 = None):
  covar = get_covar(lag, series, mean, total)
  correlation = covar/covar0
  return correlation

def get_acf(series, lags, mean, total):
  covar0 = get_covar(0, series, mean, total)
  corrs = []
  for k in lags:
    corr = get_correlation(k, series, mean, total, covar0)
    corrs.append(round(corr, 2))
  return corrs

corrs = get_acf(series, lags, mean, total)

# plot acf
plt.plot(lags, corrs)
plt.xlabel('lags')
plt.ylabel('co2 concentration')
plt.savefig('./acf_scatter.png')

plt.clf()
plt.bar(lags, corrs)
plt.xlabel('lags')
plt.ylabel('co2 concentration')
plt.savefig('./acf_bar.png')

# plot monthly co2 trend
plt.clf()
plt.rcParams['xtick.labelsize'] = 5
plt.plot([ 'y' + str(i+1)+ '.m' +ele for i, ele in enumerate(months[:14])], [math.log(ele) for ele in series[:14]])
plt.xlabel('month')
plt.ylabel('co2 concentration (log scale)')
plt.savefig('./monthly_trend_scatter.png')


