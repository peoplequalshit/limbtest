from ROOT import *
from math import *
from array import *
import numpy as np
import pyfits
import os
import sys

def Fluxcompute(A,gamma1,gamma2,Ebreak,normAll):
    os.system('gfortran BPLwHe.f frag.f -o test1.out') #use SPLwHe
    RunFlux='./test1.out %f %f %f %f %f'%(A,gamma1,gamma2,Ebreak,normAll)
    os.system(RunFlux)
def SumlogPois(dummy):
    A=dummy[0]
    gamma1=dummy[1]
    gamma2=dummy[2]
    Ebreak=dummy[3]
    normAll=dummy[4]
    print A,gamma1,gamma2,Ebreak,normAll
    Fluxcompute(A,gamma1,gamma2,Ebreak,normAll)
    file=open('0.dat')
    data = np.genfromtxt('0.dat')
    x,y=data[:,0],data[:,1]
    #Start stat. program
    sumlogpois=0
    for i in range(len(x)):
        measurement=g.Eval(x[i],0,'S')
        model=y[i]*(x[i]**2.75)
        if normAll<0 :#or gamma2>gamma1 or Ebreak < 200:
            sumlogpois+=308
        if TMath.Poisson(measurement,model)==0:
            sumlogpois+=308
        if TMath.Poisson(measurement,model)!=0:
            sumlogpois+=-log(TMath.Poisson(measurement,model))
    return sumlogpois
# Start program
if __name__ == "__main__":
    # read Eavgbin.olo
    datEavgbin=np.genfromtxt('Eavgbin.olo')
    Eavgbin=datEavgbin[:,1]
    # open E275Flux file
    File=TFile('present.root')
    h=File.Get('E3')
    g=TGraph(h)
    plotslps=TH1F('plotslps','plotslps',400,100,500)
    #plotslps=TH1F('plotslps','plotslps',100,2.5,3.1)
#    for i in range(100):
#        gamma2=2.5+i*(3.0-2.5)/100.
    for i in range(400):
        Eb=100.+i
        slps=SumlogPois([30024,2.849,2.716,Eb,0.000215]) # AMS-02 [30024,2.849,2.716,336,0.000215]
        plotslps.SetBinContent(i+1,slps)
    gslps=TGraph(plotslps)
    C=TCanvas('C','C',800,600)
    gslps.GetYaxis().SetTitle('SumLogPois')
    gslps.GetXaxis().SetTitle('#gamma_{2}')
    gslps.Draw()
    raw_input()
