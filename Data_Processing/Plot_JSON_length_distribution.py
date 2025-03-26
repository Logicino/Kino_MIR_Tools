import json
import matplotlib.pyplot as plt

# 读取JSON文件
with open('/data/xyth/Dataset/My_Final_Dataset_s1r2/train.json', 'r') as f:
    json_data = f.read()
# 将JSON字符串转换为字典
data = json.loads(json_data)

# 初始化乐器时间总长度字典
instrument_durations = {}

# 遍历JSON数据，提取乐器时间总长度
for song in data.values():
    for source_info in song.values():
        parts = source_info['instrument'].split('_')
        for part in parts:
            if any(char.isalpha() for char in part):
                instrument_prefix = part
                break  # 找到第一个包含字母的部分后就退出循环
        duration = source_info['duration']
        if instrument_prefix in instrument_durations:
            instrument_durations[instrument_prefix] += duration
        else:
            instrument_durations[instrument_prefix] = duration

# 绘制统计表
instruments = list(instrument_durations.keys())
durations = list(instrument_durations.values())

plt.bar(instruments, durations)
plt.xlabel('Instrument')
plt.ylabel('Total Duration (seconds)')
plt.title('Instrument Duration Statistics')
plt.xticks(rotation=45)  # 旋转x轴标签，避免重叠
plt.tight_layout()  # 自动调整布局
plt.savefig('json.png')