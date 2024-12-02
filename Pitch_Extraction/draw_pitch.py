import numpy as np
import matplotlib.pyplot as plt

# 指定.npy文件路径
# file_path = '/data/xyth/Dataset/stringquad/train/AlTardarDellaVendetta/Cello_f0_note_12.npy'
file_path = '/data/xyth/Dataset/stringquad/train/AlTardarDellaVendetta/Cello_f0.npy'

# 读取.npy文件
array = np.load(file_path)
# array = array.flatten()
array = array[:1000]

# 输出一维数组
# 检查数组是否为一维
if array.ndim == 1:
    # 绘制一维数组
    plt.figure(figsize=(10, 4))  # 可以指定图像的大小
    plt.plot(array, label='Data')  # 绘制数组
    plt.title('Array Visualization')  # 设置图像标题
    plt.xlabel('Index')  # 设置x轴标签
    plt.ylabel('Value')  # 设置y轴标签
    plt.legend()  # 显示图例
    plt.grid(True)  # 显示网格
    plt.savefig("tmp.jpg")  # 显示图形
else:
    print("The array is not one-dimensional. Please provide a one-dimensional array for visualization.")

def plot_2d(dir, save_name):
    '''
    输入是二维的矩阵
    '''
    # freq_presence_matrix = np.load("/data/xyth/pitch_guided_ensemble_separation/separated_audios_max/est_f0_0.npy")
    # freq_presence_matrix = np.load("/data/xyth/pitch_guided_ensemble_separation/separated_audios/orig_f0_1.npy")
    freq_presence_matrix = np.load(dir)
    # freq_presence_matrix = freq_presence_matrix[:, :2000]
    
    # 时间间隔设置
    time_interval = 0.1  # 10ms一个时间点

    # 创建图形和轴对象
    fig, ax = plt.subplots()

    # 遍历二维矩阵，绘制点
    for freq_index, presence_row in enumerate(freq_presence_matrix):
        time_steps = np.arange(0, len(presence_row) * time_interval, time_interval)
        non_zero_indices = presence_row == 1
        if np.any(non_zero_indices):  # 如果当前频率线有1存在，则绘制
            ax.scatter(time_steps[non_zero_indices], [freq_index] * non_zero_indices.sum(), s=1, color='red')
            # ax.plot(time_steps, [freq_index] * len(time_steps), color='blue', alpha=0.5)  # 统计音高

    # 设置y轴的刻度标签为钢琴音符
    A_notes_positions = [1, 25, 49, 73, 97, 121, 145, 169]  # 24平均律
    ax.set_yticks(A_notes_positions)
    ax.set_yticklabels(['A{}'.format(i) for i in range(0, 8)])  # 从A0到A7

    # 设置图表标题和坐标轴标签
    ax.set_title('Frequency Presence over Time')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Piano note)')

    # 显示图形
    # plt.savefig("freq_presence_24.png")
    plt.savefig(save_name)
