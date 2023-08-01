import tkinter as tk
import os
import tkinter
import tkinter.messagebox
import customtkinter
import customtkinter as ctk
from RangeSlider.RangeSlider import RangeSliderH 
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
import threading
import time
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar

from CTkRangeSlider import *

import panel as pn
import math

import pandas as pd
import numpy as np
import scipy
from scipy import integrate
import pickle
import random
from tqdm.tk import tqdm
from time import sleep

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue

h=0.701
om=0.1408*h**(-2)
rc0MMpc=2.7753*1e11*h**2
sigma80=0.811

z0=0
zf=6
samples=1000
steps=10
Mlim=2e8
Mmin=12.097777777777777
Mmax=14.0



def sigma8(z):
    return mt.sigma80*(1+z)**(-1)

#make the function which calculates the mass variance S(M) 
# assign M[Msolar] ,z(redshift)[nondim]
def varipsapp(M):
    M8=4/3 * np.pi * om * rc0MMpc * 8**3
    #alpha=(cn.ns+3)/3
    alpha = 0.3
    SM=sigma80**2*((M/M8)**(-alpha))
    return SM

def varipsapproximate(M):
    M8=4/3 * np.pi * om * rc0MMpc * 8**3
    #alpha=(cn.ns+3)/3
    alpha = 0.3
    SM=sigma80**2*((M/M8)**(-alpha))
    return SM

def varipsapproximatediffM(M):
    M8=4/3 * np.pi * om * rc0MMpc * 8**3
    #alpha=(cn.ns+3)/3
    alpha = 0.3
    #SM=sigma8(z)**2*((M/M8)**(-alpha))
    SM=sigma80**2*((M/M8)**(-alpha))
    diffdSdM=0.3/M * SM
    return abs(diffdSdM)

def SMtoM(SM):
    M8=4/3 * np.pi * om * rc0MMpc * 8**3
    alpha = 0.3
    #M = M8*(SM/((sigma8(z)**2)**(-1/alpha))
    M = M8*(SM/(sigma80**2))**(-1/alpha)
    return M

#make the function which calculate the f_{FU}.
# z0:parent halo redshift M0: parent halo mass
# z1:progenitor halo redshift M1:main progenitor halo mass
def ffu(z0,z1,M0,M1):
    deltac=1.686
    #introduce the mass variance square
    vari0=varipsapproximate(M0)
    vari1=varipsapproximate(M1)
    # calculate ffu
    coefficientterm=deltac*(z1-z0)/(np.sqrt(2*np.pi)*(abs(vari1-vari0))**(1.5))
    expterm=np.exp(-(deltac*(z1-z0))**2/(2*(vari1-vari0)))
    ffuterm=coefficientterm*expterm
    #print(coefficientterm,expterm)
    return ffuterm

def ffu1(dw,deltaS):
    coefficientterm1 = (dw)/((np.sqrt(2*np.pi))*((deltaS)**1.5))
    expterm1 = np.exp(-((dw)**2)/(2*(deltaS)))
    ffuterm1 = coefficientterm1 * expterm1
    return ffuterm1

#Under the t=t_0 and M=M_0, the probability on M=M_1.
#make the function which calculate the dP/dM_1.
def dpdm1(z0,z1,M0,M1):
    diffdSdM=varipsapproximatediffM(M1)
    dpdm1=ffu(z0,z1,M0,M1) * diffdSdM
    #print(ffu(z0,z1,M0,M1),diffdSdM)
    return dpdm1

def dpdm2(dw,deltaS):
    return ffu1(dw,deltaS)*deltaS

def PSMF(M,w):
    rho= 0.3 * 2.78 * (10**11)
    S = varipsapp(M)
    psmf = (rho/M)*(w/(((2*np.pi)**(1/2))*(S**(3/2))))*np.exp(-(w**2)/(2*S))*varipsapproximatediffM(M) * M
    return psmf

def Srem(deltaS,S0,w):
    deltac=1.686
    z = (w/deltac)
    alpha=0.3
    Mrem = -((((deltaS/S0)+1)**(-1/alpha))-1)*SMtoM(S0)
    Srem=varipsapproximate(Mrem)
    return Srem

def nsteps(dw,z):
    n=1.68*(1+z)/dw
    return n

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

def EPSrandommass(S0,dw,binnumber):
    alpha = 0.3
    deltaS = np.logspace(-10,np.log10((0.231)*S0)) #0.231*S0 refers to deltaS that gives M/2
    dpdm = ffu1(dw,deltaS)*deltaS
    SMg=random.choices(deltaS, weights=dpdm)
    return SMg

def wx(z):
    deltac= 1.68
    w = deltac * (1+z)
    return w

def halo_samples(Mmin, Mmax, z0,samples):
    n = samples
    M = np.logspace(Mmin,Mmax,int(samples))
    w = wx(z0)
    dpdm = PSMF(M,w)
    SMg=random.choices(M, weights=dpdm, k=n)
    return SMg

def outputS(n,dw,Smax,Sinitial):
    wstart = 0
    S=[[]]*n
    Sprior=np.array([Sinitial])

    for ii in range(1,n):
        # set the w correspond to next step
        w = wstart + ii*dw
        # prior S put the Sprior (Sprior means S[i-1])
        # make the new array to put the generated S at the next step
        S[ii]=np.zeros((len(Sprior)*2))
        # generate the S at the next step (all halo label)
        #print("starting the timestep:%d ,w=%.3f"%(ii,w))
        for j in range(0,len(Sprior)*2):
        # odd and even case
            if(j% 2 ==0):
                deltaS=EPSrandommass(Sprior[round(j/2)],dw,1000)[0]
                S[ii][j]=Sprior[round(j/2)]+deltaS
            else:
                S[ii][j]=Srem(deltaS,Sprior[round((j-1)/2)],w)
        # if the condition, S>Smax, is satisfied, this element is excluded.
        
        Sprior=np.delete(S[ii],np.where(S[ii]>Smax))
    return S


def halo_create(z0,zf,samples,steps,Mlim, Mmin, Mmax):
    n = samples
    iter_step = 100/n
    progress_step = iter_step
    
    Smax=varipsapp(Mlim)
    halo_sample=halo_samples(Mmin, Mmax, z0,samples)
    dw=1.68*(1+(zf-z0))/steps

    for i in tqdm(range(samples), desc='Creating Halos'):
        filenum=i
        #progress_var.set(i)
        result = outputS(steps,dw,Smax,varipsapp(halo_sample[i]))
        result=np.array(result,dtype=object)
        data=np.transpose(result)
        my_df = pd.DataFrame(data, columns=['halomass'])
        my_df.to_pickle("halos/test{:03d}".format(filenum))
        time.sleep(0.02)

 
halo_create(float(z0),float(zf),int(samples),int(steps),float(Mlim),float(Mmin),float(Mmax))    
    
