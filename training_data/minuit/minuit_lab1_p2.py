import sys , ROOT, time
from math import *
import numpy as np
import ctypes

def Lorentz_linear(x, params):
	Area, Gamma, x0, A, B = params[0],params[1],params[2],params[3],params[4],
	return Area * ((1/np.pi)*Gamma/(np. square (x-x0)+np.square (Gamma)))+A*x+B

params = [5000, 20., 90., -0.2, 60.]
tArea, tGamma, tx0, tA, tB = 5000, 20., 90., -0.2, 60.0
rnd = ROOT. TRandom3 ()
nChan = 200
nPar = 5
xExpt = np. linspace (1, nChan, nChan)
Tot = [Lorentz_linear(x, params) for x in xExpt]
dx = xExpt [1] - xExpt[0]
yExpt = np.zeros_like(xExpt)
for chan in range(nChan):
	yExpt[chan] = rnd.Poisson(Tot[chan])
indPos = yExpt > 0
nPos = indPos.sum()
print (indPos)
print (nPos)

def FCN(npar, gin, f, par, iflag):
	global valFCN
	yTheor = np.array([Lorentz_linear(x, par) for x in xExpt])
	indPos = yExpt > 0
	arrayFCN = np.square (yExpt [indPos] - yTheor [indPos])/yExpt[indPos]
	valFCN = np.sum(arrayFCN)
	f.value = valFCN

def FCN2(npar, gin, f,par ,iflag):
	global valFCN
	yTheor = np.array ([Lorentz_linear(x, par) for x in xExpt])
	indPos = yExpt > 0
	fi = yTheor[indPos]
	di = yExpt[indPos]
	fi = np.where(fi<0,1,fi)
	arrayFCN = (fi-di)-di*np.log(fi/di)
	valFCN = np.sum(arrayFCN)
	f.value = valFCN

# Now ready for minimization step
ierflg = ctypes.c_int(0)
minuit = ROOT.TMinuit(nPar)
minuit . SetPrintLevel (1)
minuit .SetFCN(FCN2)
errordef = 1.

minuit.DefineParameter(0, 'Area', 13, 1e-2, 0., 0.)
minuit.DefineParameter (1, 'g', 10., 1e-4, 0., 0.) 
minuit.DefineParameter (2, 'x0', 100, 1e-4, 0., 0.)
minuit.DefineParameter (3, 'a_bg', -0.3, 1e-4, 0., 0.)
minuit.DefineParameter (4, 'b_bg', 50, 1e-4, 0., 0.)

minuit .mncomd("SET ERR "+str(errordef), ierflg);
minuit .mncomd("SET STR 1", ierflg); # strategy (1)
maxIter=10000
tolerance =1.e-8
minuit .mncomd("MIGRAD "+str(maxIter)+' '+str(tolerance), ierflg)

minuit .mncomd("SET STR 2", ierflg); # strategy (2)
minuit .mncomd("MIGRAD "+str(maxIter)+' '+str(tolerance), ierflg)
minuit .mnmnos() # Minos

ndf = nPos-minuit.GetNumFreePars()
print (' chi2/ndf: ' , valFCN, '/' , ndf)
parFit = np.zeros(nPar)
errFit = np.zeros(nPar)
valPar , errPar = ctypes.c_double(0.0), ctypes.c_double(0.0)
for iPar in range(nPar):
	minuit .GetParameter(iPar,valPar , errPar )
	parFit [ iPar ] = valPar.value
	errFit [ iPar ] = errPar.value
Area1, gamma1, x01, a1, b1 = parFit[0], parFit[1], parFit[2], parFit[3], parFit[4]

# histogram decoration
ROOT.gStyle.SetOptStat(0)
h = ROOT.TH1F('histLorentz','Lorentzian MLH',nChan-1,xExpt-dx/2.)
h.SetMinimum(0)
h.SetMarkerColor(ROOT.kBlack)
h. SetLineColor(ROOT.kBlack)
h.SetMarkerStyle(20)
h.SetMarkerSize(1)
h.GetXaxis() . SetTitle ( ' channels ' )
h.GetYaxis() . SetTitle ( 'Counts')

fTrue = ROOT.TF1('fTrue','[0]*(([1]/3.14159265359)/((x - [2])*(x - [2]) + [1]*[1])) + [3] * x + [4]',xExpt[0],xExpt[-1])
fTrue . SetLineColor(ROOT.kRed)
fTrue .SetLineWidth(2)
fTrue .SetParameters(tArea, tGamma, tx0, tA, tB)


fFit = ROOT.TF1('fFit','[0]*(([1]/3.14159265359)/((x - [2])*(x - [2]) + [1]*[1])) + [3] * x + [4]',xExpt[0],xExpt[-1])
fFit . SetLineColor(ROOT.kBlue)
fFit .SetParameters(Area1, gamma1, x01, a1, b1)

hLeg = ROOT.TLegend(0.8,0.8,0.95,0.95)
hLeg.AddEntry(h,'Data', 'p')
hLeg.AddEntry(fTrue,'True' , ' l ' )
hLeg.AddEntry(fFit, ' Fit ' , ' l ' )
hLeg. SetFillColor (0)
for chan in range(nChan):
	h.SetBinContent(chan+1,yExpt[chan])
cMnt = ROOT.TCanvas('cMnt','chi2',600,500)
h.Draw('e')
fTrue.Draw('same&l')
ROOT.gPad.SetTicks(1,1)
ROOT.gPad.RedrawAxis()
fFit.Draw('same&l')

hLeg.Draw()
ROOT.gPad.Update()