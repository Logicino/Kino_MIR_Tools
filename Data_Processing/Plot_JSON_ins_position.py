import json
import matplotlib.pyplot as plt

# 读取JSON文件
with open('/data/xyth/Dataset/My_Final_Dataset_s1r2/train.json', 'r') as f:
    json_data = f.read()

# 将JSON字符串转换为字典
data = json.loads(json_data)

# 定义乐器列表
instrument_list = ['Bassoon', 'Clarinet', 'Flute', 'Oboe', 'Sax', 'Cello', 'Viola', 'Violin']

# 初始化乐器位置时间总长度字典，位置取值范围为1～5
instrument_position_durations = {instrument: {str(i): 0 for i in range(1, 6)} for instrument in instrument_list}

# 遍历JSON数据，提取乐器位置时间总长度
for song in data.values():
    for source_info in song.values():
        parts = source_info['instrument'].split('_')
        for part in parts:
            if any(char.isalpha() for char in part):
                instrument_prefix = part
                break
        if instrument_prefix in instrument_list:
            position = parts[0]  # 提取位置信息
            duration = source_info['duration']
            if position in instrument_position_durations[instrument_prefix]:
                instrument_position_durations[instrument_prefix][position] += duration

# 为每种乐器绘制并保存图表
for instrument in instrument_list:
    positions = list(instrument_position_durations[instrument].keys())
    durations = list(instrument_position_durations[instrument].values())

    plt.bar(positions, durations, color='skyblue')
    plt.xlabel('Position')
    plt.ylabel('Total Duration (seconds)')
    plt.title(f'{instrument} Position Duration Statistics')
    plt.xticks(ticks=range(1, 6), labels=[str(i) for i in range(1, 6)])  # 明确设置x轴刻度和标签
    plt.tight_layout()  # 自动调整布局
    plt.savefig(f'{instrument}.png', dpi=300)  # 保存图表，设置分辨率为300dpi
    plt.close()  # 关闭图表，避免内存泄漏