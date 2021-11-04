#!/usr/bin/env python
# coding: utf-8

# # Run ParallelFold GPU part in the Exxact

# set up parameters

# In[17]:


logname = 'logfile_gpu'
max_template_date = '2021-07-15'


# In[1]:


path_input = '/home/yyang18/pipeline/parallelfold/fasta/'
path_output = '/home/yyang18/pipeline/parallelfold/out/' # same output directory of cpu and gpu part
path_gpu_log = '/home/yyang18/pipeline/parallelfold/gpu_log/'
path_data = '/data/yyang18/alphafold/AlphaFold/'
path_script = '/home/yyang18/software/ParallelFold/'
gpu_script = 'run_alphafold.sh'
number = 4 # the number of sequence run in the same time (gpu part)


# In[19]:


import subprocess
import os
import logging


# step1: create a directory for gpu log

# In[ ]:


os.mkdir(path_gpu_log)


# setp2: run gpu part

# In[20]:


files = os.listdir(path_input)


# In[21]:


# divide files into chunks for sequences run in the same time
def divide_chunks(l, n):    
    for i in range(0, len(l), n): 
        yield l[i:i + n] 
files_chunk = list(divide_chunks(files, number))


# In[22]:


# f is file_name
# n is the index of the file
def parallelfold_gpu(f,n):
    script = './'+gpu_script+' '+                 '-d'+' '+path_data+' '+                 '-o'+' '+path_output+' '+                 '-m'+' '+'model_1,model_2,model_3,model_4,model_5'+' '+                 '-f'+' '+path_input+f+' '+                 '-t'+' '+max_template_date+' '+                 '-a'+' '+str(n)+' '+                 '-r'+' '+'True'+' '+                 '>'+' '+path_gpu_log+f.replace('.fasta','')+'_gpu.log'+' '+'2>&1'
    return script


# In[ ]:


logging.basicConfig(level=logging.DEBUG, 
                        filename=logname, 
                        filemode="a",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
logger.info("parallelfold gpu part start!")
for files in files_chunk:
    commands = []
    for n,file in enumerate(files):
        commands.append(parallelfold_gpu(file,n))
    procs = [subprocess.Popen(i,shell=True,cwd=path_script,stdout=subprocess.PIPE,stderr=subprocess.STDOUT) for i in commands]
    for p in procs:
        p.communicate()
    for file in files:
        logging.info(file+" gpu part is done!")


# In[ ]:




