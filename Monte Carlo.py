#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf


# In[2]:


ticker = 'PG'
data = yf.download(ticker)


# In[3]:


# daily average return for 100 days
# NOT A PERCENT

av_return = 0

opens = data.tail(500)['Open']
closes = data.tail(500)['Close']

for i in range(100):
    av_return+=(closes[i]/opens[i]-1)

av_return/=100

print(av_return)


# In[4]:


import math


# In[5]:


price_relatives = []

prices = data.tail(500)['Close']
for i in range(1, 500):
    price_relatives.append(math.log(prices[i]/prices[i-1]))


# In[6]:


import statistics


# In[7]:


std_dev = statistics.stdev(price_relatives)

print(std_dev)


# In[8]:


from scipy.stats import norm
import random


# In[9]:


def prod_array(av_return, std_dev, period):
    
    days = []
    cumulative = []

    for i in range(period):
        ret = norm.ppf(random.random(), loc=av_return, scale=std_dev)
        days.append(ret)
        if i == 0:
            cumulative.append(ret)
        else:
            cumulative.append(((ret+1)*(cumulative[i-1]+1))-1)

    return cumulative


# In[10]:


#100 day final
final = []
all_paths = []

for i in range(100):
    gen = prod_array(av_return, std_dev, 100)
    all_paths.append(gen)
    final.append(gen[-1]*100)
    
print(final)


# In[11]:


import matplotlib.pyplot as plt


# In[12]:


plt.hist(final)


# In[13]:


x = [i for i in range(1, 101)]
plt.scatter(x, final)


# In[14]:


import plotly.graph_objects as go


# In[15]:


fig = go.Figure()

for path in all_paths:
    fig.add_trace(go.Scatter(x=list(range(len(path))), y=path, mode='lines'))

fig.update_layout(
    title="Cumulative Percent Increase vs. Time",
    xaxis_title="Days",
    yaxis_title="Cumulative Percent Increase"
)

fig.show()

