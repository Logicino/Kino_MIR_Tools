import numpy as np
import mir_eval
import soundfile as sf

# def filter_silent_sources(reference_sources, estimated_sources):
#     """过滤掉全零的参考源和对应的估计源"""
#     non_silent_indices = [i for i, source in enumerate(reference_sources) if not np.all(source == 0)]
#     reference_sources = reference_sources[non_silent_indices]
#     estimated_sources = estimated_sources[non_silent_indices]
#     return reference_sources, estimated_sources

def calculate_sdr(reference_sources, estimated_sources, compute_permutation=True):
    """
    使用 mir_eval 计算 SDR。

    参数:
    - reference_sources: np.ndarray, shape=(nsrc, nsampl[, nchan])
                         真实源信号矩阵。
    - estimated_sources: np.ndarray, shape=(nsrc, nsampl[, nchan])
                         估计源信号矩阵。
    - compute_permutation: bool, 是否计算估计源和真实源之间的最佳排列。

    返回:
    - sdr: np.ndarray, shape=(nsrc,)
           每个源的 SDR 值。
    - sir: np.ndarray, shape=(nsrc,)
           每个源的 SIR 值。
    - sar: np.ndarray, shape=(nsrc,)
           每个源的 SAR 值。
    - perm: np.ndarray, shape=(nsrc,)
            最佳排列索引。
    """

    # 计算 SDR、SIR、SAR 和最佳排列
    sdr, sir, sar, perm = mir_eval.separation.bss_eval_sources(
        reference_sources, estimated_sources, compute_permutation=compute_permutation
    )

    return sdr, sir, sar, perm

reference_file = "/data/xyth/Dataset/stringquad_reverb_2seating_for_validation/1-8-CaraSposa/4_Violin_1.wav"
estimate_file = "/data/xyth/LASAFT-Net-v2-stringquad-4ch-cross-attention/results_2_6_2/song_3.wav"

reference_sources, sr = sf.read(reference_file) # 示例真实源信号
estimated_sources, sr = sf.read(estimate_file)

reference_sources = reference_sources[:11862900, :]
estimated_sources = estimated_sources[:11862900, :]

sdr, sir, sar, perm = calculate_sdr(reference_sources, estimated_sources)
print("SDR:", sdr)
print("SIR:", sir)
print("SAR:", sar)
print("Permutation:", perm)