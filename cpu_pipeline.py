#!/usr/bin/env python
# coding: utf-8

# # Run ParallelFold CPU part in the SuperMicro

# set up parameters

# In[1]:


logname = 'logfile_cpu'
max_template_date = '2021-07-15'


# set up path

# In[2]:


path_input = '/home/yyang18/pipeline/parallelfold/fasta/'
path_output = '/home/yyang18/pipeline/parallelfold/out/' # same output directory of cpu and gpu part
path_data = '/data/yyang18/alphafold/AlphaFold/'
path_script = '/home/yyang18/software/ParallelFold/'
cpu_script = 'run_feature.sh'
number = 4 # the number of sequence run in the same time (cpu part)


# In[3]:


import subprocess
import os
import logging


# setp1: run cpu part

# In[4]:


files = os.listdir(path_input)


# In[6]:


# divide files into chunks for sequences run in the same time
def divide_chunks(l, n):    
    for i in range(0, len(l), n): 
        yield l[i:i + n] 
files_chunk = list(divide_chunks(files, number))


# In[ ]:


# f is file_name
# n is the index of the file
def parallelfold_cpu(f,n):
    script = './'+cpu_script+' '+             '-d'+' '+path_data+' '+             '-o'+' '+path_output+' '+             '-m'+' '+'model_1'+' '+             '-f'+' '+path_input+f+' '+             '-t'+' '+max_template_date
    if n < number-1:
        subprocess.Popen(script,shell=True,cwd=path_script,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    else:
        process = subprocess.Popen(script,shell=True,cwd=path_script,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        process.communicate()


# In[11]:


logging.basicConfig(level=logging.DEBUG, 
                        filename=logname, 
                        filemode="a",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
logger.info("parallelfold cpu part start!")
for file in files_chunk:
    for n,file in enumerate(files):
        parallelfold_cpu(file,n)
    logging.info((',').join(files)+" cpu part is done!")


# In[ ]:




