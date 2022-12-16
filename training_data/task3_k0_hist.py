import ROOT
import time
import os
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)


def drawMezonHist(modes):
	f = ROOT.TFile("DstDst0_9modes.root")

	canv = ROOT.TCanvas("canvDs","Ks histograms",1300,500)

	#canv.Divide(2,2)
	hists = []

	i = 0
	for key in modes:
	    hname = 'hDs' + str(i)
	    hists.append(ROOT.TH1F(hname,"K0",1000,0.46,0.54))
	    hists.append(hists[2*i].Clone( hists[2*i].GetName()+'_cut' ))    
	    t = f.Get(key) 
	    iFig = i + 1
	    canv.cd(iFig) 
	    t.Draw( 'ms_k0'+'>>'+hists[2*i].GetName() )
	    t.Draw( 'ms_k0'+'>>'+hists[2*i+1].GetName(), modes[key]["cut"] )
	    hists[2*i].Draw()
	    hists[2*i+1].Draw('same&h')
	    hists[2*i+1].SetFillColor(ROOT.kCyan+3)
	    i += 1
	interrupt = input()


if __name__ == '__main__':
	modes = {
	"dsc_k03p" : {"title" : "K#pi", "cut" : '(ms_k0>0.492) & (ms_k0<0.5035)' },	
	}
	drawMezonHist(modes)
