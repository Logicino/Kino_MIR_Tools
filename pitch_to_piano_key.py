import numpy as np
import os

def freq_to_piano_key(freq_list, concert_pitch=440, temperament=12):
    # 确保输入是一个NumPy数组
    freq_array = np.asarray(freq_list)
    
    # 检查concert_pitch是否为数字
    if not isinstance(concert_pitch, (int, float)):
        raise TypeError("'concert_pitch' must be a number.")
    
    # 使用NumPy的log2函数并进行向量化计算
    ### 十二平均律 1~88
    if (temperament == 12):
        midi_notes = 49 + 12 * np.log2(freq_array / concert_pitch)
        
    ### 二十四平均律 1~175
    # [27.5, 55.0, 110, 220, 440, 880, 1760, 3520](A0, A1, A2, A3, A4, A5, A6, A7)  => [  1.  25.  49.  73.  97. 121. 145. 169.]
    if (temperament == 24):
        midi_notes = 97 + 24 * np.log2(freq_array / concert_pitch)
        
    # 处理静音频率
    midi_notes[freq_array == 0] = 0  # silent
    
    # 将MIDI音符编号四舍五入到最接近的整数
    midi_notes = np.round(midi_notes)
    
    # 将负值置零
    midi_notes[midi_notes < 0] = 0
    
    return midi_notes

# 使用示例
def demo():
    frequencies = np.load("/data/xyth/Dataset/stringquad/aasesdeath/Cello_f0.npy")
    # frequencies = [27.5, 29.14, 30.87, 3729.31, 3951.07, 4186.01] # A0, A#0, B0, A#7, B7, C8
    # frequencies = [27.5, 55.0, 110, 220, 440, 880, 1760, 3520] # A0, A1, A2, A3, A4, A5, A6, A7
    print(frequencies)

    mapped_keys = freq_to_piano_key(frequencies, temperament=24)  # 计算MIDI音符编号
    print(mapped_keys)  # 输出数组
    np.save("mapped_keys_24.npy", mapped_keys)

## 批量化处理
def main():
    root_dir = "/data/xyth/Dataset/stringquad"
    target_files = {"Violin_1_f0.npy", "Violin_2_f0.npy", "Viola_f0.npy", "Cello_f0.npy"}
    
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file in target_files:
                file_path = os.path.join(subdir, file)
                # 使用freq_to_piano_key函数处理.npy文件
                processed_data = freq_to_piano_key(np.load(file_path), temperament=24)
                
                # 构建新的文件名
                new_file_name = file.replace('.npy', '_note_24.npy')
                new_file_path = os.path.join(subdir, new_file_name)
                
                # 将处理后的数据保存到新的文件
                np.save(new_file_path, processed_data)
                print(f'Processed and saved: {new_file_path}')
                
main()
    
