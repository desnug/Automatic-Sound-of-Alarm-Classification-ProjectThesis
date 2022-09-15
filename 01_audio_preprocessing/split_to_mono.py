# Python3 program to illustrate
# splitting stereo audio to mono
# using pydub

# Import AudioSegment from pydub
from pydub import AudioSegment

# Open the stereo audio file as
# an AudioSegment instance
stereo_audio = AudioSegment.from_file(
    "audio_data/fire_alarm_0.wav",
    format="wav")

# Calling the split_to_mono method
# on the stereo audio file
mono_audios = stereo_audio.split_to_mono()

# Exporting/Saving the two mono
# audio files present at index 0(left)
# and index 1(right) of list returned
# by split_to_mono method
mono_left = mono_audios[0].export(
    "audio_data/fire_alarm_monoL.wav",
    format="wav")
mono_right = mono_audios[1].export(
    "audio_data/fire_alarm_monoR.wav",
    format="wav")
