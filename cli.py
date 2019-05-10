import sys
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub.silence import detect_nonsilent
from pydub import AudioSegment

def extract_audio(input_video_path, input_audio_path = './data/test.wav'):
    video = VideoFileClip(input_video_path)
    audio = video.audio
    audio.write_audiofile(input_audio_path, codec='pcm_s16le')

def detect_audio_chunks(input_audio_path = './data/test.wav'):
    audio = AudioSegment.from_wav(input_audio_path)
    dBFS = audio.dBFS
    non_silent_ranges = detect_nonsilent(audio, silence_thresh=dBFS-16)
    return non_silent_ranges
   
def split_video(input_video_path, t1, t2):
    with VideoFileClip(input_video_path) as video:
        # Generate file names
        output_video_path = "./outputs/video_{}_{}.mp4".format(t1,t2)
        output_frame_path = "./outputs/frame_{}.png".format(t1)

        # Save first frame
        new = video.subclip(t1, t2)
        new.save_frame(output_frame_path)
        new.close()
        
        # Save video
        new = video.subclip(t1, t2)
        new.write_videofile(output_video_path, audio_codec='aac')
        new.close()
        
def main():
    input_video_path = sys.argv[1]
    extract_audio(input_video_path)
    chunks = detect_audio_chunks()
    print("Total chunks detected: ", len(chunks))

    for start, end in chunks:
        split_video(input_video_path, start/1000, end/1000)

if __name__ == "__main__":
    main()
