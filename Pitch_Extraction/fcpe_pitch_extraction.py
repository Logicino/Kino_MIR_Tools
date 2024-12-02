from torchfcpe import spawn_bundled_infer_model
import torch
import librosa
import numpy as np

# Configure device and target hop size
device = 'cuda'  # or 'cuda' if using a GPU
sr = 16000  # Sample rate
hop_size = 160  # Hop size for processing

# Load and preprocess audio
audio, sr = librosa.load('/data/xyth/Dataset/stringquad/train/AlTardarDellaVendetta/Cello.wav', sr=sr)
audio = librosa.to_mono(audio)
audio_length = len(audio)
f0_target_length = (audio_length // hop_size) + 1
audio = torch.from_numpy(audio).float().unsqueeze(0).unsqueeze(-1).to(device)

# Load the model
model = spawn_bundled_infer_model(device=device)

# Perform pitch inference
f0 = model.infer(
    audio,
    sr=sr,
    decoder_mode='local_argmax',  # Recommended mode
    threshold=0.006,  # Threshold for V/UV decision
    f0_min=80,  # Minimum pitch
    f0_max=1100,  # Maximum pitch
    interp_uv=False,  # Interpolate unvoiced frames
    output_interp_target_length=f0_target_length,  # Interpolate to target length
)

print(f0)

pitch_numpy = f0.cpu().numpy()
# print(pitch_numpy[0].shape)

# 构建保存结果的文件名
result_file_name = "AlTardarDellaVendetta_Cello_f0.npy"

# 保存结果数组
np.save(result_file_name, pitch_numpy[0])

print("yes")