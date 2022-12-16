import ROOT
import time
import os
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)


def drawMezonHist(modes):
	f = ROOT.TFile("DstDst0Dss_14modes.root")

	canv = ROOT.TCanvas("canvDs","D^{0} histograms",1300,500)

	canv.Divide(1,1)
	hists = []

	i = 0
	for key in modes:
		hname = 'hDs' + str(i)
		if "ds0" in key:
			h = ROOT.TH1F(hname,modes[key]["title"],100,2.002,2.012)
			h.SetMinimum(0)
			if "2" in key or "3" in key:
				h.SetMaximum(10000)
			hists.append(h)
		else:
			h = ROOT.TH1F(hname,modes[key]["title"],100,2.002,2.017)
			h.SetMinimum(0)
			hists.append(h)					    
		hists.append(hists[3*i].Clone( hists[3*i].GetName()+'_cut' )) 
		hists.append(hists[3*i].Clone( hists[3*i].GetName()+'_cut_gen' ))		   
		t = f.Get(key) 
		iFig = i + 1
		canv.cd(iFig)
		print(t)
		print(hists)		 
		t.Draw( 'ms_ds'+'>>'+hists[3*i].GetName() )
		t.Draw( 'ms_ds'+'>>'+hists[3*i+1].GetName(), modes[key]["cut"] )
		t.Draw( 'ms_ds'+'>>'+hists[3*i+2].GetName(), '(gen_ds == 1)')		
		
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
	eg_min = 0.04
	pt_d0_min = 1.0
	pt_d0_cut = '(pt_d0>' + str(pt_d0_min) + ')'
	mgg_s0_min = 0.13
	mgg_s0_max = 0.14
	mgg_s0_cut = '(mgg_s0>'+str(mgg_s0_min)+') & (mgg_s0<'+str(mgg_s0_max)+ ')'
	eg_cut = '(eg1_s0>'+str(eg_min)+') & (eg2_s0>'+str(eg_min)+ ')'
	hel_d0_min = -0.1
	hel_d0_max = 0.1
	hel_d0_cut = '(hel_d0<'+str(hel_d0_min)+') & (hel_d0>'+str(hel_d0_max)+ ')'
	modes = {
		"dsch3" : {"title" : "D*^{+}#rightarrow D^{0}(K3#pi)#pi_{s}^{+};M(D*^{+});Counts", "cut" : '(ms_d0>1.85) & (ms_d0<1.88)' },
			
}
	drawMezonHist(modes)