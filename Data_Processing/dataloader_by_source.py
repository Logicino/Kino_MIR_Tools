import json
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import math
from torch.utils import data
import sys
import torchaudio
import re
from torch.utils.data import DataLoader


class CadenzaDataset(data.Dataset):
    def __init__(
        self,
        root_path,
        music_tracks_file,
        segment_length=5.0,
        split: str="train",
        sample_rate=44100,
        shift=1.0, 
    ):
        
        self.root_path = Path(root_path)

        self.music_tracks_file = Path(music_tracks_file)  # json文件的地址
        self.segment_length = segment_length
        self.sample_rate = sample_rate
        self.shift = shift

        ## label_info
        instrument_list = ['Bassoon', 'Clarinet', 'Flute', 'Oboe', 'Sax', 'Cello', 'Viola', 'Violin']

        with open(self.music_tracks_file) as f:
            self.tracks = json.load(f)   # self.tracks的值就是json，包括了所有的参数

        self.tracks_list = list(self.tracks.keys())  # self.track_list是json中所有歌曲的名字

        self.num_examples = []   # 用于记录：每个分轨有多少个样本
        self.example_to_track = []   # 用于记录每个样本对应的歌曲名字
        self.example_to_ins_index = []   # 用于记录每个分轨对应的ins标签
        self.example_to_pos_index = []   # 用于记录每个分轨对应的pos标签

        for track_name, sources in self.tracks.items():
            num_sources = 0  # 初始化source数量计数器

            # 统计当前歌曲的source数量
            for source_name in sources:
                if source_name.startswith("source"):
                    num_sources += 1

            # 处理每个source
            for source_name, source_info in sources.items():
                if source_name.startswith("source"):
                    track_duration = source_info["duration"]
                    
                    examples = int(math.ceil((track_duration - self.segment_length) / self.shift) + 1)   # 每首歌曲能裁出来的片段数，这里的单位是秒(s)

                    instrument_prefix = source_info['instrument'].split('_')[0]  # 对重复乐器的_1 _2进行去重

                    source_index = source_name.split('_')[-1]

                    pos_index = self.find_pos_index(num_sources=num_sources, source_index=source_index)
                    
                    self.num_examples.append(examples)  # 这里是一个数组，记录了每个歌曲里面有多少个片段
                    self.example_to_track.append(source_info['track'])   # 记录了这个example对应的track地址
                    self.example_to_ins_index.append(instrument_list.index(instrument_prefix))
                    self.example_to_pos_index.append(pos_index)
            
    def __len__(self):
        return sum(self.num_examples)
    
    def __getitem__(self, index):
        for examples, track_dir, ins, pos in zip(self.num_examples, self.example_to_track, self.example_to_ins_index, self.example_to_pos_index):  # name：歌曲名字，examples：这首歌曲的采样片段数
            # print("name, examples", track_name, examples)
            # 用全局index来查询在哪一首歌曲里
            if index >= examples:
                index -= examples
                continue

            ### 读取分轨和mixture
            # 分轨的：track_dir
            # mixture的：track_dir改一下
            mixture_dir = re.sub(r'/[^/]+\.flac$', '/mix_Mix_1.flac', track_dir)
            # 用采样率和时间换算，找到采样的位置
            segment_samples = int(self.segment_length * self.sample_rate)   # 裁剪片段长度
            shift_samples = int(self.shift * self.sample_rate)

            start_sample = int(index * shift_samples)   # 开始的sample点位置
            end_sample = start_sample + segment_samples   # 结束的sample点位置

            source_audio_path = self.root_path / track_dir
            mixture_audio_path = self.root_path / mixture_dir

            source_audio, sr = torchaudio.load(Path(source_audio_path), frame_offset=end_sample, num_frames=segment_samples)
            mixture_audio, sr = torchaudio.load(Path(mixture_audio_path), frame_offset=end_sample, num_frames=segment_samples)

            return source_audio, mixture_audio, ins, pos
 

    def find_pos_index(self, num_sources, source_index):
        '''
        num_sources： 一共有多少个sources
        source_index：是第几个source
        '''
        num_sources = int(num_sources)
        source_index = int(source_index)

        if num_sources == 2:
            if source_index == 1:
                return 4
            if source_index == 2:
                return 6
        if num_sources == 3:
            if source_index == 1:
                return 3
            if source_index == 2:
                return 5
            if source_index == 3:
                return 7
        if num_sources == 4:
            if source_index == 1:
                return 2
            if source_index == 2:
                return 4
            if source_index == 3:
                return 6
            if source_index == 4:
                return 8
        if num_sources == 5:
            if source_index == 1:
                return 1
            if source_index == 2:
                return 3
            if source_index == 3:
                return 5
            if source_index == 4:
                return 7
            if source_index == 5:
                return 9
        

