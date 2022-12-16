import ROOT
import time
import os
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)


def drawMezonHist(modes):
	f = ROOT.TFile("DstDst0_9modes.root")

	canv = ROOT.TCanvas("canvDs","D^{0} histograms",1300,500)

	canv.Divide(3,1)
	hists = []

	i = 0
	for key in modes:
		hname = 'hDs' + str(i)
		if "ds0" in key:
			h = ROOT.TH1F(hname,modes[key]["title"],100,1.998,2.014)
			h.SetMinimum(0)
			if "2" in key or "3" in key:
				h.SetMaximum(4000)
			hists.append(h)
		else:
			h = ROOT.TH1F(hname,modes[key]["title"],100,2.002,2.017)
			h.SetMinimum(0)
			hists.append(h)					    
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
	eg_min = 0.05
	pt_d0_min = 1.0
	pt_d0_cut = '(pt_d0>' + str(pt_d0_min) + ')'
	eg_cut = '(eg1_s0>'+str(eg_min)+') & (eg2_s0>'+str(eg_min)+ ')'
	modes = {
		"ds01" : {"title" : "D*^{0}#rightarrow D^{0}(K#pi)#pi_{s}^{0};M(D^{0});Counts",\
			"cut" : '(ms_d0>1.85) & (ms_d0<1.88) & '+ eg_cut +' & ' + pt_d0_cut },
		"ds02" : {"title" : "D*^{0}#rightarrow D^{0}(K3#pi)#pi_{s}^{0};M(D^{0});Counts",\
			"cut" : '(ms_d0>1.85) & (ms_d0<1.88) & '+ eg_cut +' & ' + pt_d0_cut  },
		"ds03" : {"title" : "D*^{0}#rightarrow D^{0}(K#pi#pi^{0})#pi_{s}^{0};M(D^{0});Counts",\
			"cut" : '(ms_d0>1.85) & (ms_d0<1.88) & '+ eg_cut +' & ' + pt_d0_cut  },	
}
	drawMezonHist(modes)