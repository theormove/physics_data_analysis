import ROOT
import numpy
import time

#Initializing 

f = ROOT.TFile("../DstDst0_9modes.root")

t  = f.Get("dsc_k03p")

start_time = time.time()

events = t.GetEntries()

hD = ROOT.TH1F('hDs','D*^{+}',100,2.006,2.014)
hK_nocut = ROOT.TH1F('hKnc','K^{0}_{s} Candidates;M(K^{0}_{s});Counts',100,0.48,0.52)
hD_nocut = ROOT.TH1F('hDnc','D*^{+} Candidates;M(D*^{+});Counts',100,2.006,2.014)
#t.Draw('ms_ds>>hDnc')
hK = ROOT.TH1F('hK','K^{0}_{S}',100,0.48,0.52)
canv = ROOT.TCanvas("canvDs","histogram",1300,500)
hAngle = ROOT.TH1F('angl','Angle',100,0.0,4)
canv.Divide(1,1)

#Setting cuts 

angle_cut = 0.1

min_dist = 0.5



ms_d0_min = 1.85
ms_d0_max = 1.88
ms_ds_max = 2.014

#Go over all events
for i in range(events):
	t.GetEntry(i)

	# розташування частинок
	k0_pos = ROOT.TVector3(t.vx_k0,t.vy_k0,t.vz_k0)
	d0_pos = ROOT.TVector3(t.vx_d0,t.vy_d0,t.vz_d0)
	
	k0_vect = ROOT.TVector3()
	d0_vect = ROOT.TVector3()
	# імпульс  
	k0_vect.SetMagThetaPhi(1,t.th_k0,t.ph_k0)
	d0_vect.SetMagThetaPhi(1,t.th_d0,t.ph_d0)
	# відстань
	dist_vect = k0_pos-d0_pos
	dist = dist_vect.Mag()
	# кут 
	angle = k0_vect.Angle(dist_vect)  
	
	hAngle.Fill(angle)

	if (angle < angle_cut) and (dist>min_dist):		
		hK.Fill(t.ms_k0)
		hAngle.Fill(angle)	


print("--- %s seconds ---" % (time.time() - start_time))

#Drawing


t.Draw('ms_k0>>hKnc')
canv.cd(1)
hK_nocut.SetMinimum(0)
hK_nocut.Draw()
hK.Draw('same&h')
hK.SetFillColor(ROOT.kCyan+3)
legend =  ROOT.TLegend(0.1,0.7,0.48,0.9)
legend.AddEntry('hKnc',"All")
legend.AddEntry('hK',"Filtered")
legend.Draw()


#hAngle.Draw()
'''
canv.cd(1)
hD_nocut.SetMinimum(0)
hD_nocut.Draw()
hD.Draw('same&h')
hD.SetFillColor(ROOT.kCyan+3)
legend =  ROOT.TLegend(0.1,0.7,0.48,0.9)
legend.SetHeader("Candidates")
legend.AddEntry('hDnc',"All")
legend.AddEntry('hDs',"Filtered")
legend.Draw()
'''

