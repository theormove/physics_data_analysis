import ROOT
import numpy
import time


#Initializing 

f = ROOT.TFile("DstDst0_9modes.root")

t  = f.Get("dsc_k04p")

start_time = time.time()

events = t.GetEntries()

hD = ROOT.TH1F('hDs','D*^{+}#rightarrow D^{0}(K^{0}_{S}#pi^{-}#pi^{+}#pi^{0})#pi_{s}^{+};M(D*);Counts',200,2.006,2.014)
#hD_nocut = ROOT.TH1F('hDsn','D*',100,2.06,2.014)
hD0 = ROOT.TH1F('hD0','D^{0};M(D^{0});Counts',200,1.7,2)
#hD0_nocut = ROOT.TH1F('hD0n','D0',100,1.7,2)
hK = ROOT.TH1F('hK','K^{0}_{S};M(K^{0}_{S});Counts',200,0.45,0.55)
#hK_nocut = ROOT.TH1F('hKn','K^{0}_{S}',100,0.45,0.55)
canv = ROOT.TCanvas("canvDs","dsc_k04p modes histograms",1300,500)
hAngle = ROOT.TH1F('angl','Angle',100,0.0,4)
canv.Divide(3,1)

#Setting cuts 

angle_cut = 0.2
min_dist = 1
max_dist = 20
ms_d0_min = 1.7
ms_d0_max = 2
ms_ds_max = 2.014
ms_ds_min = 2.006

#Go over all events
for i in range(1000000):
	t.GetEntry(i)
	'''
	k0_point = numpy.array((t.vx_k0,t.vy_k0,t.vz_k0)) 
	d0_point = numpy.array((t.vx_d0,t.vy_d0,t.vz_d0))
	dist = numpy.linalg.norm(d0_point-k0_point)
	'''
	k0_pos = ROOT.TVector3(t.vx_k0,t.vy_k0,t.vz_k0)
	d0_pos = ROOT.TVector3(t.vx_d0,t.vy_d0,t.vz_d0)
	dist_vect = k0_pos-d0_pos
	dist = dist_vect.Mag()

	k0_vect = ROOT.TVector3()
	d0_vect = ROOT.TVector3()
	k0_vect.SetMagThetaPhi(1,t.th_k0,t.ph_k0)

	d0_vect.SetMagThetaPhi(1,t.th_d0,t.ph_d0)
	angle = k0_vect.Angle(d0_vect)  
	hAngle.Fill(angle)
	if (angle < angle_cut) and (dist>min_dist) and (dist<max_dist)\
	 and (t.ms_ds < ms_ds_max) and (t.ms_ds > ms_ds_min) and (t.ms_d0>ms_d0_min) and (t.ms_d0<ms_d0_max):		
			hD.Fill(t.ms_ds)
			hD0.Fill(t.ms_d0)
			hK.Fill(t.ms_k0)

	#if dist>1 and dist<20:
	#	h.Fill(t.ms_ds)

print("--- %s seconds ---" % (time.time() - start_time))

#Drawing
canv.cd(1)
hD.Draw()
hD.SetFillColor(ROOT.kCyan+3)
canv.cd(2)
hD0.Draw('same&h')
hD0.SetFillColor(ROOT.kCyan+3)
canv.cd(3)
#t.Draw('ms_k0>>hKn')
#hK_nocut.Draw()
hK.Draw('same&h')
hK.SetFillColor(ROOT.kCyan+3)

