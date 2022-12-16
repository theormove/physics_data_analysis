import ROOT
import time
import os
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)


def drawMezonHist(modes):
	f = ROOT.TFile("DstDst0Dss_14modes.root")

	canv = ROOT.TCanvas("canvDs","D_{s} histograms",1300,500)

	canv.Divide(1,1)
	hists = []

	i = 0
	for key in modes:
		hname = 'hDs' + str(i)
		if "dsst" in key:
			h = ROOT.TH1F(hname,modes[key]["title"],200,2.08,2.14)
			h.SetMinimum(0)
			if "2" in key or "3" in key:
				h.SetMaximum(600)			
			hists.append(h)
			hists.append(hists[3*i].Clone( hists[3*i].GetName()+'_cut' ))    
			hists.append(hists[3*i].Clone( hists[3*i].GetName()+'_cut_gen' ))			
			t = f.Get(key) 
			iFig = i + 1
			canv.cd(iFig)
			print(t)
			print(hists) 
			t.Draw( 'ms_dsst'+'>>'+hists[3*i].GetName() )
			t.Draw( 'ms_dsst'+'>>'+hists[3*i+1].GetName(), modes[key]["cut"] )
			t.Draw( 'ms_dsst'+'>>'+hists[3*i+2].GetName(), '(gen_dsst == 1)')			
		else:	
			h = ROOT.TH1F(hname,modes[key]["title"],200,1.895,2.045)
			h.SetMinimum(0)
			hists.append(h)
			hists.append(hists[3*i].Clone( hists[3*i].GetName()+'_cut' ))
			hists.append(hists[3*i].Clone( hists[3*i].GetName()+'_cut_gen' ))			    
			t = f.Get(key) 
			iFig = i + 1
			canv.cd(iFig)
			print(t)
			print(hists) 
			t.Draw( 'ms_dss'+'>>'+hists[3*i].GetName() )
			t.Draw( 'ms_dss'+'>>'+hists[3*i+1].GetName(), modes[key]["cut"] )
			t.Draw( 'ms_dss'+'>>'+hists[3*i+2].GetName(), '(gen_dss == 1)')		
		
		hists[3*i].Draw()
		hists[3*i].SetLineWidth(3)		
		

		hists[3*i+2].Draw('same&h')
		hists[3*i+2].SetLineColor(ROOT.kGreen+1)
		hists[3*i+2].SetLineWidth(3)		
		
		hists[3*i+1].Draw('same&h')
		hists[3*i+1].SetLineWidth(3)		
		hists[3*i+1].SetLineColor(ROOT.kCyan+1)

		legend =  ROOT.TLegend(0.1,0.7,0.48,0.9)
		legend.SetHeader("Candidates")
		legend.AddEntry(hists[3*i].GetName(),"Unclined")
		legend.AddEntry(hists[3*i + 1].GetName(),"With Cuts")
		legend.AddEntry(hists[3*i + 2].GetName(),"Real particles")
		legend.Draw()		
		i += 1
	interrupt = input()


if __name__ == '__main__':
	modes = {
	"ds_k0sk" : {"title" : "D^{+}_{s}#rightarrow  #phi#pi^{+};M(D_{s});Counts", "cut" : '(ms_k0>0.492) & (ms_k0<0.505)' },
	"ds_ksr0k" : {"title" : "D^{+}_{s}#rightarrow K*^{0}K^{+};M(D_{s});Counts", "cut" : '(ms_ks0>0.86) & (ms_ks0<0.94)' },
	"ds_ph0p" : {"title" : "D^{+}_{s}#rightarrow K^{0}_{s}K^{+};M(D_{s});Counts", "cut" : '(ms_ph0>1.015) & (ms_ph0<1.025)' },
    "dsst1" : {"title" : "D*^{+}_{s}#rightarrow D^{+}_{s}(#phi#pi^{+})#gamma;M(D*_{s});Counts", "cut" : '(ms_dss>1.96) & (ms_dss<1.98) & (ms_ph0>1.015) & (ms_ph0<1.025)' },
    "dsst2" : {"title" : "D*^{+}_{s}#rightarrow D^{+}_{s}(K*^{0}K^{+})#gamma;M(D*_{s});Counts", "cut" : '(ms_dss>1.96) & (ms_dss<1.98) & (ms_ks0>0.88) & (ms_ks0<0.92)' },
    "dsst3" : {"title" : "D*^{+}_{s}#rightarrow D^{+}_{s}(K^{0}_{s}K^{+})#gamma;M(D*_{s});Counts", "cut" : '(ms_dss>1.96) & (ms_dss<1.98) & (ms_k0>0.492) & (ms_k0<0.505)' },             
	}
	drawMezonHist(modes)