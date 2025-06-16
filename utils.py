
'''
utils.py

Some utility functions

'''

import scipy.ndimage as nd
import scipy.io as io
import matplotlib
import params
import glob

if params.device.type != 'cpu':
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
import skimage.measure as sk
from mpl_toolkits import mplot3d
import matplotlib.gridspec as gridspec
import numpy as np
from torch.utils import data
from torch.autograd import Variable
import torch
import os
import pickle
import binvox_rw



def load_binvox_data(file_path):
    with open(file_path, 'rb') as f:
        model = binvox_rw.read_as_3d_array(f)
        data = model.data.astype(np.float32)
        data = np.expand_dims(data, axis=-1)
        return data
    
def write_binvox(data, path):
    """
    write out voxel data
    """
    data = np.rint(data).astype(np.uint8)
    dims = data.shape
    translate = [0., 0., 0.]
    scale = 1.0
    axis_order = 'xyz'
    v = binvox_rw.Voxels( data, dims, translate, scale, axis_order)

    with open(path, 'bw') as f:
        v.write(f)



def getVoxelFromMat(path, cube_len=64):
    if cube_len == 32:
        voxels = io.loadmat(path)['instance'] # 30x30x30
        voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))

    else:
        # voxels = np.load(path) 
        # voxels = io.loadmat(path)['instance'] # 64x64x64
        # voxels = np.pad(voxels, (2, 2), 'constant', constant_values=(0, 0))
        # print (voxels.shape)
        voxels = io.loadmat(path)['instance'] # 30x30x30
        voxels = np.pad(voxels, (1, 1), 'constant', constant_values=(0, 0))
        voxels = nd.zoom(voxels, (2, 2, 2), mode='constant', order=0)
        # print ('here')
    # print (voxels.shape)
    return voxels


def getVFByMarchingCubes(voxels, threshold=0.5):
    v, f = sk.marching_cubes_classic(voxels, level=threshold)
    return v, f


def plotVoxelVisdom(voxels, visdom, title):
    v, f = getVFByMarchingCubes(voxels)
    visdom.mesh(X=v, Y=f, opts=dict(opacity=0.5, title=title))


def SavePloat_Voxels(voxels, path, iteration):
    voxels = voxels[:8].__ge__(0.5)
    fig = plt.figure(figsize=(32, 16))
    gs = gridspec.GridSpec(2, 4)
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(voxels):
        x, y, z = sample.nonzero()
        ax = plt.subplot(gs[i], projection='3d')
        ax.scatter(x, y, z, zdir='z', c='cyan', edgecolors="black")
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        # ax.set_aspect('equal')
    # print (path + '/{}.png'.format(str(iteration).zfill(3)))
    plt.savefig(path + '/{}.png'.format(str(iteration).zfill(3)), bbox_inches='tight')
    plt.close()


class ShapeNetDataset(data.Dataset):

    def __init__(self, root, args, train_or_val="train"):
        
        
        self.root = root
        self.listdir = os.listdir(self.root)
        # print (self.listdir)  
        # print (len(self.listdir)) # 10668

        data_size = len(self.listdir)
#        self.listdir = self.listdir[0:int(data_size*0.7)]
        self.listdir = self.listdir[0:int(data_size)]
        
        print ('data_size =', len(self.listdir)) # train: 10668-1000=9668
        self.args = args

    def __getitem__(self, index):
        with open(self.root + self.listdir[index], "rb") as f:
            volume = np.asarray(getVoxelFromMat(f, params.cube_len), dtype=np.float32)
            # print (volume.shape)
        return torch.FloatTensor(volume)

    def __len__(self):
        return len(self.listdir)


def generateZ(args, batch):

    if params.z_dis == "norm":
        Z = torch.Tensor(batch, params.z_dim).normal_(0, 0.33).to(params.device)
    elif params.z_dis == "uni":
        Z = torch.randn(batch, params.z_dim).to(params.device).to(params.device)
    else:
        print("z_dist is not normal or uniform")

    return Z
