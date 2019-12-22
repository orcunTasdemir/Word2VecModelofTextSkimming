# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 01:29:15 2019

@author: orcuntasdemir
"""

%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np


words = []
frequency = []
for pairs in pos_freq_matrix:
    frequency.append(pairs[2])


    
#words = words[:20000]
frequency = frequency[:20000]

for freq in frequency:
    word = get_word(freq, pos_freq_matrix)
    words.append(word)

frequency.reverse()
words.reverse()

x = frequency
y = words

plt.figure()
plt.plot(x, y)
plt.title('Frequency Graph for English Words')
plt.xlabel('Frequency of Use') 
plt.ylabel('Ordered Words') 
plt.xticks
plt.xticks(np.arange(0, len(frequency), 200), rotation = 90) 
plt.yticks(np.arange(0, len(words), 200))
plt.tick_params(axis='x', which='major', labelsize=10)
plt.tick_params(axis='y', which='major', labelsize=15)
#plt.xscale('linear')
 
#plt.yscale('log')
plt.autoscale(enable=True, axis='both', tight=None)
plt.show()


























