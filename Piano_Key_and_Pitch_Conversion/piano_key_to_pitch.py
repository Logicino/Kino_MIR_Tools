### Reference: https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies

def piano_key_to_pitch(piano_key):
    '''
    默认输入piano_key值为1～88
    '''
    freq = 440 * 2 ** ((piano_key - 69)/12)
    
    return freq

piano_key = 60.  # C4
print(piano_key_to_pitch(piano_key))
