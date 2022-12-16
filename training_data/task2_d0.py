import ROOT
import time
import os
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)


def drawMezonHist(modes):
    f = ROOT.TFile("DstDst0_9modes.root")

    canv = ROOT.TCanvas("canvDs","D0/D^{+} histograms",1300,500)

    canv.Divide(3,2)
    hists = []

    i = 0
    for key in modes:
        hname = 'hDs' + str(i)
        t = f.Get(key) 
        iFig = i + 1
        canv.cd(iFig)    
        if key != "dsc_dcp0": 
            h = ROOT.TH1F(hname,modes[key]["title"],100,1.81,1.92)
            h.SetMinimum(0)
            hists.append(h)
            hists.append(hists[2*i].Clone( hists[2*i].GetName()+'_cut' )) 
            t.Draw( 'ms_d0'+'>>'+hists[2*i].GetName() )
            t.Draw( 'ms_d0'+'>>'+hists[2*i+1].GetName(), modes[key]["cut"] )
        else:
            h = ROOT.TH1F(hname,modes[key]["title"],100,1.82,1.93)
            h.SetMinimum(0)
            hists.append(h)
            hists.append(hists[2*i].Clone( hists[2*i].GetName()+'_cut' )) 
            t.Draw( 'ms_dc'+'>>'+hists[2*i].GetName() )
            t.Draw( 'ms_dc'+'>>'+hists[2*i+1].GetName(), modes[key]["cut"] )                    

        print(t)
        print(hists)
        hists[2*i].GetYaxis().SetTitle("Counts")
        hists[2*i].GetYaxis().SetTitleOffset(0.)
        hists[2*i].Draw()
        hists[2*i+1].Draw('same&h')
        hists[2*i+1].SetFillColor(ROOT.kCyan)
        i += 1
    interrupt = input()


if __name__ == '__main__':
    modes = {
    "dsch1" : {"title" : "D*^{+}#rightarrow D^{0}(K#pi)#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_ds>2.008) & (ms_ds<2.013)' },
    "dsch2" : {"title" : "D*^{+}#rightarrow D^{0}(K3#pi)#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_ds>2.005) & (ms_ds<2.015)' },
    "dsch3" : {"title" : "D*^{+}#rightarrow D^{0}(K#pi#pi^{0})#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_ds>2.005) & (ms_ds<2.015) & (eg1_p0>0.075) & (eg2_p0>0.075)' },
    "dsc_k03p" : {"title" : "D*^{+}#rightarrow D^{0}(K^{0}_{S}#pi^{-}#pi^{+})#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_ds>2.005) & (ms_ds<2.015) & (ms_k0>0.492) & (ms_k0<0.5035)' },
    "dsc_k04p" : {"title" : "D*^{+}#rightarrow D^{0}(K^{0}_{S}#pi^{-}#pi^{+}#pi^{0})#pi_{s}^{+};M(D*);Counts", "cut" : '(ms_ds>2.002) & (ms_ds<2.017) & (ms_k0>0.493) & (ms_k0<0.502)' },
    "dsc_dcp0" : {"title" : "D*^{+}#rightarrow D^{+}#pi_{s}^{0};M(D*);Counts", "cut" : '(ms_ds>2.005) & (ms_ds<2.015)' },  
    }
    drawMezonHist(modes)