#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:10:33 2022
submit a batch of analyze scripts
@author: jiedeng
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--begin","-b",default=0,type=int,help="begining index, default: 0 ")
parser.add_argument("--end","-e",type=int,help="end index, default is end of file")
parser.add_argument("--interval","-i",default=30,type=int,help="interval")
parser.add_argument("--run","-r",default=True,action='store_false',help="submit?")
args   = parser.parse_args()

# import numpy as np
from subprocess import call

interval  = args.interval
beg = args.begin
end = args.end
run = True

string = """#!/bin/bash
#$ -cwd
#$ -o out.$JOB_ID
#$ -j y
#$ -pe shared 1
#$ -l h_rt=24:00:00
. "/u/local/apps/anaconda3/2020.11/etc/profile.d/conda.sh"
conda activate /u/home/j/jd848/project-lstixrud/dpkit2;
. /u/local/Modules/default/init/modules.sh
module load gcc/8.3.0;module load intel/2020.4;module load cmake

export PLUMED_KERNEL=/u/home/j/jd848/project-lstixrud/plumed/lib/libplumedKernel.so
export PATH=/u/home/j/jd848/project-lstixrud/plumed/bin:$PATH
export LD_LIBRARY_PATH=/u/home/j/jd848/project-lstixrud/plumed/lib:$LD_LIBRARY_PATH
"""

log = open('log.sub','w')
for i in range(beg,end,interval):
    file = open('sub_{0}'.format(i//interval),'w')
    file.writelines(string)
    if i+interval < end:
        endidx = i+interval
    else:
        endidx = end
    file.writelines('python ~/script/mldp/similiarity/stat.py -sh -b {0} -e {1}'.format(i,endidx))
    log.writelines('stat_{0}_{1}.sh\n'.format(i,endidx-1))
    file.close()
    if run:
        call("/u/systems/UGE8.6.4/bin/lx-amd64/qstat sub_{0}".format(i//interval),shell=True)        
log.close()
