import ROOT
f = ROOT.TFile("DstDst0Dss_14modes.root")
hname = 'hDs'
tree_name= 'ds01'
h = ROOT.TH1F(hname,"D*^{0} Candidates",100,2.002,2.012)
t = f.Get(tree_name)
t.Draw( 'ms_ds'+'>>'+hname, '(ms_d0>1.85 & ms_d0<1.88)')

#h.Draw()