def collate_fn(batch):
    # batch是一个列表，其中包含了多个(mixture, ilens, final_sources)元组
    mixtures, ilens, sources = zip(*batch)  # 解压批次数据

    '''
    mixtures: 
        tuple, (tensor([-0.0057, -0.0071, -0.0084,  ...,]), tensor([0., 0., 0.,  ...,]), ...)
    ilens: 
        tuple, (441000, 441000, 441000, ...)
    sources:
        tuple, (tensor([[5.7220e-03,  6.2256e-03,  6.8817e-03,  ...,], [ 2.9144e-03,  3.0975e-03,  3.1433e-03,  ..., ], ...]), tensor([[5.7220e-03,  6.2256e-03,  6.8817e-03,  ...,], [ 2.9144e-03,  3.0975e-03,  3.1433e-03,  ..., ], ...]))
        从外到里：batch，每首歌
    '''
    # print("mixtures", mixtures)
    # print("ilens", ilens)
    # print("sources", sources)

    batch_size = len(sources)
    # print(sources[0].shape[0])  # number of sources

    # 找到有最多分轨的分轨数量
    max_num_of_sources = 0
    for i in range(batch_size):
        if (sources[i].shape[0] > max_num_of_sources):
            max_num_of_sources = sources[i].shape[0]

    # print(max_num_of_sources)

    # 对mixtures进行填充（？）mixtures不需要填充
    # 将tuple转为list
    mixtures = list(mixtures)
    ilens = list(ilens)
    sources = list(sources)
    # print("mixtures", mixtures)

    # 对final_sources进行填充
    for i in range(batch_size):
        # 如果这首歌的sources数量，比最大的sources数量小的话，进行填充
        if (sources[i].shape[0] < max_num_of_sources):
            source_to_be_pad_num = max_num_of_sources - sources[i].shape[0]
            paddings = torch.zeros(source_to_be_pad_num, ilens[0])  # 按缺的轨道数目、序列长度填充
            sources_to_be_pad = sources[i]
            # print("source[i]", sources[i])
            sources_padded = torch.vstack((sources_to_be_pad, paddings))
            # print("sources_padded", sources_padded)

            sources[i] = sources_padded

    mixtures_tensor = torch.stack(mixtures)
    ilens_tensor = torch.tensor(ilens)
    sources_tensor = torch.stack(sources)

    return mixtures_tensor, ilens_tensor, sources_tensor

if __name__ == "__main__":
    _root_path = Path(
        "/data/xyth/Dataset/Stereo_Reverb_EnsembleSet"
    )
    _music_tracks_file = Path(
        "/data/xyth/Kino_MIR_Tools/Data_Processing/tracks_info.json"
    )
    dataset = CadenzaDataset(
        _root_path,
        _music_tracks_file,
        split="train",
        segment_length=3.0,
        shift = 2.0,
    )
    # print(len(dataset))
    # print(dataset.num_examples)
    # print(len(dataset.num_examples))  # 分轨的个数总和
    # print(sum(dataset.num_examples))   # 总共切片数量
    # print(dataset.example_to_ins_index)   # 乐器表
    # print(len(dataset.example_to_ins_index))
    # print(len(dataset.example_to_track))
    # print(dataset.example_to_pos_index)
    # print(len(dataset.example_to_pos_index))
    # print(len(dataset.example_to_ins_index))   ## instrument检测完毕

    data_loader = DataLoader(dataset, batch_size=10, shuffle=False)  # 假设批量大小为4

    print(data_loader)
    for batch_idx, (source_audio, mixture_audio, ins, pos) in enumerate(data_loader):
        print(batch_idx)

        print(source_audio)
        print("mixed_signal", mixture_audio)
        print(ins)
        print(pos)

        print("hw")
        sys.exit(-1)