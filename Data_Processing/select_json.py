import json
import random

# 假设原始 JSON 数据存储在文件 'data.json' 中
input_file_path = '/data/xyth/Kino_MIR_Tools/Data_Processing/Remixed_info.json'
# 输出文件路径
output_file_path_m = 'filtered_Remixed_train.json'
output_file_path_n = 'filtered_Remixed_valid.json'
# 需要筛选的歌曲数量
m = 25  # 例如，从 CadenzaWoodwind 中筛选的数量
n = 5  # 例如，从 EnsembleSet 和 Remixed 中筛选的总数量

# 读取原始 JSON 文件
with open(input_file_path, 'r') as file:
    data = json.load(file)

# 获取所有歌曲的键
song_keys = list(data.keys())
print(song_keys)

# 确保 m + n 不超过总歌曲数
assert m + n <= len(song_keys), "m + n 不能超过总歌曲数"

# 随机选择 m 首歌曲
selected_keys_m = random.sample(song_keys, m)

# 从剩余的歌曲中选择 n 首歌曲
remaining_keys = [key for key in song_keys if key not in selected_keys_m]
selected_keys_n = random.sample(remaining_keys, n)

# 创建新的 JSON 数据
filtered_data_m = {key: data[key] for key in selected_keys_m}
filtered_data_n = {key: data[key] for key in selected_keys_n}

# 将筛选后的数据保存到新的 JSON 文件
with open(output_file_path_m, 'w') as file:
    json.dump(filtered_data_m, file, indent=4)

with open(output_file_path_n, 'w') as file:
    json.dump(filtered_data_n, file, indent=4)

print(f"已从原始数据中随机筛选出 {m} 首歌曲，并保存到 {output_file_path_m}")
print(f"已从原始数据中随机筛选出 {n} 首歌曲，并保存到 {output_file_path_n}")