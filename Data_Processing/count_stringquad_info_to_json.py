### 根据数据集，生成json信息

import os
import json
import mutagen  # 需要安装mutagen库来读取flac文件信息
import sys

# 定义根目录
# ROOT_DIR = "/data/xyth/Dataset/My_Final_Dataset_s1r2/Remixed"
# ROOT_DIR = "/data/xyth/Dataset/stringqud_reverb_shuffle"
# ROOT_DIR = "/data/xyth/Dataset/stringqud_reverb_two_seating"
# ROOT_DIR = "/data/xyth/Dataset/URMP_test_set"
ROOT_DIR = "/data/xyth/Dataset/stringquad_reverb_2seating_for_validation"

# 初始化JSON数据结构
data = {}

def process_Remixed():
    # 遍历根目录下的所有歌曲文件夹
    for song_dir in os.listdir(ROOT_DIR):
        song_path = os.path.join(ROOT_DIR, song_dir)
        
        # 确保是文件夹
        if os.path.isdir(song_path):
            # mix_1_path = os.path.join(song_path, "Mix_1")
            mix_1_path = song_path
            print(mix_1_path)
            
            # 检查Mix_1文件夹是否存在
            if os.path.exists(mix_1_path):
                sources = {}
                mixture = {}
                duration = 0
                
                print(os.listdir(mix_1_path))
                res = os.listdir(mix_1_path)
                res.sort()   ## Very very important!
                print(res)
                
                # 列出Mix_1文件夹中的所有.flac文件
                for flac_file in os.listdir(mix_1_path):
                    
                    if flac_file.endswith('.wav'):
                        flac_path = os.path.join(mix_1_path, flac_file)
                        # 使用mutagen读取flac文件信息
                        print("filepath", flac_path)
                        audio = mutagen.File(flac_path)
                        if duration == 0:  # 如果duration还未设置，则计算一次
                            duration = round(audio.info.length, 2)  # 四舍五入到两位小数
                        
                        # if flac_file == 'mix_Mix_1.flac':
                        if flac_file.startswith("mix")==True:
                            mixture = {
                                "instrument": "Mixture",
                                "track": os.path.join(song_dir, flac_file),
                                "start": 0,
                                "duration": duration
                            }
                        else:
                            # 假设文件名格式为 Instrument.flac，从中提取乐器名称
                            instrument = flac_file.replace('.flac', '')
                            sources[f"source_{len(sources) + 1}"] = {
                                "instrument": instrument,
                                "track": os.path.join(song_dir, flac_file),
                                "start": 0,
                                "duration": duration
                            }
                # sys.exit(-1)
                # 将分轨和混合音频添加到JSON数据结构中
                data[song_dir] = {**sources, "mixture": mixture}

    # 将JSON数据写入文件
    with open('tracks_info.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


process_Remixed()
print("JSON file has been created.")