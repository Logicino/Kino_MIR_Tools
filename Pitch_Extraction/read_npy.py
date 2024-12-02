import numpy as np

dir = "/data/xyth/Dataset/stringquad/train/k458/Violin_1_f0_note_12_2d_1025.npy"
# dir = "/data/xyth/Dataset/stringquad/train/k458/Violin_2_f0_note_12_2d.npy"
data = np.load(dir)

data.astype(np.float64)
print(data.shape)
print(data.dtype)

# print(float_data.dtype)
