from __future__ import division
import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import namedtuple
from math import sqrt

fileName='combined_DIPS_loose.h5'
Bins = {"truthOrigin" : np.arange(0,26,1)}
with h5py.File(fileName,'r') as h5f:
    jetlist=h5f['jets'][:]
    locbjets=[i for i,x in enumerate(jetlist) if x['HadronConeExclTruthLabelID']==5]
    njets=len(locbjets)
    tracksInBJets=np.array([h5f['tracks_from_jet'][i]['truthOrigin'][h5f['tracks_from_jet'][i]['truthOrigin'] > -1] for i in locbjets],dtype=object)
    tracksInBJets=np.concatenate(tracksInBJets)
    tracksInBJets=tracksInBJets.astype(int)
    print("Shape of the tracks item is: ", tracksInBJets.shape)
    plt.style.use('ggplot')
    plt.hist(tracksInBJets,bins=Bins['truthOrigin'],histtype='stepfilled',label="Truth Origin Distribution \n for tracks corr to b-jets")
    plt.xlabel('truthOrigin',fontsize=10)
    plt.ylabel(f"Track truthOrigin Distribution \n for {njets} b-jets",fontsize=10)
    plt.legend(loc='upper right',fontsize=10)
    plt.subplots_adjust(bottom=.25, left=.25)
    plt.savefig("truthOriginDist.png")


