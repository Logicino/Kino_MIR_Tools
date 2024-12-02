import librosa

y, sr = librosa.load('/data/xyth/Dataset/stringquad/train/AlTardarDellaVendetta/Cello.wav')
f0, voiced_flag, voiced_probs = librosa.pyin(y,
                                             sr=sr,
                                             fmin=librosa.note_to_hz('C2'),
                                             fmax=librosa.note_to_hz('C7'))
times = librosa.times_like(f0, sr=sr)

print(f0)