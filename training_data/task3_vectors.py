import ROOT
import numpy
import time
from scipy.spatial import distance

#Initializing 

f = ROOT.TFile("DstDst0_9modes.root")

t  = f.Get("dsc_k04p")

start_time = time.time()

events = t.GetEntries()

hD = ROOT.TH1F('hDs','D*',100,2.06,2.014)
hD_nocut = ROOT.TH1F('hDsn','D*',100,2.06,2.014)
hK = ROOT.TH1F('hK','K^{0}_{S}',100,0.45,0.55)
#canv = ROOT.TCanvas("canvDs","D_{s} histograms",1300,500)
hAngle = ROOT.TH1F('angl','Angle',100,0.0,4)
#canv.Divide(2,1)

#Setting cuts 

angle_cut = 0.2
min_dist = 1
max_dist = 20
ms_d0_min = 1.85
ms_d0_max = 1.88
ms_ds_max = 2.014

#Go over all events
for i in range(10000):
	t.GetEntry(i)
	#k0_point = numpy.array((t.vx_k0,t.vy_k0,t.vz_k0)) 
	#d0_point = numpy.array((t.vx_d0,t.vy_d0,t.vz_d0))
	#dist = numpy.linalg.norm(d0_point-k0_point)
	#print(dist)
	k0_pos = ROOT.TVector3(t.vx_k0,t.vy_k0,t.vz_k0)
	d0_pos = ROOT.TVector3(t.vx_d0,t.vy_d0,t.vz_d0)

	k0_vect = ROOT.TVector3()
	d0_vect = ROOT.TVector3()

	k0_vect.SetMagThetaPhi(1,t.th_k0,t.ph_k0)

	d0_vect.SetMagThetaPhi(1,t.th_d0,t.ph_d0)
	dist_vect = k0_pos-d0_pos
	dist = dist_vect.Mag()
	
	angle = k0_vect.Angle(d0_vect)  
	hAngle.Fill(angle)
	if (angle < angle_cut) and (dist>min_dist) and (dist<max_dist)\
	 and (t.ms_ds < ms_ds_max) and (t.ms_d0>ms_d0_min) and (t.ms_d0<ms_d0_max):		
			hD.Fill(t.ms_ds)
			hK.Fill(t.ms_k0)	
	#if dist>1 and dist<20:
	#	h.Fill(t.ms_ds)

print("--- %s seconds ---" % (time.time() - start_time))
'''
#Drawing
canv.cd(1)
#t.Draw('ms_ds>>hDsn')
#hD_nocut.Draw()
hD.Draw('same&h')
hD.SetFillColor(ROOT.kCyan+3)
canv.cd(2)
hAngle.Draw()
'''

#a = ROOT.TLorentzVector(1,2,3,4)
#b =ROOT.TLorentzVector(2,3,4,5)
#print(a.Angle(b.Vect()))
#print(a.X())