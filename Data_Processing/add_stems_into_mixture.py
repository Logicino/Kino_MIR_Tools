import os
import soundfile as sf
import numpy as np
import sys

# 定义根目录
# root_dir = '/data/xyth/Dataset/My_Final_Dataset_s1r2/CadenzaWoodwind_clipped_Reverb'
root_dir = "/data/xyth/Dataset/My_Final_Dataset_s1r2/CadenzaWoodwind_clipped_no_Reverb"

# 遍历根目录下的所有文件夹
for subdir, dirs, files in os.walk(root_dir):
    # print("subdir", subdir)
    # print("dirs", dirs)
    # print("files", files)
    # 确保当前目录是子文件夹
    if subdir != root_dir:
        print("subdir", subdir)
        # 获取当前子文件夹中的所有.flac文件
        flac_files = [f for f in files if f.endswith('.flac')]
        # print("flac_file", flac_files)
        
        if flac_files:
            # 读取第一个文件以获取采样率和初始数据
            first_file_path = os.path.join(subdir, flac_files[0])
            first_audio, sr = sf.read(first_file_path)
            mix_audio = np.zeros_like(first_audio, dtype=np.float64)
            
            # sys.exit(-1)
            # 将所有.flac文件相加
            for flac_file in flac_files:
                file_path = os.path.join(subdir, flac_file)
                audio, _ = sf.read(file_path)
                mix_audio += audio
            
            # 保存混合后的音频文件
            mix_file_path = os.path.join(subdir, 'mix_Mix_1.flac')
            sf.write(mix_file_path, mix_audio, samplerate=sr)
            print(f"Saved mixed file: {mix_file_path}")

print("All mix files generated successfully.")