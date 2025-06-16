'''
params.py

Managers of all hyper-parameters

'''
import glob
import torch

epochs = 250
batch_size = 64
soft_label = False
adv_weight = 0
d_thresh = 0.8
z_dim = 200
z_dis = "norm"
model_save_step = 10
g_lr = 0.00020
d_lr = 0.00001
beta = (0.5, 0.750)
cube_len = 128
leak_value = 0.2
bias = False


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
data_dir = '.../3D_Datasets/3d_lattice_binvox_128/'
output_dir = '.../outputs'
# images_dir = '../test_outputs'


def print_params():
    l = 16
    print(l * '*' + 'hyper-parameters' + l * '*')

    print('epochs =', epochs)
    print('batch_size =', batch_size)
    print('soft_labels =', soft_label)
    print('adv_weight =', adv_weight)
    print('d_thresh =', d_thresh)
    print('z_dim =', z_dim)
    print('z_dis =', z_dis)
    print('model_images_save_step =', model_save_step)
    print('data =', model_dir)
    print('device =', device)
    print('g_lr =', g_lr)
    print('d_lr =', d_lr)
    print('cube_len =', cube_len)
    print('leak_value =', leak_value)
    print('bias =', bias)

    print(l * '*' + 'hyper-parameters' + l * '*')

    print("cuda available: ", torch.cuda.is_available())

    print("device count: ",torch.cuda.device_count())

    print("active device: ",torch.cuda.current_device())

    print("device name: ", torch.cuda.get_device_name(0))

