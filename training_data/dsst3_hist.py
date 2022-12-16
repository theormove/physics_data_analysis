import ROOT
import numpy
import time


#Initializing 

f = ROOT.TFile("DssDsst_6modes.root")

t  = f.Get("dsst3")

start_time = time.time()

events = t.GetEntries()

hDst = ROOT.TH1F('hDs','D*^{+}_{s}#rightarrow D^{+}_{s}(K^{0}_{s}K^{+})#gamma;Counts',200,2.06,2.16)
#hD_nocut = ROOT.TH1F('hDsn','D*',100,2.06,2.014)
hDs = ROOT.TH1F('hD0','D^{+}_{s};M(D^{+}_{s});Counts',200,1.9,2.05)
#hD0_nocut = ROOT.TH1F('hD0n','D0',100,1.7,2)
hK = ROOT.TH1F('hK','K^{0}_{S};M(K^{0}_{S});M(D*_{s});Counts',200,0.45,0.55)
#hK_nocut = ROOT.TH1F('hKn','K^{0}_{S}',100,0.45,0.55)
canv = ROOT.TCanvas("canvDs","dsst3 modes histograms",1300,500)
hAngle = ROOT.TH1F('angl','Angle',100,0.0,4)
canv.Divide(3,1)

#Setting cuts 

angle_cut = 0.2
min_dist = 1
max_dist = 20
ms_dss_min = 1.9
ms_dss_max = 2.05
ms_dsst_max = 2.16
ms_dsst_min = 2.06

#Go over all events
for i in range(events):
	t.GetEntry(i)
	'''
	k0_point = numpy.array((t.vx_k0,t.vy_k0,t.vz_k0)) 
	d0_point = numpy.array((t.vx_d0,t.vy_d0,t.vz_d0))
	dist = numpy.linalg.norm(d0_point-k0_point)
	'''
	k0_pos = ROOT.TVector3(t.vx_k0,t.vy_k0,t.vz_k0)
	dss_pos = ROOT.TVector3(t.vx_dss,t.vy_dss,t.vz_dss)
	dist_vect = k0_pos-dss_pos
	dist = dist_vect.Mag()

	k0_vect = ROOT.TVector3()
	dss_vect = ROOT.TVector3()
	k0_vect.SetMagThetaPhi(1,t.th_k0,t.ph_k0)
	dss_vect.SetMagThetaPhi(1,t.th_dss,t.ph_dss)

	angle = k0_vect.Angle(dss_vect)  
	hAngle.Fill(angle)
	if (dist>min_dist) and (dist<max_dist)\
	 and (t.ms_dsst < ms_dsst_max) and (t.ms_dsst > ms_dsst_min) and (t.ms_dss>ms_dss_min) and (t.ms_dss<ms_dss_max):		
			hDst.Fill(t.ms_dsst)
			hDs.Fill(t.ms_dss)
			hK.Fill(t.ms_k0)

	#if dist>1 and dist<20:
	#	h.Fill(t.ms_ds)

print("--- %s seconds ---" % (time.time() - start_time))

#Drawing
canv.cd(1)
hDst.Draw()
hDst.SetFillColor(ROOT.kCyan+3)
canv.cd(2)
hDs.Draw('same&h')
hDs.SetFillColor(ROOT.kCyan+3)
canv.cd(3)
#t.Draw('ms_k0>>hKn')
#hK_nocut.Draw()
hK.Draw('same&h')
hK.SetFillColor(ROOT.kCyan+3)

