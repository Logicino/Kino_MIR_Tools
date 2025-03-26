import os

# 设置根目录
root_dir = "/data/xyth/Dataset/My_Final_Dataset_s1r2/Remixed"

# 初始化统计变量
track_count_dict = {}  # 用于记录每个分轨数量对应的歌曲数量

# 遍历根目录下的所有子文件夹
for song_folder in os.listdir(root_dir):
    song_folder_path = os.path.join(root_dir, song_folder)
    
    # 确保是文件夹
    if os.path.isdir(song_folder_path):
        mix_count = 0  # 当前歌曲的分轨文件数量
        
        # 遍历文件夹中的所有文件
        for file_name in os.listdir(song_folder_path):
            if file_name.startswith("mix") != 1 and file_name.endswith(".flac"):
                mix_count += 1
        
        # 如果分轨数量大于0，记录到字典中
        if mix_count > 0:
            if mix_count in track_count_dict:
                track_count_dict[mix_count] += 1
            else:
                track_count_dict[mix_count] = 1

# 输出统计结果
print("分轨数量统计结果：")
for track_count, song_count in sorted(track_count_dict.items()):
    print(f"分轨数量为 {track_count} 的歌曲数量: {song_count}")

# 计算总歌曲数量
total_tracks = sum(track_count_dict.values())
print(f"\n总歌曲数量: {total_tracks}")