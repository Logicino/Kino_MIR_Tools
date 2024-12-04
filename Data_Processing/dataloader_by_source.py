import json
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import math
from torch.utils import data
import sys
import torchaudio
from torch.utils.data import DataLoader


class CadenzaDataset(data.Dataset):
    def __init__(
        self,
        root_path,
        music_tracks_file,
        segment_length = 5.0,
        split: str = "train",
        sample_rate=44100,
        shift = 1.0, 
    ):
        
        self.root_path = Path(root_path)

        # if split == "train":
        #     self.root_path = root_path / "train"

        self.music_tracks_file = Path(music_tracks_file)  # json文件的地址
        self.segment_length = segment_length
        # self.split = split
        self.sample_rate = sample_rate
        self.shift = shift

        ## label_info
        instrument_list = ['Basson', 'Clarinet', 'Flute', 'Oboe', 'Sax', 'Cello', 'Viola', 'Violin']

        with open(self.music_tracks_file) as f:
            self.tracks = json.load(f)   # self.tracks的值就是json，包括了所有的参数

        self.tracks_list = list(self.tracks.keys())  # self.track_list是json中所有歌曲的名字

        self.num_examples = []   # 用于记录：每个分轨有多少个样本
        self.example_to_track = []   # 用于记录每个样本对应的歌曲名字
        self.example_to_ins_index = []   # 用于记录每个分轨对应的ins标签
        self.example_to_pos_index = []   # 用于记录每个分轨对应的pos标签

        '''
        source_info {'instrument': 'Oboe', 'track': '02-lamortdase-strings/Mix_1/Oboe.flac', 'start': 0, 'duration': 249.0}
        '''

        for track_name, sources in self.tracks.items():
            for source_name, source_info in sources.items():
                source_num = 0

                if source_name.startswith("source"):
                    source_num += 1
                    # print(source_name)
                    track_duration = source_info["duration"]
                    
                    examples = int(math.ceil((track_duration - self.segment_length) / self.shift) + 1)   # 每首歌曲能裁出来的片段数，这里的单位是秒(s)

                    instrument_prefix = source_info['instrument'].split('_')[0]

                    source_index = source_name.split('_')[-1]

                    pos_index = self.find_pos_index(num_sources=, source_index=source_index)
                    
                    self.num_examples.append(examples)  # 这里是一个数组，记录了每个歌曲里面有多少个片段
                    self.example_to_track.append(source_info['track'])
                    self.example_to_ins_index.append(instrument_prefix)
                    self.example_to_pos_index.append(pos_index)

            

    def __len__(self):
        return sum(self.num_examples)
    
    def __getitem__(self, index):
        for track_name, examples in zip(self.tracks, self.num_examples):  # name：歌曲名字，examples：这首歌曲的采样片段数
            # print("name, examples", track_name, examples)
            # 用全局index来查询在哪一首歌曲里
            if index >= examples:
                index -= examples
                continue

            track_data = self.tracks[track_name]  # 找到目标歌曲的轨道信息
            # 找歌曲的对应的分轨，还有mixture
            # 用采样率和时间换算，找到采样的位置
            segment_samples = int(self.segment_length * self.sample_rate)   # 裁剪片段长度
            shift_samples = int(self.shift * self.sample_rate)

            start_sample = int(index * shift_samples)   # 开始的sample点位置
            end_sample = start_sample + segment_samples   # 结束的sample点位置
            
            wavs = []
            total_track_numbers = 0
            setting_track_numbers = 0

            # 统计有多少个轨道
            # for source_name, source_data in track_data.items():
            #     if source_name != "mixture":
            #         total_track_numbers += 1

            for source_name, source_data in track_data.items():    # 循环每个轨道
                if source_name == "mixture":
                    audio_path = self.root_path / source_data['track']
                    audio, sr = torchaudio.load(Path(audio_path), frame_offset=end_sample, num_frames=segment_samples)

                    if audio.size(1) < segment_samples:
                        padding = torch.zeros(audio.size(0), segment_samples - audio.size(1))
                        audio = torch.cat((audio, padding), dim=1)

                    audio = (audio[0] + audio[1])/2  # 转换为单通道
                    
                    mixture = audio
                    ilens = mixture.shape[0]
                    # print(ilens)

                if source_name != "mixture":
                    audio_path = self.root_path / source_data['track']
                    audio, sr = torchaudio.load(Path(audio_path),frame_offset=start_sample, num_frames=segment_samples)

                    # 如果音频长度不够，用零填充
                    if audio.size(1) < segment_samples:
                        padding = torch.zeros(audio.size(0), segment_samples - audio.size(1))
                        audio = torch.cat((audio, padding), dim=1)

                    audio = (audio[0] + audio[1])/2 # 转换为单通道
                    # TODO：增加panning代码   
                    wavs.append(audio)
                    setting_track_numbers = setting_track_numbers + 1

            # while setting_track_numbers < 5:
            #     empty_track = torch.zeros(2, segment_samples)
            #     wavs.append(empty_track)
            #     setting_track_numbers = setting_track_numbers + 1

            # 查看一下wavs里面每个元素的大小
            # for i, wav in enumerate(wavs):
            #     print(f"wavs[{i}] size: {wav.size()}")

            # total_track_numbers = 0

            # final_sources = torch.cat(wavs)  # return: [bs, 10, 44100]
            final_sources = torch.stack(wavs)  # return: [bs, 5, 2, 44100]

            # if final_sources.size(0) != 5:
            #     print("name", track_name)  # 找到的歌曲名字

            return mixture, ilens, final_sources

    def find_pos_index(self, num_sources, source_index):
        '''
        num_sources： 一共有多少个sources
        source_index：是第几个source
        '''

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
    print(len(dataset))
    print(dataset.num_examples)
    # print(len(dataset.num_examples))  # 分轨的个数总和
    # print(sum(dataset.num_examples))   # 总共切片数量
    # print(dataset.example_to_ins_index)   # 乐器表
    # print(len(dataset.example_to_ins_index))
    # print(len(dataset.example_to_track))


    data_loader = DataLoader(dataset, batch_size=10, shuffle=False, collate_fn=collate_fn)  # 假设批量大小为4

    # print(data_loader)
    # for batch_idx, (mixed_signal, ilens, ys_wav_pad) in enumerate(data_loader):
    #     print(batch_idx)
    #     print("mixed_signal", mixed_signal)

    #     print("ilens", ilens)
    #     print("ys_wav_pad", ys_wav_pad)
    #     print("ys_wav_pad", type(ys_wav_pad))
    #     print("hw")
    #     sys.exit(-1)