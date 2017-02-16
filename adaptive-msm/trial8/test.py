from glob import glob
import mdtraj as md
from os.path import join
import tempfile
import os
from msmbuilder.dataset import dataset
import argparse
from msmbuilder.featurizer import DihedralFeaturizer

from msmbuilder.preprocessing import RobustScaler
from msmbuilder.decomposition import tICA

import msmexplorer as msme
import numpy as np

from msmbuilder.cluster import MiniBatchKMeans
from matplotlib import pyplot as plt

from msmbuilder.msm import MarkovStateModel
from msmbuilder.utils import dump

from msmbuilder.lumping import PCCAPlus


if __name__ == '__main__':


    xyz = dataset("iter2/*.nopbc.xtc", topology='iter2/reference_0.pdb', stride=2)

    # The raw (x, y, z) coordinates from the simulation do not respect the translational 
    # and rotational symmetry of our problem. A Featurizer transforms cartesian 
    # coordinates into other representations. Here we use the DihedralFeaturizer to turn 
    # our data into phi and psi dihedral angles.
    featurizer = DihedralFeaturizer(types=['phi', 'psi'])
    diheds = xyz.fit_transform_with(featurizer, 'diheds/', fmt='dir-npy')


    # Since the range of values in our raw data can vary widely from feature to feature, 
    # we can scale values to reduce bias. Here we use the RobustScaler to center and 
    # scale our dihedral angles by their respective interquartile ranges.
    scaler = RobustScaler()
    scaled_diheds = diheds.fit_transform_with(scaler, 'scaled_diheds/', fmt='dir-npy')

    # Intermediate kinetic model: tICA
    # tICA is similar to principal component analysis
    tica_model = tICA(lag_time=2, n_components=4)
    # fit and transform can be done in seperate steps:
    tica_model = scaled_diheds.fit_with(tica_model)
    tica_trajs = scaled_diheds.transform_with(tica_model, 'ticas/', fmt='dir-npy')

    # Conformations need to be clustered into states (sometimes written as microstates). 
    # We cluster based on the tICA projections to group conformations that interconvert 
    # rapidly. Note that we transform our trajectories from the n_components-dimensional 
    # tICA space into a 1-dimensional cluster index
    txx = np.concatenate(tica_trajs)
    #_ = msme.plot_histogram(txx)
    clusterer = MiniBatchKMeans(n_clusters=100, random_state=42)
    clustered_trajs = tica_trajs.fit_transform_with(clusterer, 'kmeans/', fmt='dir-npy')
    plt.hexbin(txx[:,0], txx[:,1], bins='log', mincnt=1, cmap='viridis')
    plt.scatter(clusterer.cluster_centers_[:,0], clusterer.cluster_centers_[:,1], s=100, c='w')
    plt.savefig('microstate_clusters.png')

    # We can construct an MSM from the labeled trajectories
    msm = MarkovStateModel(lag_time=10, n_timescales=20)
    msm.fit(clustered_trajs)
    assignments = clusterer.partial_transform(txx)
    assignments = msm.partial_transform(assignments)
    #print max(assignments[0])
    #print type(assignments[0])
    #print assignments[0]
    #print msm.transmat_
    #print type(msm.transmat_)
   
    ''' 
    msme.plot_free_energy(txx, obs=(0, 1), n_samples=10000,
                      pi=msm.populations_[assignments],
                      xlabel='tIC 1', ylabel='tIC 2')
    plt.scatter(clusterer.cluster_centers_[msm.state_labels_, 0],
            clusterer.cluster_centers_[msm.state_labels_, 1],
            s=1e4 * msm.populations_,       # size by population
            c=msm.left_eigenvectors_[:, 1], # color by eigenvector
            cmap="coolwarm",
            zorder=3)
    plt.colorbar(label='First dynamical eigenvector')
    plt.tight_layout()
    #plt.figure()
    plt.savefig('free_energy_plot.png')
    print assignments
    # Macrostate model
    pcca = PCCAPlus.from_msm(msm, n_macrostates=4)
    macro_trajs = pcca.transform(clustered_trajs)

    print macro_trajs
    #print type(macro_trajs)
    print dir(pcca)
    print len(macro_trajs[0])

    
    msme.plot_free_energy(txx, obs=(0, 1), n_samples=10000,
                      pi=msm.populations_[assignments],
                      xlabel='tIC 1', ylabel='tIC 2')
    plt.scatter(clusterer.cluster_centers_[msm.state_labels_, 0],
            clusterer.cluster_centers_[msm.state_labels_, 1],
            s=50,
            c=pcca.microstate_mapping_,
            zorder=3
           )
    plt.tight_layout()
    plt.savefig('macrostate_clusters.png')
    ''' 
