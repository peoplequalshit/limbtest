from ROOT import *
from math import *
from array import *
import pyfits
import numpy

# open measurement dat
File=TFile('present.root')
h=File.Get('E3')
# open Model dat
dataBPL=numpy.genfromtxt('specBPL.dat')
xBPL,yBPL=dataBPL[:,0],dataBPL[:,1]

dataSPL=numpy.genfromtxt('specSPL.dat')
xSPL,ySPL=dataSPL[:,0],dataSPL[:,1]

dataSPLnHe=numpy.genfromtxt('specSPLnoHe.dat')
xSPLnHe,ySPLnHe=dataSPLnHe[:,0],dataSPLnHe[:,1]

dataBPLnHe=numpy.genfromtxt('specBPLnoHe.dat')
xBPLnHe,yBPLnHe=dataBPLnHe[:,0],dataBPLnHe[:,1]

datEavgbin=numpy.genfromtxt('Eavgbin.olo')
Eavgbin=datEavgbin[:,1]

dat17=numpy.genfromtxt('spec17.dat')
x17,y17=dat17[:,0],dat17[:,1]
dat16=numpy.genfromtxt('spec16.dat')
x16,y16=dat16[:,0],dat16[:,1]

V=array('d',xSPL)
EBPL=TH1F('EBPL','#gamma-ray from proton BPL with He (Model)',len(V)-1,V)
ESPL=TH1F('ESPL','#gamma-ray from proton SPL with He (Model)',len(V)-1,V)
EBPLnHe=TH1F('EBPLnHe','#gamma-ray from proton BPL (Model)',len(V)-1,V)
ESPLnHe=TH1F('ESPLnHe','#gamma-ray from proton SPL (Model)',len(V)-1,V)
EHe=TH1F('EHe','Helium spectrum (AMS-02)',len(V)-1,V)
C1=TCanvas('C1','C1',800,600)
for k in range(len(V)-1):
    EBPL.SetBinContent(k+1,yBPL[k]*(xBPL[k]**2.75))
    ESPL.SetBinContent(k+1,ySPL[k]*(xSPL[k]**2.75))
    ESPLnHe.SetBinContent(k+1,ySPLnHe[k]*(xSPLnHe[k]**2.75))
    EBPLnHe.SetBinContent(k+1,yBPLnHe[k]*(xBPLnHe[k]**2.75))
    EHe.SetBinContent(k+1,((y17[k]-y16[k])*10)*(x16[k]**2.75))
EBPL.GetXaxis().SetTitle('E (GeV)')
EBPL.GetYaxis().SetTitle('flux*E^{2.75}')
EBPL.SetMarkerStyle(0)
EBPL.SetMarkerColor(9)
ESPL.SetMarkerStyle(0)
ESPL.SetMarkerColor(30)
ESPLnHe.SetMarkerStyle(0)
EBPLnHe.SetMarkerStyle(0)
EHe.SetMarkerStyle(22)
EHe.SetMarkerColor(39)
bandh=h.Clone('bandh')
bandh.SetFillColorAlpha(kRed,0.3)
h.SetStats(0)
h.GetYaxis().SetTitle('E^{2.75}Flux (GeV^{1.75}m^{-2}s^{-1}sr^{-1})')
h.Draw()
gSPL=TGraph(ESPL)
gSPL.SetLineStyle(9)
gSPL.SetLineWidth(2)
gSPL.SetLineColor(4)
gSPL.Draw('same')
gBPL=TGraph(EBPL)
gBPL.SetLineStyle(7)
gBPL.SetLineWidth(3)
gBPL.SetLineColor(3)
gBPL.Draw('same')
gSPLnHe=TGraph(ESPLnHe)
gSPLnHe.SetLineWidth(2)
gSPLnHe.SetLineColorAlpha(kBlack,0.2)
gSPLnHe.Draw('same')
gBPLnHe=TGraph(EBPLnHe)
gSPLnHe.SetLineWidth(2)
gBPLnHe.SetLineColor(6)
gBPLnHe.Draw('same')
EHe.Draw('Psame')
C1.BuildLegend(0.3).SetFillColor(0)
for i in range(50):
    if Eavgbin[i]<100.:
        syserr=0.05
    if Eavgbin[i]>=100.:
        syserr=0.05+0.1*(log10(Eavgbin[i]*1000.)-5.)
    toterr=syserr*h.GetBinContent(i+1)+h.GetBinError(i+1)
    bandh.SetBinError(i+1,toterr)
bandh.Draw('E3same')
h.SetMarkerColor(2)
h.SetLineColor(2)
h.SetMarkerStyle(20)
#h.Draw('same')
#gBPL.Draw('same')
#gSPL.Draw('same')
#gBPLnHe.Draw('same')
gSPLnHe.Draw('same')
EBPL.SetTitle('Plot of Model and measurement')
C1.SetLogx()
C1.SetLogy()
h.SetTitle('Model vs  measurement')
h.GetYaxis().SetRangeUser(1,15)
print "finish"
raw_input()

