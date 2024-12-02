### use environment py37
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import librosa
import os
from scipy.interpolate import interp1d
import torchcrepe

# 根目录路径
file_path = '/data/xyth/Dataset/stringquad/train/AlTardarDellaVendetta/Cello.wav'

audio, sr = torchcrepe.load.audio(file_path)
print(audio.shape)
print(audio[0].shape)
### For Stereo
# audio_mono = ((audio[0].permute(1,0)[0] + audio[0].permute(1,0)[1])/2).unsqueeze(0)  # 处理双通道音频
audio_mono = (audio[0] + audio[1]) / 2  # 处理双通道音频
audio_mono = audio_mono.unsqueeze(0)
hop_length = 1024

fmin = 60
fmax = 1200

# Select a model capacity--one of "tiny" or "full"
model = 'full'

# Choose a device to use for inference
device = 'cuda:1'

# Pick a batch size that doesn't cause memory errors on your gpu
batch_size = 2048


# Compute pitch using first gpu
pitch = torchcrepe.predict(audio_mono,
                        sr,
                        hop_length,
                        fmin,
                        fmax,
                        model,
                        batch_size=batch_size,
                        device=device)

pitch_numpy = pitch.cpu().numpy()
# print(pitch_numpy[0].shape)

# 构建保存结果的文件名
result_file_name = "AlTardarDellaVendetta_Cello_f0.npy"

# 保存结果数组
np.save(result_file_name, pitch_numpy[0])

print("yes")

