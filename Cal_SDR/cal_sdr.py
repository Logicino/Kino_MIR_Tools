import numpy as np
import soundfile as sf

# def calculate_sdr(reference, estimate):
#     """
#     计算SDR（源失真比）
    
#     参数：
#     reference：参考音频信号，numpy数组，形状为（n_samples, n_channels）
#     estimate：估计音频信号，numpy数组，形状为（n_samples, n_channels）
    
#     返回值：
#     sdr：源失真比，浮点数
#     """
#     # 确保参考信号和估计信号形状相同
#     assert reference.shape == estimate.shape, "参考信号和估计信号形状不一致"
    
#     # 初始化SDR列表
#     sdr_list = []
    
#     # 遍历每个通道
#     for i in range(reference.shape[1]):
#         # 提取当前通道的参考信号和估计信号
#         reference_channel = reference[:, i]
#         estimate_channel = estimate[:, i]
        
#         # 计算当前通道的参考信号能量
#         reference_energy = np.sum(reference_channel ** 2)
        
#         # 计算当前通道的误差信号
#         error = reference_channel - estimate_channel
        
#         # 计算当前通道的误差信号能量
#         error_energy = np.sum(error ** 2)
        
#         # 计算当前通道的SDR
#         sdr_channel = 10 * np.log10(reference_energy / error_energy)
        
#         # 将当前通道的SDR添加到列表中
#         sdr_list.append(sdr_channel)
    
#     # 计算整体SDR（平均值）
#     sdr = np.mean(sdr_list)
    
#     return sdr

def calculate_sdr(references, estimates):
    """
    计算SDR（源失真比）

    参数：
    references：参考音频信号，numpy数组，形状为（n_samples, n_channels）
    estimates：估计音频信号，numpy数组，形状为（n_samples, n_channels）

    返回值：
    sdr_values：每个通道的SDR值，numpy数组，形状为（n_channels,）
    """
    # 确保参考信号和估计信号形状相同
    assert references.shape == estimates.shape, "参考信号和估计信号形状不一致"

    # 初始化SDR列表
    sdr_values = []

    # 遍历每个通道
    for i in range(references.shape[1]):
        # 提取当前通道的参考信号和估计信号
        reference_channel = references[:, i]
        estimate_channel = estimates[:, i]

        # 计算当前通道的参考信号能量
        reference_energy = np.sum(np.square(reference_channel))

        # 计算当前通道的误差信号
        error = reference_channel - estimate_channel

        # 计算当前通道的误差信号能量
        error_energy = np.sum(np.square(error))

        # 计算当前通道的SDR
        sdr_channel = 10 * np.log10(reference_energy / error_energy)

        # 将当前通道的SDR添加到列表中
        sdr_values.append(sdr_channel)

    # 将列表转换为numpy数组
    sdr_values = np.array(sdr_values)

    return sdr_values

# 示例使用
if __name__ == "__main__":
    # 读取参考音频文件和估计音频文件
    # to_test = "2-59-SentiSeLIngannai/Violin_2.wav"

    # reference_file = "/data/xyth/Dataset/stringquad_reverb_2seating_for_training/valid/" + to_test
    # estimate_file = "/data/xyth/Dataset/stringquad_reverb_2seating_for_training/results/" + to_test
    
    reference_file = "/data/xyth/Dataset/stringquad_reverb_2seating_for_validation/2-59-SentiSeLIngannai/4_Violin_1.wav"
    estimate_file = "/data/xyth/LASAFT-Net-v2-stringquad-4ch-cross-attention/results_2_6_2/song_47.wav"
    # 读取音频文件
    reference, sr_reference = sf.read(reference_file)
    estimate, sr_estimate = sf.read(estimate_file)
    
    print(sr_estimate)
    print(sr_reference)
    print(len(reference))
    print(len(estimate))
    
    # 确保采样率相同
    assert sr_reference == sr_estimate, "参考音频和估计音频采样率不一致"
    
    # 定义要使用的音频时长（秒）
    # duration = 25  # 例如，只使用前5秒
    
    # 计算需要截取的采样点数
    # samples = int(duration * sr_reference)
    
    # 截取前几秒的音频信号
    estimate = estimate[:len(reference), :]
    # reference = reference[:6348000, :]
    # estimate = estimate[:6348000, :]
    
    # 计算SDR
    sdr = calculate_sdr(reference, estimate)
    print(sdr)
    mean_sdr = (sdr[0] + sdr[1])/2
    print(f"SDR: {mean_sdr:.2f} dB")