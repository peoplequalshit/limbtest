from ROOT import *
from math import *
from array import *
import numpy as np
from scipy.optimize import fmin
import os
import sys
global Norm,gamma1,gamma2,Ebreak,normAll#hii
def Fluxcompute(A,gamma1,gamma2,Ebreak,normAll):
    os.system('gfortran SPLwHe.f frag.f -o test1.out')
    RunFlux='./test1.out %f %f %f %f %f'%(A,gamma1,gamma2,Ebreak,normAll)
    os.system(RunFlux)
def SumlogPois(dummy):
    normAll=dummy[0]
    Fluxcompute(Norm,gamma1,gamma2,Ebreak,normAll)
    print Norm,gamma1,gamma2,Ebreak,normAll
    file=open('0.dat')
    data=np.genfromtxt('0.dat')
    x,y=data[:,0],data[:,1]
    sumlogpois=0
    for i in range(len(x)):
        if TMath.Poisson(g.Eval(x[i])*(x[i]**2.75),y[i]*(x[i]**2.75))==0:
            sumlogpois+=308
        if TMath.Poisson(g.Eval(x[i])*(x[i]**2.75),y[i]*(x[i]**2.75))!=0:
            sumlogpois+=-log(TMath.Poisson(g.Eval(x[i])*(x[i]**2.75),y[i]*(x[i]**2.75)))
    collectsumlogpois=sumlogpois
    return sumlogpois
##########################
# condition
binNorm=50
bingamma=50
gamma2=0
Ebreak=0
normAll=0.00021
# start
File=TFile('present.root')
h=File.Get('E3')
g=TGraph(h)
mountain=TH2F('mountain','hill',binNorm,15000,35000,bingamma,2.5,3.1)
for i in range(binNorm):
    print i
    Norm=15000+i*(30000-15000)/binNorm
    for j in range(bingamma):
        gamma1=2.5+j*(3.1-2.5)/bingamma
        bestfit=fmin(SumlogPois,[0.00021])
#        mountain.SetBinContent(i+1,j+1,SumlogPois(bestfit))
C=TCanvas('C','C',800,600)
mountain.SetStats(0)
mountain.Draw('COLZ')
raw_input()
