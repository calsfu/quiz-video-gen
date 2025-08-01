from moviepy import VideoClip, CompositeVideoClip, ColorClip
from background_v2 import create_background_clip
import numpy as np

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
VIDEO_RESOLUTION = (VIDEO_WIDTH, VIDEO_HEIGHT)
PADDING = 10
QUESTION_FONT_SIZE = 30
QUESTION_FONT_COLOR = 'white'
QUESTION_FONT_NAME = 'fonts/vag-rounded-bold_gEBUv/VAG Rounded Bold/VAG Rounded Bold.ttf'
NUMBER_FONT_SIZE = 30
NUMBER_FONT_COLOR = 'white'
NUMBER_FONT_NAME = 'fonts/vag-rounded-bold_gEBUv/VAG Rounded Bold/VAG Rounded Bold.ttf'
MAX_IMAGE_WIDTH = 100
MAX_IMAGE_HEIGHT = 100

def make_frame(t, duration=3):
    # Define the bar height, color, and other properties
    bar_height = 20
    bar_color = (255, 0, 0)  # Red bar
    bar_width = (VIDEO_WIDTH - 2 ) * (t / duration)  # Bar width increases over time
    
    # Create a frame with transparent background (all zeros means transparent)
    frame = np.ones((bar_height, VIDEO_WIDTH, 3), dtype=np.uint8) * 255
    
    # Draw the red bar on the frame
    frame[:, :int(bar_width)] = bar_color
    
    return frame

def create_bar_timer_clip(duration):
    transparent_clip = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=(0, 0, 0, 0), duration=duration)
    timer_clip = VideoClip(lambda t: make_frame(t, duration=duration), duration=duration).with_position('bottom')
    final_clip = CompositeVideoClip([transparent_clip, timer_clip])
    return final_clip

def main():
    duration = 3
    background_clip = create_background_clip(duration=duration)
    timer_clip = VideoClip(lambda t: make_frame(t, duration=duration), duration=duration).with_position('bottom')
    final_clip = CompositeVideoClip([background_clip, timer_clip])
    final_clip.write_videofile("videos/bar_timer.mp4", fps=24)

if __name__ == "__main__":
    main()