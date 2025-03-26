import json

# 假设 JSON 数据存储在文件 'data.json' 中
file_path = '/data/xyth/Kino_MIR_Tools/Data_Processing/Remixed_info.json'

# 读取 JSON 文件
with open(file_path, 'r') as file:
    data = json.load(file)

# 统计歌曲数量
song_count = len(data)

# 输出结果
print(f"该 JSON 文件中共有 {song_count} 首歌曲")