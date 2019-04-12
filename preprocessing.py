#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''Implement a preprocessing script (preprocess.py) that reads the original file in
the training or gold folder and produce an input file with no spaces and a label
file in the BIES format.'''


# In[26]:


import os
import re


# In[42]:


#preprocess(a)
#b = filter_characters(a)
#print(b)

def bmes_tag(input_file, output_file):
    with open(input_file) as input_data, open(output_file, 'w') as output_data:
        for line in input_data:
            word_list = line.strip().split()
            for word in word_list:
                if len(word) == 1 or (len(word) > 2 and word[0] == '<' and word[-1] == '>'):
                    output_data.write("S")
                else:
                    output_data.write("B")
                    for w in word[1:len(word) - 1]:
                        output_data.write("I")
                    output_data.write("E")
            output_data.write("\n")
            

def filter_before_tag(text):
    #remove only n
    rNUM = u'(-|\+)?\d+((\.|·)\d+)?%?'
    rENG = u'[A-Za-z_.]+'
    non_eng = re.sub(rENG, '', text)
    non_num = re.sub(rNUM, '', non_eng)
    s = re.sub("[\u3000\t\ax03]", '', non_num)
    print(s)
    return s

def filter_after_tag(text):
    s = text.replace(" ", "")
    s = s.replace("\n", "")
    return s

def preprocess_before_tag(src, des, split_long_sentence=False):
    #preprocess before tag
    with open(src) as src, open(des, 'w') as des:
        for line in src:
            sent = filter_before_tag(line)
            des.write(sent)
                # if len(''.join(sent)) > 200:
                #     print(' '.join(sent))
        
def preprocess_after_tag(src, des, split_long_sentence=False):
    with open(src) as src, open(des, 'w') as des:
        for line in src:
            sent = filter_after_tag(line)
            des.write(sent)
            
            
def getfile(filename):
    abs = os.getcwd()
    res = abs + '/resources'
    train = res + '/training/'
    sample_f = train + filename
    return sample_f


chinese_sample = getfile('sample_icwb2.utf8')
file_ch = open(chinese_sample)
            
out = getfile('output.txt')
sample_f = getfile('sample.txt')
filtered_f = getfile('filtered.txt')

preprocess_before_tag(chinese_sample, sample_f)
bmes_tag(sample_f, out)
preprocess_after_tag(out, filtered_f)

#preprocess_file(chinese_sample, sample_f)


# In[ ]:




