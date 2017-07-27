from ROOT import *
from math import *
from array import *
import numpy as np
import pyfits
from scipy.optimize import fmin,minimize,basinhopping,brute
import os
import sys
def Fluxcompute(A,gamma1,gamma2,Ebreak,normAll):
    os.system('gfortran BPLwHe.f frag.f -o test1.out') #use SPLwHe
    RunFlux='./test1.out %f %f %f %f %f'%(A,gamma1,gamma2,Ebreak,normAll)
    os.system(RunFlux)
def SumlogPois(dummy):
    print dummy
    A=dummy[0]
    gamma1=dummy[1]
    gamma2=dummy[2]
    Ebreak=dummy[3]
    normAll=dummy[4]
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
#variable that use x,y,V,E1,CE1,h,CE2
if __name__ == "__main__":
    # read Eavgbin.olo
    datEavgbin=np.genfromtxt('Eavgbin.olo')
    Eavgbin=datEavgbin[:,1]
    #Plot real gamma-ray flux
    File=TFile('present.root') #####
    h=File.Get('E3') ####
    h.SetTitle('Measurement')
    CE3=TCanvas('CE3','CE3',800,600)
    h.SetStats(0)
    h.Draw()
    CE3.SetLogx()
    CE3.SetLogy()
    g=TGraph(h) #line between point
    #Compute best fit
    #bestfit=fmin(SumlogPois,[30024.,2.849,2.716,336,0.000215])
    ##test
    rangetrial=(slice(1000.,40000.,1000.),slice(2.5,3.1,0.05),slice(2.5,3.1,0.05),slice(150,500,10),slice(0.0001,0.001,0.00005))
    res=brute(SumlogPois,rangetrial)
    # save best output
    Fbest=open('bestoutput.olo','w')
    Fbest.write(res)
    Fbest.close()
    #Plot K&O flux
    file=open('0.dat')
    data = np.genfromtxt('0.dat')
    #print data
    x,y=data[:,0],data[:,1]
    #CE1=TCanvas("CE1","Canvas Discrete Energy",800,600)
    V=array('d',x)
    E2=TH1F("E2","K&O prediction",len(V)-1,V)
    for k in range(len(y)):
        E2.SetBinContent(k+1,y[k]*(x[k]**2.75))
    #h.Draw('E1')# Try to draw same graph with canvas 2
    E2.SetMarkerStyle(24)
    E2.SetMarkerColor(2)
    E2.Draw("Psame")
    h.GetXaxis().SetTitle('E (GeV)')
    h.GetYaxis().SetTitle('E^{2.75}Flux (GeV^{1.75}m^{-2}s^{-1}sr^{-1})')
    CE3.BuildLegend();
    h.SetTitle('Measurement vs Model')
    print bestfit
    raw_input()


    #os.chdir('/home/jab/backupgalaxy/research')
    #os.system('python perflux.py')#/home/jab/backupgalaxy/research/perflux.py
