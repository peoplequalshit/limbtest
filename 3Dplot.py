from ROOT import *
from math import *
from array import *
import numpy as np
import pyfits
from scipy.optimize import fmin
from scipy.stats import poisson
import os
import sys
global gamma1,gamma2,Ebreak,g
def Fluxcompute(A,gamma1,gamma2,Ebreak,normAll):
    os.system('gfortran BPLwHe.f frag.f -o test1.out')
    RunFlux='./test1.out %f %f %f %f %f'%(A,gamma1,gamma2,Ebreak,normAll)
    os.system(RunFlux)
def SumlogPois(dummy):
    A=dummy[0]
    normAll=dummy[1]
    print A,gamma1,gamma2,Ebreak,normAll
    Fluxcompute(A,gamma1,gamma2,Ebreak,normAll)
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
# Call flux
File=TFile('/Users/Macintosth/Desktop/Backupalljabcosmic/backupgalaxy/research/flux2.root') # for Laptop
#File=TFile('/home/jab/backupgalaxy/research/flux.root') #For cluster
h=File.Get('E3')
g=TGraph(h)
# start program
clay=TH3F('clay','clay of sumlogpois',50,2.5,3.0,50,2.5,3.0,200,200,400)
for i in range(clay.GetNbinsX()):
    gamma1=2.5+i*0.01 # 2.50-2.99
    for j in range(clay.GetNbinsY()):
        gamma2=2.5+j*0.01 # 2.50-2.99
        for k in range(clay.GetNbinsZ()):
            Ebreak=float(200+k) #200-399
            bestfit=fmin(SumlogPois,[32544,0.00021])
            clay.SetBinContent(i+1,j+1,k+1,SumlogPois(bestfit))
            if k==3:
                break
C=TCanvas('C','C',1200,400)
C.Divide(3,0)
clay.GetXaxis().SetTitle('gamma1')
clay.GetYaxis().SetTitle('gamma2')
clay.GetZaxis().SetTitle('Ebreak')

gStyle.SetFillColor(kBird)
# Draw to Canvas
C.cd(1)
xy=clay.Project3D('xy')
xy.SetStats(0)
xy.Draw('COLZ')
C.cd(2)
xz=clay.Project3D('xz')
xz.SetStats(0)
xz.Draw('COLZ')
C.cd(3)
yz=clay.Project3D('yz')
yz.SetStats(0)
yz.Draw('COLZ')
# Save TH3F to root file                                                        
file1=TFile('playground.root','RECREATE')
clay.Write()
file1.Write()
xy.Write()
xz.Write()
yz.Write()
file1.Close()

C.SaveAs('playground.png')
print clay.GetBinContent(clay.GetMaximumBin()) #GetMaximum value of this
print 'finish'
#raw_input()
