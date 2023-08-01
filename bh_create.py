import re
#from mpi4py import MPI
#from bigmpi4py import MPI
import os
import subprocess
import numpy as np
import random 
import matplotlib.pyplot as plt 
from scipy import signal, interpolate, integrate
import copy
import scipy
from scipy import integrate
import sympy
import glob
import collections
from tqdm.notebook import tqdm
from scipy.optimize import curve_fit
import pickle
import seaborn as sns

h=0.701
om=0.1408*h**(-2)
rc0MMpc=2.7753*1e11*h**2
sigma80=0.811


def SMtoM(SM):
    M8=4/3 * np.pi * om * rc0MMpc * 8**3
    alpha = 0.3
    #M = M8*(SM/((sigma8(z)**2)**(-1/alpha))
    M = M8*(SM/(sigma80**2))**(-1/alpha)
    return M


def nsteps(dw,z):
    n=1.68*(1+z)/dw
    return n

def MbhthBassem(Mdm,z):
    Mbhth= ((Mdm/1e12)**1.33)*(0.86)*(10**(8+z/3))
    return Mbhth

def MbhthShimasaku(Mdm,z):
    Mbhth= ((Mdm/1e12)**1.65)*(0.1)*(10**(8+z/3))
    return Mbhth

#z is a useless variable below, z is fixed at 6
def Mbhthfit6(Mdm,z):
    a= 5.00041824
    b= 0.31992748
    Mbhth=(10**a)*(Mdm**b)
    return Mbhth

#Group of lines with different slopes and common point
#y=y1+m(x-x1)
def func(x,x1,y1,m):
    y= y1+(m*(x-x1))

def arraysum(A):
    sum = 0
    for i in range(0, len(A)):    
        sum = sum + A[i]
    return sum

def flatten(the_lists):
    result = []
    for _list in tqdm(the_lists,total=1000,desc='flattening'):
        result.extend(_list)
    return result

def flatten2(the_lists):
    result = []
    for _list in (the_lists):
        result.extend(_list)
    return result
    

#input variables from halo.py here
dirlist=[r"bh7e8full"]
Smax=22
steps=235
Mlim=2e9
samples=
mass_loss_ratio = 0.85 #0.95 for a 0.05 massloss
ratio=MbhthShimasaku(np.mean(obs6x),6)/MbhthShimasaku(np.mean(obs6x),6)
slope = 1.2
 
    
#reading observations data
#z=0
obs0xr,xerr0up,xerr0low,obs0yr,yerr0up,yerr0low=np.loadtxt("Mhratioz0",unpack='true')

#z=6
obs6xr,xerr6up,xerr6low,obs6yr,yerr6up,yerr6low=np.loadtxt("Mhratioz6",unpack='true')

obs0xr=np.delete(obs0xr,41)
xerr0up=np.delete(xerr0up,41)
xerr0low=np.delete(xerr0low,41)
obs0yr=np.delete(obs0yr,41)
yerr0up=np.delete(yerr0up,41)
yerr0low=np.delete(yerr0low,41)

obs0x=10**(obs0xr)
obs0y=10**(obs0xr+obs0yr)
obs6x=10**(obs6xr)
obs6y=10**(obs6xr+obs6yr)

lower_error0=np.zeros(len(obs0x))
upper_error0=np.zeros(len(obs0x))
left_error0=np.zeros(len(obs0x))
right_error0=np.zeros(len(obs0x))

for i in range (len (obs0x)):
    lower_error0[i] = xerr0low[i]*obs0x[i]
    upper_error0[i] = xerr0up[i]*obs0x[i]
    left_error0[i] = yerr0low[i]*obs0y[i]
    right_error0[i] = yerr0up[i]*obs0y[i]   
    
asymmetric_errorx0 = [lower_error0, upper_error0]
asymmetric_errory0 = [left_error0, right_error0]

lower_error6=np.zeros(len(obs6x))
upper_error6=np.zeros(len(obs6x))
left_error6=np.zeros(len(obs6x))
right_error6=np.zeros(len(obs6x))

for i in range (len (obs6x)):
    lower_error6[i] = xerr6low[i]*obs6x[i]
    upper_error6[i] = xerr6up[i]*obs6x[i]
    left_error6[i] = yerr6low[i]*obs6y[i]
    right_error6[i] = yerr6up[i]*obs6y[i]   
    
asymmetric_errorx6 = [lower_error6, upper_error6]
asymmetric_errory6 = [left_error6, right_error6]

import re
from pathlib import Path


def bh6mr(x,x1,y1,m):
    y= y1*((x/x1)**m)
    return y


dirlist = [Path(d) for d in dirlist] #convert directory paths to pathlib.Path objects for ease of file system manipulation

black_holes = {} #use a dictionary so we don't have to preallocate indices
z6_halo = {}
z0_halo = {}

z6_bh = {}
z0_bh = {}

for dir_path in dirlist:
    for child in tqdm(dir_path.iterdir(),position=0, leave=True, total=1000):
        m = re.match(".*?test(?P<index>\d+)$", str(child))
        
        if m: #if we match the end of the child path as a testxxx.dat file (not another directory or some other file type)
            file_index = int(m["index"])
            
            df =pd.read_pickle(m.group(0))
            mh = np.array(df['halomass'].tolist(),dtype=object)
            
            bh = copy.deepcopy(mh)
            for i in range(len(bh)):
                bh[i]=np.array(bh[i])
                for j in range (len(bh[i])):
                    if bh[i][j]>Smax:
                        bh[i][j]=0
                    else:
                        bh[i][j]=1
            
            bh6= bh6mr(SMtoM(np.array(mh[234])),np.mean(obs6x),ratio*np.mean(obs6y), slope)
            bh[234]= np.array(bh6)

            bh=np.array(bh)
            mh=np.array(mh)
            for i in range(len(bh)-1,0,-1):
                bh_sum=np.zeros(int(len(bh[i])/2))
                for j in range(int(len(bh[i])/2)):
                    if np.logical_and(bh[i][2*j]!=0,bh[i][(2*j)+1]!=0):
                        bh_sum[j]=mass_loss_ratio*(bh[i][2*j]+bh[i][(2*j)+1])
                    else:
                        bh_sum[j]=bh[i][2*j]+bh[i][(2*j)+1]
                bh[i-1][np.where(bh[i-1]==1)[0]]= bh_sum

            bh[0]=np.sum(bh[1])
            
            z0_halo[file_index] = SMtoM(mh[1][0])+SMtoM(mh[1][1])
            z6_halo[file_index] = np.array(mh[234])
            black_holes[file_index] = np.array(bh)
            z0_bh[file_index] = bh[0]
            z6_bh[file_index] = np.array(bh[234])
            

z0_halo=list(z0_halo[i] for i in range(1000))
z6_halo=list(z6_halo[i] for i in range(1000))
black_holes=list(black_holes[i] for i in range(1000))
z0_bh=list(z0_bh[i] for i in range(1000))
z6_bh=list(z6_bh[i] for i in range(1000))

# Save the black holes data:

my_df = pd.DataFrame({'z0_halo':z0_halo,'z6_halo':z6_halo,'z0_bh':z0_bh,'z6_bh':z6_bh})
my_df.to_pickle('bh7e8_0.15')