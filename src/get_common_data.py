#!/usr/bin/env python
# coding: utf-8

# In[1]:


files = ['europarl-v7.et-en.en', 'europarl-v7.fi-en.en',  'europarl-v7.hu-en.en', 'europarl-v7.fr-en.en', 'europarl-v7.de-en.en']


# In[2]:


raw_data = []
data_path = './../data/'
for file in files:
    with(open(data_path + file)) as handle:
        x = handle.read().splitlines()
    raw_data.append(x)


# In[3]:


set_et = set(raw_data[0])
set_fi = set(raw_data[1])
set_hu = set(raw_data[2])
set_fr = set(raw_data[3])
set_de = set(raw_data[4])
intersection = list(set_et.intersection(set_fi.intersection(set_hu.intersection(set_fr.intersection(set_de)))))


# In[15]:


source_sents = sorted(intersection)
source_sents = source_sents[1:]


# In[5]:


data = {}
data['fi'] = {}
data['et'] = {}
data['hu'] = {}
data['de'] = {}
data['fr'] = {}

for i in data.keys():
    data[i][i] = []
    data[i]['en'] = []
    


# In[6]:


base = 'europarl-v7.'
for i in (data.keys()):
    nbase = base + i + "-en."
    filename_eng = nbase + "en"
    filename_lang = nbase + i
    x = open(data_path + filename_lang).read().splitlines()
    y = open(data_path + filename_eng).read().splitlines()
    for j in range(len(y)):
        if(y[j] != ''):
            data[i][i].append(x[j])
            data[i]['en'].append(y[j])


# In[35]:


target_sents = {}
for i in data.keys():
    target_sents[i] = [[] for i in range(len(source_sents))]


# In[36]:


for lang in (data.keys()):
    list2 = data[lang][lang]
    list1 = data[lang]['en']
    indexes = list(range(len(list1)))
    indexes.sort(key=list1.__getitem__)
    sorted_list1 = list(map(list1.__getitem__, indexes))
    sorted_list2 = list(map(list2.__getitem__, indexes))
    count = 0
    for i in range(len(source_sents)):
        while (sorted_list1[count] != source_sents[i]):
            count+=1
        while(sorted_list1[count] == source_sents[i]):
            target_sents[lang][i].append(sorted_list2[count])
            count+=1

    for i in range(len(target_sents[lang])):
        target_sents[lang][i] = target_sents[lang][i][0]


# In[44]:


def writeToFile(file_name, file_array):
    with open(data_path + file_name,'w') as handle:
        for i in file_array:
            handle.write(i)
            handle.write("\n")


# In[45]:


writeToFile('en.txt', source_sents)
for i in target_sents.keys():
    name = i + '.txt'
    writeToFile(name, target_sents[i])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




