import ROOT
import time
import os
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)


def drawMezonHist(modes):
	f = ROOT.TFile("DstDst0_9modes.root")

	canv = ROOT.TCanvas("canvDs","D* histograms",1300,500)

	canv.Divide(2,2)
	hists = []

	i = 0
	for key in modes:
	    hname = 'hDs' + str(i)
	    hists.append(ROOT.TH1F(hname,'D*^{+}#rightarrow D^{0}'+'('+ modes[key]["title"]+')'+ '#pi_{s}^{+};M(D*);Counts',100,2.002,2.017))
	    hists.append(hists[2*i].Clone( hists[2*i].GetName()+'_cut' ))    
	    t = f.Get(key) 
	    iFig = i + 1
	    canv.cd(iFig) 
	    t.Draw( 'ms_ds'+'>>'+hists[2*i].GetName() )
	    t.Draw( 'ms_ds'+'>>'+hists[2*i+1].GetName(), modes[key]["cut"] )
	    hists[2*i].Draw()
	    hists[2*i+1].Draw('same&h')
	    hists[2*i+1].SetFillColor(ROOT.kCyan+3)
	    i += 1
	interrupt = input()


if __name__ == '__main__':
	modes = {
	"dsch1" : {"title" : "K#pi", "cut" : '(ms_d0>1.865) & (ms_d0<1.866)' },
	"dsch2" : {"title" : "K3#pi", "cut" : '(ms_d0>1.85) & (ms_d0<1.88)' },
	"dsch3" : {"title" : "K#pi#pi^{0}", "cut" : '(ms_d0>1.85) & (ms_d0<1.88)' },	
	}
	drawMezonHist(modes)
