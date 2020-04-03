#!/usr/bin/env python
# coding: utf-8

# In[3]:


files = ['europarl-v7.et-en.en', 'europarl-v7.fi-en.en',  'europarl-v7.hu-en.en' ]


# In[4]:


# Read the data
raw_data = []
data_path = 'nla_data'
for file in files:
    with(open(data_path + file)) as handle:
        x = handle.read().splitlines()
    raw_data.append(x)


# In[5]:


# Define the sets and find the common lines
set_et = set(raw_data[0])
set_fi = set(raw_data[1])
set_hu = set(raw_data[2])
intersection = set_et.intersection(set_fi.intersection(set_hu))



# In[12]:


line_indices_et = []
line_indices_fi = []
line_indices_hu = []
count = 0
total_count = len(intersection)
for line in intersection:
    if (count % 1000 == 0):
        print(count/total_count * 100)
    x1 = [i for (i,j) in enumerate(raw_data[0]) if j == line]
    x2 = [i for (i,j) in enumerate(raw_data[1]) if j == line]
    x3 = [i for (i,j) in enumerate(raw_data[2]) if j == line]
    line_indices_et = line_indices_et + x1
    line_indices_fi = line_indices_fi + x2
    line_indices_hu = line_indices_hu + x3
    count += 1
    
    


# In[15]:


import pickle
with open('et_line_indices.pickle','wb') as handle:
    pickle.dump( line_indices_et, handle)
with open('fi_line_indices.pickle','wb') as handle:
    pickle.dump( line_indices_fi, handle)
with open('hu_line_indices.pickle','wb') as handle:
    pickle.dump( line_indices_hu, handle)


# In[11]:


import pickle
with open('et_line_indices.pickle','rb') as handle:
    et_li = pickle.load(handle)
with open('hu_line_indices.pickle','rb') as handle:
    hu_li = pickle.load(handle)
with open('fi_line_indices.pickle','rb') as handle:
    fi_li = pickle.load(handle)


# In[ ]:


fi_en = open('nla_data/europarl-v7.fi-en.en').read().splitlines()
fi_fi = open('nla_data/europarl-v7.fi-en.fi').read().splitlines()
fi_eng_sents = []
fi_fin_sents = []
for i in fi_li:
    if(fi_en[i]):
        fi_eng_sents.append(fi_en[i])
        fi_fin_sents.append(fi_fi[i])    


# In[ ]:


et_en = open('nla_data/europarl-v7.et-en.en').read().splitlines()
et_et = open('nla_data/europarl-v7.et-en.et').read().splitlines()
et_eng_sents = []
et_et_sents = []
for i in et_li:
    if(et_en[i]):
        et_eng_sents.append(et_en[i])
        et_et_sents.append(et_et[i])    


# In[ ]:


hu_en = open('nla_data/europarl-v7.hu-en.en').read().splitlines()
hu_hu = open('nla_data/europarl-v7.hu-en.hu').read().splitlines()
hu_eng_sents = []
hu_hun_sents = []
for i in hu_li:
    if(hu_en[i]):
        hu_eng_sents.append(hu_en[i])
        hu_hun_sents.append(hu_hu[i])    


# In[ ]:


source_sents = list(set(fi_eng_sents))
source_sents = sorted(source_sents)


# In[ ]:


target_sents = {}
target_sents['fi'] = [[] for i in range(len(source_sents))]
target_sents['hu'] = [[] for i in range(len(source_sents))]
target_sents['et'] = [[] for i in range(len(source_sents))]


# In[ ]:


list1 = et_eng_sents
list2 = et_et_sents


indexes = list(range(len(list1)))
indexes.sort(key=list1.__getitem__)
sorted_list1 = list(map(list1.__getitem__, indexes))
sorted_list2 = list(map(list2.__getitem__, indexes))
count = 0
for i in range(len(source_sents)):
    try:
        while(sorted_list1[count] == source_sents[i]):
            target_sents['et'][i].append(sorted_list2[count])
            count+=1
    except:
        print(i)
    
    
for i in range(len(target_sents['et'])):
    target_sents['et'][i] = target_sents['et'][i][0]
    


# In[ ]:


list1 = fi_eng_sents
list2 = fi_fin_sents


indexes = list(range(len(list1)))
indexes.sort(key=list1.__getitem__)
sorted_list1 = list(map(list1.__getitem__, indexes))
sorted_list2 = list(map(list2.__getitem__, indexes))
count = 0
for i in range(len(source_sents)):
    try:
        while(sorted_list1[count] == source_sents[i]):
            target_sents['fi'][i].append(sorted_list2[count])
            count+=1
    except:
        print(i)
    
    
for i in range(len(target_sents['fi'])):
    target_sents['fi'][i] = target_sents['ft'][i][0]


# In[ ]:


list1 = hu_eng_sents
list2 = hu_hun_sents


indexes = list(range(len(list1)))
indexes.sort(key=list1.__getitem__)
sorted_list1 = list(map(list1.__getitem__, indexes))
sorted_list2 = list(map(list2.__getitem__, indexes))
count = 0
for i in range(len(source_sents)):
    try:
        while(sorted_list1[count] == source_sents[i]):
            target_sents['hu'][i].append(sorted_list2[count])
            count+=1
    except:
        print(i)
    
    
for i in range(len(target_sents['hu'])):
    target_sents['hu'][i] = target_sents['hu'][i][0]


# In[ ]:


with open('source.txt','w') as handle:
    for i in source_sents:
        handle.write(i)
        handle.write("\n")


# In[ ]:


with open('fi.txt','w') as handle:
    for i in target_sents['fi']:
        handle.write(i)
        handle.write("\n")


# In[ ]:


with open('et.txt','w') as handle:
    for i in target_sents['et']:
        handle.write(i)
        handle.write("\n")


# In[ ]:


with open('hu.txt','w') as handle:
    for i in target_sents['hu']:
        handle.write(i)
        handle.write("\n")

