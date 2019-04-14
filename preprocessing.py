#!/usr/bin/env python
# coding: utf-8

# In[6]:


'''Implement a preprocessing script (preprocess.py) that reads the original file in
the training or gold folder and produce an input file with no spaces and a label
file in the BIES format.'''


# In[41]:


import os
import re
#from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn import preprocessing


# In[48]:


def bies_tag(input_file, output_file):
    with open(input_file) as input_data, open(output_file, 'w+') as output_data:
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
            

def normalize(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:
            inside_code = 32
        elif 65281 <= inside_code <= 65374:
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring
            
            
def filter_before_tag(text):
    #remove only n
    text = normalize(text)
    rNUM = u'(-|\+)?\d+((\.|·)\d+)?%?'
    rENG = u'[A-Za-z_.]+'
    non_eng = re.sub(rENG, '', text)
    non_num = re.sub(rNUM, '', non_eng)
    s = re.sub("[\u3000\t\ax03]", '', non_num)
    return s



def filter_after_tag(text):
    s = text.replace(" ", "")
    #s = s.replace("\n", "")
    return s



def preprocess_before_tag(src, des, split_long_sentence=False):
    with open(src) as src, open(des, 'w+') as des:
        for line in src:
            sent = filter_before_tag(line)
            des.write(sent)
                # if len(''.join(sent)) > 200:
                #     print(' '.join(sent))
                
        
def preprocess_after_tag(src, des, split_long_sentence=False):
    with open(src) as src, open(des, 'w+') as des:
        for line in src:
            sent = filter_after_tag(line)
            des.write(sent)
            
            
            
def getres_from_folder(filename, folder):
    abs = os.getcwd()
    res = abs + '/../resources'
    train = res + folder
    sample_f = train + filename
    return sample_f



def encode_bies_labels(bies_file, bies_encoded_file):
    with open(bies_file) as bies, open(bies_encoded_file, 'w+') as encoded:
        #use LabelEncoder class
        token_list = []
        le = preprocessing.LabelEncoder()
        for line in bies:
            bies_line = line.split()
            for single in bies_line:
                token_list.append(single)
        le.fit(token_list)
        encoded_list = le.transform(token_list)
        for encoded_label in encoded_list:
            encoded.write(str(encoded_label))
            encoded.write("\n")


# In[49]:


def cleaning(data, folder):
    appendix = data.split(".")[0]
    labelname = appendix + "_" + "label.txt"
    
    train = getres_from_folder(data, folder)

    sample_train = getres_from_folder('temp.utf8', folder)
    L_train = getres_from_folder(labelname, folder + 'clean/')
    TRAIN = getres_from_folder(data, folder + 'clean/')
    enc_name = appendix + '_enc_label'
    encoded_bies = getres_from_folder(enc_name, folder + 'clean/')
    
    preprocess_before_tag(train, sample_train)
    bies_tag(sample_train, L_train)
    preprocess_after_tag(sample_train, TRAIN)    
    encode_bies_labels(L_train, encoded_bies)


# In[ ]:





# In[50]:


#PREPROCESSING OF TRAINING DATA

#datasets = ["as_simpl.utf8"]
datasets = ["as_simpl.utf8", "cityu_simpl.utf8", "msr.utf8", "pku.utf8"]
folders = ["/training/", "/gold/", "/testing/"]
#folders = ["/training/"]

for folder in folders:
    for data in datasets:
        cleaning(data, folder)
        
    '''for data in datasets:
    appendix = data.split("_")[0]
    labelname = appendix + "_" + "label.txt"
    
    #TRAINING DATA 
    train = getres_from_folder(data, '/training/')
    sample_train = getres_from_folder('temp.utf8', '/training/')
    L_train = getres_from_folder(labelname, '/training/clean/')
    TRAIN = getres_from_folder(data, '/training/clean/')
    enc_name = appendix + '_enc_label'
    encoded_bies = getres_from_folder(enc_name, '/training/clean/')

    preprocess_before_tag(train, sample_train)
    bies_tag(sample_train, L_train)
    preprocess_after_tag(sample_train, TRAIN)
    
    encode_bies_labels(L_train, encoded_bies)'''

#EMBEDDINGS


# In[ ]:





# In[ ]:




