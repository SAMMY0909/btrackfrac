from __future__ import division

import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import namedtuple
from math import sqrt

Plot=namedtuple('Plot', ['container', 'varName', 'xName', 'xBins', 'yName', 'canvasName'])

Plots=[ Plot('tracks', 'truthOrigin', 'truthOrigin', np.arange(-0.5, 8.5, 1), 'Number of tracks', 'truthOrigin.png')
      ]

def getVal(fileName):
	# Open hdf5 file 
	with h5py.File(fileName,'r') as h5f:
    	#print('Jet variables:\n')
    	#print(h5f['jets'].dtype)
	
    	#print(h5f['jets'][0:21]['HadronConeExclTruthLabelID'])
    	#for i in range(0,21):
    	#	ntracks=len(h5f['tracks_from_jet'][i:(i+1),:]['truthOrigin'][h5f['tracks_from_jet'][i:(i+1),:]['truthOrigin'] > -1])
    	#	nTB=len(h5f['tracks_from_jet'][i:(i+1),:]['truthOrigin'][h5f['tracks_from_jet'][i:(i+1),:]['truthOrigin'] == 3])
    	#	nTB+=len(h5f['tracks_from_jet'][i:(i+1),:]['truthOrigin'][h5f['tracks_from_jet'][i:(i+1),:]['truthOrigin'] == 4])
    	#	isB=(h5f['jets'][i]['HadronConeExclTruthLabelID'] == 5)
    	#	#print(f"Jet {i} - isb = {isB} - ntracks = {ntracks} , nTr_FromB = {nTB}")
	
		jetlist=h5f['jets'][0:162586]
		locbjets=[i for i,x in enumerate(jetlist) if x['HadronConeExclTruthLabelID']==5]
		nbjets=len(locbjets)
		tracksInBJets=[h5f['tracks_from_jet'][i]['truthOrigin'][h5f['tracks_from_jet'][i]['truthOrigin'] > -1] for i in locbjets]
		btracksInBJets=[h5f['tracks_from_jet'][i]['truthOrigin'][(h5f['tracks_from_jet'][i]['truthOrigin'] == 5)] for i in locbjets]
		ptbjets=[h5f['jets'][i]['pt_btagJes']*0.001 for i in locbjets]
    	#print(locbjets)
    	#print(nbjets)
    	#print(tracksInBJets)
    	#print(btracksInBJets)
	
		ptbins=[0., 25., 50., 75., 100., 150., 300., 500.,750., 1000.,1500., 2000.,2500., 3000.,3500.,4000.]
		njetsBinI=[0]*(len(ptbins)-1)
		njetsBinI0B=[0]*(len(ptbins)-1)
	
		for i in range(0, nbjets):
			print(f"{locbjets[i]} , nT = {len(tracksInBJets[i])} , nBT = {len(btracksInBJets[i])} , pT = {ptbjets[i]}")
			for binN, val in enumerate(ptbins):
				if ptbjets[i] > val:
					continue
				else:
					njetsBinI[binN-1] += 1
					if len(btracksInBJets[i]) == 0:
						njetsBinI0B[binN-1] += 1
					break
	
		print(ptbins)
		print(njetsBinI)
		print(njetsBinI0B)	 
		frac=[100.*float(i)/float(j) if j > 0 else 0 for i, j in zip(njetsBinI0B, njetsBinI)]
		fracErr=[ 100.*sqrt(((float(i)/float(j))*(1.-float(i)/float(j)))/float(j)) if j > 0 else 0 for i, j in zip(njetsBinI0B, njetsBinI) ]
		print(frac)	
		return ptbins, frac, fracErr	
#combined_DIPS_loose.h5  standard_DIPS_loose.h5
#combined_LRT_loose.h5   standard_LRT_loose.h5

ptbins_sDL, frac_sDL, fracErr_sDL = getVal('standard_DIPS_loose.h5')
ptbins_cDL, frac_cDL, fracErr_cDL = getVal('combined_DIPS_loose.h5')
ptbins_sLL, frac_sLL, fracErr_sLL = getVal('standard_LRT_loose.h5')
ptbins_cLL, frac_cLL, fracErr_cLL = getVal('combined_LRT_loose.h5')


plt.errorbar(ptbins_sDL[0:-1], frac_sDL, fracErr_sDL, label='DIPS Loose STD')
plt.errorbar(ptbins_cDL[0:-1], frac_cDL, fracErr_cDL, label='DIPS Loose STD+LRT')

plt.errorbar(ptbins_sLL[0:-1], frac_sLL, fracErr_sLL, label='LRT Loose STD')
plt.errorbar(ptbins_cLL[0:-1], frac_cLL, fracErr_cLL, label='LRT Loose STD+LRT')

plt.xscale('log')
plt.xlim(30., 4000.)
plt.xlabel(r'$p_T$ [GeV]')
plt.ylabel('frac. b-jets with 0 b-tracks [%]')
plt.legend()
plt.savefig('hist.png')
	
plt.xscale('linear')
plt.savefig('hist_linear.png')
