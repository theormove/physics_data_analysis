import ROOT
import time
import os
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)


def drawMezonHist(modes):
	f = ROOT.TFile("DstDst0_9modes.root")

	canv = ROOT.TCanvas("canvDs","D* histograms",1300,500)

	canv.Divide(3,2)
	hists = []

	i = 0
	for key in modes:
	    hname = 'hDs' + str(i)
	    hists.append(ROOT.TH1F(hname,modes[key]["title"],100,2.002,2.017))
	    hists.append(hists[2*i].Clone( hists[2*i].GetName()+'_cut' ))    
	    t = f.Get(key) 
	    iFig = i + 1
	    canv.cd(iFig)
	    print(t)
	    print(hists) 
	    t.Draw( 'ms_ds'+'>>'+hists[2*i].GetName() )
	    t.Draw( 'ms_ds'+'>>'+hists[2*i+1].GetName(), modes[key]["cut"] )
	    hists[2*i].Draw()
	    hists[2*i+1].Draw('same&h')
	    hists[2*i+1].SetFillColor(ROOT.kCyan+3)
	    i += 1
	interrupt = input()


if __name__ == '__main__':
	modes = {
	"dsch1" : {"title" : "D*^{+}#rightarrow D^{0}(K#pi)#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_d0>1.85) & (ms_d0<1.88)' },
	"dsch2" : {"title" : "D*^{+}#rightarrow D^{0}(K3#pi)#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_d0>1.85) & (ms_d0<1.88)' },
	"dsch3" : {"title" : "D*^{+}#rightarrow D^{0}(K#pi#pi^{0})#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_d0>1.85) & (ms_d0<1.88)' },
	"dsc_k03p" : {"title" : "D*^{+}#rightarrow D^{0}(K^{0}_{S}#pi^{-}#pi^{+})#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_d0>1.85) & (ms_d0<1.88)' },
	"dsc_k04p" : {"title" : "D*^{+}#rightarrow D^{0}(K^{0}_{S}#pi^{-}#pi^{+}#pi^{0})#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_d0>1.85) & (ms_d0<1.88)' },
	"dsc_dcp0" : {"title" : "D*^{+}#rightarrow D^{+}#pi_{s}^{0};M(D*);Counts", "cut" : '(ms_dc>1.857) & (ms_dc<1.882)' },		
	}
	drawMezonHist(modes)