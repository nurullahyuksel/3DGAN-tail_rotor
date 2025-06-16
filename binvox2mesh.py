import numpy as np
import trimesh # for converting voxel grids to meshes (to import objects into simulators)
import time # to know how long it takes for the code to run
import os # to walk through directories, to rename files
import sys
import glob

import binvox_rw # to manipulate binvox files

# Parses a file of type BINVOX
# Returns a voxel grid, generated using the binvox_rw.py package


binvox_saved_path = ".../outputs/dcgan/first_test/test_outputs/test_binvox"
mesh_saved_path=  binvox_saved_path +".../mesh_samples"
filename= binvox_saved_path+ ".../01.binvox"


if not os.path.exists(mesh_saved_path):
    os.makedirs(mesh_saved_path)



def parse_BINVOX_file_into_voxel_grid(filename):
    filereader = open(filename, 'rb')
    binvox_model = binvox_rw.read_as_3d_array(filereader)
    voxelgrid = binvox_model.data
    return voxelgrid

print("Usage: ")
print("python binvox2mesh.py <FILEPATH>")


 
for i in range(30):
    # Load the voxelgrid from file
    binvox_file=glob.glob(binvox_saved_path + "/{:02d}.binvox".format(i))
    
    file= binvox_file[0]

    voxelgrid = parse_BINVOX_file_into_voxel_grid(file)


    # Generate a folder to store the images

    """
    print("Generating a folder to save the mesh")
    directory = "..."
    if not os.path.exists(directory):
        os.makedirs(directory)
    """

    mesh = trimesh.voxel.ops.matrix_to_marching_cubes(
        matrix=voxelgrid,
        pitch=1.0)
    
    print("Merging vertices closer than a pre-set constant...")
    mesh.merge_vertices()
    print("Removing duplicate faces...")
    mesh.remove_duplicate_faces()
    print("Scaling...")
    mesh.apply_scale(scaling=1.0)
    print("Making the mesh watertight...")
    trimesh.repair.fill_holes(mesh)
    print("Fixing inversion and winding...")
    trimesh.repair.fix_inversion(mesh)
    trimesh.repair.fix_winding(mesh)




    print("Generating the STL mesh file {:02d}".format(i+1))
    trimesh.exchange.export.export_mesh(
        mesh=mesh,
        file_obj=mesh_saved_path + "/{:02d}.stl".format(i),
        file_type="stl"
        )
    



